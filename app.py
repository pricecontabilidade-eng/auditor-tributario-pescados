from pathlib import Path
import pandas as pd
import streamlit as st
from app.xml_parser import parse_nfe
from app.knowledge import KnowledgeBase
from app.rules import audit_item
from app.report import dataframe_to_xlsx

st.set_page_config(page_title='Auditor Tributário de Pescados', layout='wide')
st.title('Auditor Tributário de XML de Pescados')
st.caption('MVP local: leitura de NF-e XML + NCM/origem + ICMS interestadual-base + IBS/CBS por base parametrizada. Resultados pendentes exigem validação normativa.')

BASE=Path(__file__).parent/'base_tributaria'
@st.cache_resource
def kb(): return KnowledgeBase(BASE)

files = st.file_uploader(
    'Selecione um ou vários XMLs de NF-e',
    type=['xml'],
    accept_multiple_files=True
)

if files:
    rows = []
    errors = []

    for f in files:
        try:
            h, items = parse_nfe(f.getvalue())

            for it in items:
                rows.append(audit_item(h, it, kb()))

        except Exception as e:
            errors.append(f'{f.name}: {e}')

    if errors:
        st.error('\n'.join(errors))

    if rows:
        df = pd.DataFrame(rows)

        ordem_colunas = [
    "NF-e",
    "Chave",
    "Data",
    "Item",
    "Produto",
    "NCM",
    "Pescado?",
    "CFOP",
    "Origem código",
    "Origem descrição",
    "UF Origem",
    "UF Destino",

    "CST/CSOSN ICMS XML",
    "Alíquota ICMS XML",
    "Alíquota ICMS base esperada",
    "Nota ICMS",

    "CST PIS XML",
    "CST PIS esperado",
    "Aliquota PIS esperada",
    "PIS XML",

    "CST COFINS XML",
    "CST COFINS esperado",
    "Aliquota COFINS esperada",
    "COFINS XML",

    "Tratamento PIS/COFINS",
    "Fundamento PIS/COFINS",

    "CST IBS/CBS XML",
    "CST IBS/CBS esperado",
    "cClassTrib XML",
    "cClassTrib esperado",
    "Redução IBS %",
    "Redução CBS %",
    "Enquadramento IBS/CBS",

    "Status",
    "Alertas",
] 

        colunas_existentes = [
            c for c in ordem_colunas
            if c in df.columns
        ]

        outras_colunas = [
            c for c in df.columns
            if c not in colunas_existentes
        ]

        df = df[colunas_existentes + outras_colunas]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            'NF-es',
            df['Chave'].nunique()
        )

        c2.metric(
            'Itens',
            len(df)
        )

        c3.metric(
            'Pescados identificados',
            (df['Pescado?'] == 'SIM').sum()
        )

        c4.metric(
            'Divergentes',
            (df['Status'] == 'DIVERGENTE').sum()
        )

        st.subheader('Resultado consolidado')

def destacar_status(row):
    status = str(row.get("Status", "")).upper()

    if status == "CORRETO":
        cor = "background-color: #C6EFCE; color: #006100;"
    elif status == "DIVERGENTE":
        cor = "background-color: #FFC7CE; color: #9C0006;"
    else:
        cor = "background-color: #FFEB9C; color: #9C6500;"

    return [cor] * len(row)


df_visual = df.style.apply(destacar_status, axis=1)

st.dataframe(
    df_visual,
    use_container_width=True,
    height=520
)

st.download_button(
            'Baixar relatório Excel',
            data=dataframe_to_xlsx(df),
            file_name='auditoria_pescados.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

st.download_button(
            'Baixar CSV',
            data=df.to_csv(index=False).encode('utf-8-sig'),
            file_name='auditoria_pescados.csv',
            mime='text/csv'
        )

 st.info(
     'Importante: benefícios estaduais de ICMS, regra de 4% para '
     'importados e enquadramento material de PIS/COFINS permanecem '
     'conservadoramente como pendências quando faltarem dados para '
     'uma conclusão segura.'
  )

else:
    st.write('Carregue os XMLs para iniciar a auditoria.')
