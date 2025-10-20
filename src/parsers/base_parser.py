import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional

class DocumentParser(ABC):
    """
    Classe base abstrata para parsers de documentos.
    Define a interface comum e a lógica de orquestração para processar
    um documento (extrair dados e salvar).
    """

    def __init__(self, input_path: str, output_path: str):
        """
        Inicializa o parser com os caminhos de entrada e saída.

        Args:
            input_path (str): Caminho para o arquivo PDF de entrada.
            output_path (str): Caminho para o arquivo Excel de saída.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.data_frame: Optional[pd.DataFrame] = None

    @abstractmethod
    def _extract_data(self) -> bool:
        """
        Método abstrato para extrair dados do documento.
        As subclasses devem implementar esta lógica específica.
        Deve retornar True em caso de sucesso, False caso contrário.
        """
        pass

    def _save_to_excel(self) -> bool:
        """
        Salva o DataFrame extraído em um arquivo Excel.
        Retorna True em caso de sucesso, False caso contrário.
        """
        if self.data_frame is None or self.data_frame.empty:
            print("Nenhum dado para salvar. O DataFrame está vazio.")
            return False
        
        try:
            self.data_frame.to_excel(self.output_path, index=False, engine='openpyxl')
            print(f"\nSucesso! Dados foram salvos em '{self.output_path}'")
            return True
        except Exception as e:
            print(f"Erro ao salvar o arquivo Excel em '{self.output_path}': {e}")
            return False

    def process(self):
        """Executa o fluxo completo: extração e salvamento dos dados."""
        print(f"Processando arquivo: {self.input_path}")
        if self._extract_data():
            self._save_to_excel()
