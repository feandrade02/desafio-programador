# Solução do Desafio Técnico - Quick Filler

## Introdução

Este documento descreve a solução desenvolvida para o Desafio Técnico da Quick Filler. O objetivo do projeto é criar uma aplicação robusta capaz de processar documentos PDF, como holerites e cartões de ponto, extrair informações relevantes e organizá-las de forma estruturada em uma planilha Excel.

### Abordagem Técnica

A aplicação foi desenvolvida em **Python** como uma ferramenta de linha de comando (CLI), priorizando a flexibilidade e a precisão na extração de dados. A abordagem principal é um **sistema híbrido de processamento de PDF**:

1.  **Extração Nativa (Baseada em Texto)**:
    -   Inicialmente, o sistema tenta extrair dados usando a biblioteca `pdfplumber`. Este método é ideal para PDFs "nativos" (gerados digitalmente), pois permite a leitura direta de texto e a identificação de tabelas estruturadas. É a abordagem mais rápida e precisa.

2.  **Extração com OCR (Fallback)**:
    -   Caso a extração nativa falhe em retornar texto (um forte indicativo de que o PDF é uma imagem escaneada), o sistema automaticamente aciona um fluxo de **Reconhecimento Óptico de Caracteres (OCR)**.
    -   Nesse fluxo, a página do PDF é convertida em uma imagem de alta resolução.
    -   A imagem passa por um tratamento de **binarização** para otimizar o contraste e remover ruídos, melhorando significativamente a qualidade do reconhecimento pelo OCR.
    -   A biblioteca `pytesseract`, uma interface para o motor **Tesseract OCR**, é utilizada para extrair o texto da imagem processada.

3.  **Parsing com Expressões Regulares (Regex)**:
    -   Após a obtenção do texto bruto (seja pela via nativa ou por OCR), **expressões regulares (Regex)** são aplicadas de forma intensiva para localizar, validar e extrair os dados específicos de cada campo, como códigos, descrições, valores monetários e datas. Essa técnica garante a captura correta dos dados mesmo com pequenas variações de layout.

4.  **Estruturação e Saída**:
    -   Os dados extraídos são organizados em um `DataFrame` da biblioteca `pandas`, que serve como uma estrutura intermediária robusta.
    -   Finalmente, o `DataFrame` é exportado para um arquivo de planilha no formato **Excel (.xlsx)**, que é salvo no diretório `output/`.

A aplicação é iniciada através do `src/main.py`, que apresenta um menu simples para que o usuário escolha o tipo de documento a ser processado.

---

## Dependências Necessárias

Para que a aplicação funcione corretamente, são necessárias dependências de sistema e de bibliotecas Python.

### Dependências de Sistema

-   **Python 3.10** ou superior.
-   **Tesseract OCR Engine**: Essencial para o processamento de PDFs escaneados.
    -   **Windows**: Pode ser baixado no repositório oficial do Tesseract. Durante a instalação, **certifique-se de adicionar o Tesseract ao PATH do sistema**.
    -   **Linux (Debian/Ubuntu)**: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
    -   **macOS (usando Homebrew)**: `brew install tesseract tesseract-lang`

### Dependências Python

As bibliotecas Python necessárias estão listadas abaixo e podem ser instaladas via `pip`.

-   `pdfplumber`: Para extração de texto e tabelas de PDFs.
-   `pytesseract`: Para a interface com o Tesseract OCR.
-   `pandas`: Para manipulação de dados e criação da planilha Excel.
-   `Pillow`: Dependência para manipulação de imagens (usada pelo `pdfplumber` e no pré-processamento para OCR).
-   `openpyxl`: Motor para escrita de arquivos `.xlsx` com o `pandas`.

---

## Instruções de Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

1.  **Clone o Repositório**

    ```bash
    git clone https://github.com/feandrade02/desafio-programador
    cd desafio-programador
    ```

2.  **Crie um Ambiente Virtual (Recomendado)**

    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual**

    -   **Windows**:
        ```bash
        .\venv\Scripts\activate
        ```
    -   **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```

4.  **Instale as Dependências Python**

    ```bash
    pip install -r requirements.txt
    ```

---

## Como Executar a Aplicação

A aplicação é executada através de um menu interativo.

1.  Navegue até o diretório `src`:
    ```bash
    cd src
    ```

2.  Execute o script principal:
    ```bash
    python main.py
    ```

3.  O programa exibirá um menu. Digite o número da opção desejada (`1` para Holerite, `2` para Cartão de Ponto) e pressione Enter.

4.  Siga as instruções no terminal para fornecer o caminho do arquivo PDF de entrada e o nome desejado para o arquivo de saída.

### Exemplo de Uso

Abaixo, um exemplo de interação com o programa para processar um holerite.

```
--- Transcrição de Documentos PDF ---
Escolha uma opção:
1 - Transcrever Holerite
2 - Transcrever Cartão de Ponto
3 - Encerrar programa
---------------------------------
Opção: 1
Digite o caminho para o PDF do holerite: ./input_pdfs/Exemplo-Holerite-01.pdf
Digite o nome do arquivo de saída (ex: saida.xlsx): holerite_processado.xlsx

Processando o arquivo...
Arquivo 'holerite_processado.xlsx' salvo com sucesso em 'output/'.
```
O arquivo de saída será salvo na pasta `output/` na raiz do projeto.
