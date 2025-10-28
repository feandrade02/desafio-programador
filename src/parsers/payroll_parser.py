import pdfplumber
import re
import pandas as pd
import pytesseract
from parsers.base_parser import DocumentParser
from utils.my_functions import binarize_image, parse_value

class PayrollParser(DocumentParser):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)

    def _extract_data(self) -> bool:
        processed_data = []

        try:
            with pdfplumber.open(self.input_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()

                    if not text:
                        return self._extract_with_ocr()

                    tables = page.extract_tables()

                    if not tables or len(tables) < 3:
                        print(f"AVISO: Página pulada por não ter 3 tabelas. Tabelas encontradas: {len(tables)}")
                        continue  # Pula páginas sem tabelas

                    if not text:
                        print(f"AVISO: Página pulada por não ter texto. Conteúdo encontrado: {text}")
                        continue  # Pula páginas sem texto
                    
                    month_year_regex_pattern = r'Mês/Ano:\s*(\d{2}/\d{4})'
                    month_year_match = re.search(month_year_regex_pattern, text)
                    
                    if month_year_match:
                        month_year_str = month_year_match.group(1)
                    else:
                        raise ValueError("Não foi possível encontrar o 'Mês/Ano' no PDF.")

                    month_year = month_year_str.split('\n')[-1].strip()

                    month, year = month_year.split('/')

                    row_data = {
                        'Ano': year.strip(),
                        'Mês': month.strip()
                    }
                    
                    middle_table_all_rows_list = text.split('\n')

                    middle_table_target_rows_list = []

                    # Flag para indicar quando começar a capturar
                    collecting_data = False

                    for row in middle_table_all_rows_list:
                        clean_row = row.strip()
                        
                        # Verifica a linha de fim do loop
                        if clean_row.startswith("T O T A L"):
                            collecting_data = False
                            break
                        
                        # Verifica a linha de início do loop
                        if clean_row == "Código Descrição Qtde. Valor Qtde. Valor":
                            collecting_data = True
                            continue
                        
                        # Se a flag for True e a linha não estiver vazia, é um item de interesse
                        if collecting_data and clean_row:
                            middle_table_target_rows_list.append(clean_row)

                    regex_code_pattern = r'^(\S+)'
                    regex_description_pattern = r'^\S+\s+(.+?)\s+(?=\b\d{1,3}(?:\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b)'
                    regex_value_pattern = r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b'

                    for row in middle_table_target_rows_list:
                        code_match = re.search(regex_code_pattern, row)
                        description_match = re.search(regex_description_pattern, row)
                        values_found = re.findall(regex_value_pattern, row)

                        # Apenas processa se o código e a descrição forem encontrados
                        if code_match and description_match:
                            code = code_match.group(1).strip()
                            description = description_match.group(1).strip()
                            
                            count = len(values_found)
                            if count == 2:
                                row_data[f"({code}) {description} QUANTIDADE"] = parse_value(values_found[0])
                                row_data[f"({code}) {description} VALOR"] = parse_value(values_found[1])
                            else:
                                row_data[f"({code}) {description} VALOR"] = parse_value(values_found[0])

                    bottom_table = tables[2]

                    for row in bottom_table:
                        if not row or type(row[0]) != str:
                            continue
                        if 'BARRACRED COSAN' in row[0]:
                            break
                        for item in row:
                            if type(item) != str:
                                continue
                            if '% Direito PPR' in item:
                                break

                            parts = item.split('\n')
                            if len(parts) == 2:
                                header, value = parts
                                if header.strip(): # Garante que o cabeçalho não está vazio
                                    if '13.' in header:
                                        header = header.replace('.', '°')
                                    row_data[header.strip()] = parse_value(value.strip())

                    processed_data.append(row_data)
            
            if processed_data:
                self.data_frame = pd.DataFrame(processed_data)
                return True
            
        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.input_path}' não foi encontrado.")
            return False 
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar o arquivo '{self.input_path}': {e}")
            return False
        
        return False
    
    def _extract_with_ocr(self) -> bool:
        processed_data = []

        try:
            with pdfplumber.open(self.input_path) as pdf:
                for page in pdf.pages:
                    img = page.to_image(resolution=300)
                    pil_image = img.original
                    processed_image = binarize_image(pil_image)

                    ocr_extracted_text = pytesseract.image_to_string(processed_image, lang='por')

                    if not ocr_extracted_text:
                        print(f"AVISO: Página pulada por não ter texto extraído via OCR.")
                        continue  # Pula páginas sem texto

                    month_year_regex_pattern = r'Período : \s*(\d{2}/\d{4})'
                    month_year_match = re.search(month_year_regex_pattern, ocr_extracted_text)
                    if month_year_match:
                        month_year_str = month_year_match.group(1)
                    else:
                        raise ValueError("Não foi possível encontrar o 'Mês/Ano' no PDF via OCR.")
                    
                    month_year = month_year_str.split(':')[-1].strip()

                    print(f"\nMonth/Year: {month_year}\n")
                    month, year = month_year.split('/')

                    row_data = {
                        'Ano': year.strip(),
                        'Mês': month.strip()
                    }

                    base_code = '(0000)'

                    base_inss_regex = r'Base I\.N\.8\.5\.\s*:\s*([\d.,]+)'
                    base_inss_match = re.search(base_inss_regex, ocr_extracted_text)
                    
                    if base_inss_match:
                        base_inss_value = base_inss_match.group(1).strip()
                        column_header = f"{base_code} Base I.N.S.S."
                        row_data[column_header] = parse_value(base_inss_value)

                    month_fgts_regex = r'(F\.G\.T\.S\. do Mês\s*:\s*[\d.,]+)'
                    month_fgts_match = re.search(month_fgts_regex, ocr_extracted_text)
                    if month_fgts_match:
                        month_fgts_str = month_fgts_match.group(1)
                        print(f"\nMonth FGTS str: {month_fgts_str}\n")

                        column_name, month_fgts_value = month_fgts_str.split(':')
                        column_header = f"{base_code} {column_name.strip()}"
                        row_data[column_header] = parse_value(month_fgts_value.strip())

                    base_irrf_regex = r'(Base I\.R\.R\.F\.\s*:\s*[\d.,]+)'
                    base_irrf_match = re.search(base_irrf_regex, ocr_extracted_text)
                    if base_irrf_match:
                        base_irrf_str = base_irrf_match.group(1)
                        print(f"\nBase I.R.R.F. str: {base_irrf_str}\n")

                        column_name, base_irrf_value = base_irrf_str.split(':')
                        column_header = f"{base_code} {column_name.strip()}"
                        row_data[column_header] = parse_value(base_irrf_value.strip())

                    dep_irrf_regex = r'(Dep\. I\.R\.R\.F\.\s*:\s*[\d.,]+)'
                    dep_irrf_match = re.search(dep_irrf_regex, ocr_extracted_text)
                    if dep_irrf_match:
                        dep_irrf_str = dep_irrf_match.group(1)
                        print(f"\nDep I.R.R.F. str: {dep_irrf_str}\n")

                        column_name, dep_irrf_value = dep_irrf_str.split(':')
                        column_header = f"{base_code} {column_name.strip()}"
                        row_data[column_header] = parse_value(dep_irrf_value.strip())

                    base_fgts_regex = r'(Base FGTS\s*:\s*[\d.,]+)'
                    base_fgts_match = re.search(base_fgts_regex, ocr_extracted_text)
                    if base_fgts_match:
                        base_fgts_str = base_fgts_match.group(1)
                        print(f"\nBase FGTS str: {base_fgts_str}\n")

                        column_name, base_fgts_value = base_fgts_str.split(':')
                        column_header = f"{base_code} {column_name.strip()}"
                        row_data[column_header] = parse_value(base_fgts_value.strip())

                    all_rows_list = ocr_extracted_text.split('\n')

                    regex_description_pattern = r'^[^|]+\s*\|?\s*(.+?)\s+(?=\b\d{1,3}(?:\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b)'
                    regex_value_pattern = r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b|\b\d+,\d{2}\b'

                    for row in all_rows_list:
                        clean_row = row.strip()
                        
                        if clean_row.startswith('Total'):
                            break

                        if clean_row.startswith('Descrição') or not clean_row:
                            continue

                        code = clean_row.split('|')[0].strip()
                        description_match = re.search(regex_description_pattern, clean_row)
                        values_found = re.findall(regex_value_pattern, clean_row)

                        if code and description_match:
                            description = description_match.group(1).strip()
                            
                            count = len(values_found)
                            if count == 2:
                                row_data[f"({code}) {description} REFERENCIA"] = parse_value(values_found[0])
                                row_data[f"({code}) {description} VALOR"] = parse_value(values_found[1])
                            else:
                                row_data[f"({code}) {description} VALOR"] = parse_value(values_found[0])

                    processed_data.append(row_data)

            if processed_data:
                self.data_frame = pd.DataFrame(processed_data)
                return True
            
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar o arquivo '{self.input_path}': {e}")
            return False
        
        return False