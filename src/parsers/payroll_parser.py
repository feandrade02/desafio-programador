import pdfplumber
import re
import pandas as pd
from parsers.base_parser import DocumentParser
from utils.parse_values import parse_value

class PayrollParser(DocumentParser):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)

    def _extract_data(self) -> bool:
        processed_data = []

        try:
            with pdfplumber.open(self.input_path) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    text = page.extract_text()

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
                                row_data[f"({code}) {description} VALOR"] = None

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