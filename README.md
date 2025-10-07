# Desafio Técnico - Quick Filler

## Objetivo

Este desafio tem como objetivo avaliar suas habilidades técnicas em processamento de documentos, extração de dados e estruturação de informações.

## Descrição do Desafio

Você deverá desenvolver uma aplicação que processe documentos em PDF e extraia informações relevantes de forma estruturada.

### O que você deve fazer:

1. **Ler e processar PDFs de Cartões de Ponto**
   - Extrair informações como: data, horários de entrada/saída, total de horas trabalhadas, etc.

2. **Ler e processar PDFs de Holerites**
   - Extrair informações como: dados do funcionário, salário, descontos, benefícios, etc.

3. **Gerar uma planilha com os dados extraídos**
   - Os dados extraídos devem ser organizados de forma clara e consistente em um arquivo de planilha
   - O formato específico da planilha será fornecido junto com os PDFs

## Requisitos Técnicos

- **Tecnologia**: Você pode utilizar a linguagem de programação e bibliotecas de sua preferência
- **Input**: A aplicação deve receber o caminho dos arquivos PDF como entrada
- **Output**: Gerar um arquivo de planilha (formato será especificado) com os dados extraídos

## Formato da Planilha de Saída

Um arquivo modelo de planilha será fornecido junto com os PDFs. Este arquivo conterá:

- **Estrutura das abas/planilhas** que devem ser preenchidas
- **Cabeçalhos das colunas** esperados
- **Formato dos dados** (datas, valores, etc.)
- **Exemplos** de como os dados devem ser organizados

Sua aplicação deve:
- Ler o arquivo modelo fornecido
- Extrair os dados dos PDFs
- Preencher a planilha seguindo exatamente a estrutura do modelo
- Salvar o arquivo de saída no formato indicado (será especificado: .xlsx, .xls, .ods, .csv, etc.)

**Nota**: A estrutura específica será fornecida no modelo de planilha. Siga-a rigorosamente para garantir compatibilidade com os sistemas da Quick Filler.

## O que será avaliado

1. **Qualidade do Código**
   - Organização e estrutura
   - Boas práticas de programação
   - Legibilidade e manutenibilidade

2. **Precisão na Extração**
   - Capacidade de extrair corretamente as informações dos PDFs
   - Tratamento de diferentes formatos e layouts

3. **Tratamento de Erros**
   - Como a aplicação lida com erros e exceções
   - Validações de entrada

4. **Documentação**
   - README claro com instruções de instalação e uso
   - Comentários no código quando necessário

5. **Testes** (Diferencial)
   - Testes unitários
   - Testes de integração

## Entregáveis

1. **Código-fonte** da aplicação
2. **README.md** com:
   - Instruções de instalação
   - Como executar a aplicação
   - Dependências necessárias
   - Exemplos de uso
3. **Arquivo de planilha** preenchido com os resultados da extração dos PDFs fornecidos

## Como executar (a ser preenchido pelo candidato)

```bash
# Exemplo de estrutura esperada
# Instalar dependências
npm install  # ou pip install -r requirements.txt, etc.

# Executar a aplicação
node cli/parse-time-card.js cartao_ponto.pdf cartao_ponto_transcrito.xlsx
node cli/parse-payroll.js holerite.pdf holerite_transcrito.xlsx
# ou
python parse_time_card.py cartao_ponto.pdf holerite.pdf cartao_ponto_transcrito.xlsx
python parse_payroll.py holerite.pdf holerite.pdf holerite_transcrito.xlsx

# Resultado esperado: arquivo de planilha com a transcrição do cartão de ponto corretamente transcrito
```

## Arquivos de Entrada

Os seguintes arquivos serão fornecidos:
- `cartao_ponto.pdf` - PDF do cartão de ponto *(será fornecido)*
- `holerite.pdf` - PDF do holerite *(será fornecido)*
- `modelo_planilha.[formato]` - Arquivo modelo da planilha de saída *(será fornecido)*

## Prazo

O prazo para entrega será informado ao candidato.

## Dúvidas

Em caso de dúvidas sobre o desafio, entre em contato com o recrutador responsável.

---

**Boa sorte! 🚀**
