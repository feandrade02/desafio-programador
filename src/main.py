import sys
import os
from parsers.time_card_parser import TimeCardParser
from parsers.payroll_parser import PayrollParser

class MainApplication:
    """
    Classe principal que gerencia a interface de linha de comando e
    orquestra o processamento dos documentos.
    """
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)

    def _show_menu(self):
        """Exibe o menu de opções para o usuário."""
        print("\n--- Transcrição de Documentos PDF ---")
        print("Escolha uma opção:")
        print("1 - Transcrever Holerite")
        print("2 - Transcrever Cartão de Ponto")
        print("3 - Encerrar programa")
        print("---------------------------------")

    def _process_document(self, parser_class, doc_type: str):
        """
        Lida com o fluxo de pedir os arquivos e chamar o parser.
        
        Args:
            parser_class: A classe do parser a ser usada (ex: TimeCardParser).
            doc_type (str): O tipo de documento (ex: 'holerite', 'cartão de ponto').
        """
        try:
            input_pdf_path = input(f"Digite o caminho para o PDF do {doc_type}: ")
            output_filename = input(f"Digite o nome do arquivo de saída (ex: saida.xlsx): ")
            
            output_filepath = os.path.join(self.output_dir, output_filename)

            parser = parser_class(input_pdf_path, output_filepath)
            parser.process()
        except Exception as e:
            print(f"Ocorreu um erro durante o processamento: {e}")

    def run(self):
        """Inicia o loop principal da aplicação."""
        while True:
            self._show_menu()
            choice = input("Opção: ")

            match choice:
                case '1':
                    self._process_document(PayrollParser, "holerite")
                case '2':
                    self._process_document(TimeCardParser, "cartão de ponto")
                case '3':
                    print("Encerrando o programa. Até logo!")
                    sys.exit(0)
                case _:
                    print("Opção inválida. Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    app = MainApplication()
    app.run()