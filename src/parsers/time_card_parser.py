import pandas as pd
import pdfplumber
import re
from .base_parser import DocumentParser

class TimeCardParser(DocumentParser):

    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)

    def _extract_data(self) -> bool:
        """
        Extrai a tabela do PDF e a armazena no atributo self.data_frame.
        Retorna True em caso de sucesso, False caso contrário.
        """

        columns_headers = [
            'Data', 'Entrada1', 'Saída1', 'Entrada2', 'Saída2',
            'Entrada3', 'Saída3', 'Entrada4', 'Saída4',
            'Entrada5', 'Saída5', 'Entrada6', 'Saída6'
        ]

        processed_data = []

        try:
            with pdfplumber.open(self.input_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    match_month_year = re.search(r'Mês/Ano:\s*(\d{2}/\d{4})', text)
                    
                    if match_month_year:
                        month_year = match_month_year.group(1)
                    else:
                        raise ValueError("Não foi possível encontrar o 'Mês/Ano' no PDF.")
                    
                    table = page.extract_table()
                    if not table or len(table) < 2:
                        continue  # Pula páginas sem tabela válida

                    for row in table[1:]:  # Pula o cabeçalho
                        day_info = row[0]
                        raw_times = row[1]

                        if not day_info or not raw_times:
                            continue # Pula linhas vazias ou inválidas

                        match_day = re.match(r'(\d{2})', day_info)
                        if not match_day:
                            continue  # Pula linhas que não começam com um dia

                        day = match_day.group(1)
                        date_str = f"{day}/{month_year}"

                        row_data = {'Data': date_str}

                        normalized_times = raw_times.replace('-', ':').replace(' ', ':')

                        time_entries = re.findall(r'(\d{2}:\d{2})', normalized_times)
                        time_entries.sort()

                        if time_entries:
                            for i, entry in enumerate(time_entries):
                                if (i + 1) < len(columns_headers):
                                    column_header = columns_headers[i + 1]
                                    row_data[column_header] = entry
                        
                        # Se 'horarios_encontrados' estiver vazio (ex: "Descanso Semanal"),
                        # apenas a data será adicionada

                        processed_data.append(row_data)

                self.data_frame = pd.DataFrame(processed_data, columns=columns_headers)
                return True

        except FileNotFoundError:
            print(f"Erro: O arquivo '{self.input_path}' não foi encontrado.")
            return False 
        except Exception as e:
            print(f"Ocorreu um erro inesperado ao processar o arquivo '{self.input_path}': {e}")
            return False
