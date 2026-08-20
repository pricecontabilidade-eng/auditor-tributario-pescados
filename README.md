# Auditor Tributário de XML de Pescados — MVP

Sistema local em Python/Streamlit para carregar múltiplos XMLs de NF-e e gerar uma auditoria tributária preliminar por item.

## O que já faz

- lê NF-e XML em lote;
- extrai emitente, destinatário, UF, data, produto, NCM, CFOP e tributos;
- identifica pescados por NCM/descrição;
- interpreta origem fiscal do ICMS;
- calcula a alíquota interestadual-base 7%/12% pela matriz origem x destino;
- sinaliza situações de mercadoria importada que exigem validação da Resolução 13/2012;
- consulta `10_NCM_ANEXOS.md` para NCM x Anexo x cClassTrib;
- consulta a planilha `cClassTrib 2025-11-19.xlsx` para CST, redução e vigência operacional;
- testa Anexo I, Anexo VII e candidato ao art. 137 (in natura);
- compara CST IBS/CBS e cClassTrib do XML com o esperado pela base;
- gera relatório consolidado em Excel e CSV.

## Limites deliberados do MVP

O sistema **não inventa** regras ausentes. Por isso, mantém como pendência:

- benefícios de ICMS específicos de cada Estado enquanto não houver base normativa estadual estruturada;
- conclusão automática da alíquota de 4% para importados sem os dados necessários para validar a Resolução 13/2012 e exceções;
- tratamento material de PIS/COFINS quando a base fornecida contém apenas tabela de CST e não as regras específicas por produto/operação;
- classificação fiscal definitiva do NCM;
- condição `in natura` quando a descrição do XML não for suficiente.

## Instalação

Requer Python 3.10 ou superior.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá a interface. Se não abrir, acesse o endereço exibido pelo Streamlit, normalmente `http://localhost:8501`.

## Base tributária

A pasta `base_tributaria` contém os arquivos operacionais utilizados pelo MVP. Para atualização futura, substitua os arquivos mantendo os nomes/estrutura esperados ou adapte `app/knowledge.py`.

## Evolução recomendada para produção

1. estruturar legislação de ICMS por UF em tabelas versionadas por vigência;
2. criar regra completa da Resolução 13/2012 e CAMEX;
3. estruturar legislação de PIS/COFINS por NCM/operação/data;
4. incluir todas as regras de transição IBS/CBS por ano;
5. registrar trilha de auditoria (fonte, versão e regra usada em cada decisão);
6. adicionar autenticação, banco de dados e histórico de processamentos;
7. criar testes automatizados com XMLs reais anonimizados e casos fiscais de referência.
