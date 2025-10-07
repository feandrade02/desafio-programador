# Instruções para o Candidato

## Como Começar

1. **Faça um fork ou clone deste repositório**
2. **Desenvolva sua solução** na linguagem de sua preferência
3. **Teste sua aplicação** com os PDFs fornecidos
4. **Documente seu código** e inclua instruções claras de uso

## Estrutura de Projeto Sugerida

Você é livre para organizar seu projeto como preferir, mas aqui vai uma sugestão:

```
desafio-programador/
├── README.md              # Instruções do desafio
├── SOLUCAO.md            # Sua documentação (a ser criado)
├── src/                  # Código-fonte
│   ├── parsers/          # Módulos de parsing
│   │   ├── time_card.js
│   │   └── payroll.js
│   └── utils/            # Utilitários
├── tests/                # Testes (opcional mas recomendado)
└── requirements.txt      # ou package.json, etc.
```

## Dicas Importantes

### Bibliotecas Úteis

**Python:**
- **PDFs**: `PyPDF2`, `pdfplumber`, `PyMuPDF (fitz)`, `pdfminer.six`, `tabula-py`, `camelot-py`
- **Planilhas**: `openpyxl`, `xlsxwriter`, `pandas` (com `xlrd`/`openpyxl`), `xlwt`

**JavaScript/Node.js:**
- **PDFs**: `pdf-parse`, `pdf-lib`, `pdfjs-dist`
- **Planilhas**: `exceljs`, `xlsx`, `node-xlsx`, `sheetjs`

### Desafios Comuns em Extração de PDFs

1. **PDFs podem ter diferentes layouts**: Tente criar uma solução flexível
2. **Texto pode estar em diferentes encodings**: Considere isso no parsing
3. **Tabelas podem não ser bem estruturadas**: Use heurísticas quando necessário
4. **PDFs escaneados (imagens)**: Se for o caso, pode precisar de OCR (Tesseract)

### O que NÃO fazer

- ❌ Não hardcode valores específicos dos PDFs de teste
- ❌ Não ignore tratamento de erros
- ❌ Não deixe de documentar seu código
- ❌ Não se esqueça de incluir as dependências no arquivo apropriado

### O que FAZER

- ✅ Escreva código limpo e organizado
- ✅ Trate possíveis erros e exceções
- ✅ Valide os dados extraídos
- ✅ Documente suas decisões técnicas
- ✅ Inclua exemplos de uso

## Critérios de Avaliação

### Nível Básico (Essencial)
- Consegue extrair informações básicas dos PDFs
- Código funciona sem erros críticos
- Gera planilha válida no formato correto

### Nível Intermediário
- Extração precisa de todos os campos relevantes
- Código bem organizado e legível
- Tratamento básico de erros
- Documentação clara

### Nível Avançado
- Código robusto com tratamento completo de erros
- Testes automatizados
- Documentação técnica detalhada
- Considera casos extremos (edge cases)

## Entrega

Ao finalizar:
1. Certifique-se de que seu código está funcionando
2. Inclua um arquivo `SOLUCAO.md` explicando sua abordagem
3. Inclua a planilha de saída gerada
4. Envie o link do repositório ou um arquivo ZIP

## Perguntas Frequentes

**Q: Posso usar bibliotecas de terceiros?**
A: Sim, você pode usar quaisquer bibliotecas disponíveis publicamente.

**Q: E se o PDF estiver escaneado (imagem)?**
A: Se precisar, pode usar OCR (como Tesseract), mas documente isso.

**Q: Preciso fazer interface gráfica?**
A: Não, uma interface de linha de comando é suficiente.

**Q: Posso fazer em mais de uma linguagem?**
A: Sim, mas não é necessário. Uma linguagem bem implementada é melhor que várias mal implementadas.

**Q: Quanto tempo tenho para entregar?**
A: O prazo será informado pelo recrutador.

---

**Sucesso no desafio! Estamos ansiosos para ver sua solução! 🎯**
