from pathlib import Path

from app.xml_parser import parse_nfe
from app.rules import interstate_base_rate, imported_interstate_rate, audit_item
from app.knowledge import KnowledgeBase
def test_parse_nfe_basico():
    """
    Smoke test do parser de NF-e.

    Valida se uma NF-e mínima é interpretada corretamente
    e se os principais campos do cabeçalho e do item são
    disponibilizados pelo parser.
    """

    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
      <NFe>
        <infNFe Id="NFe123">
          <ide>
            <cUF>35</cUF>
            <natOp>VENDA</natOp>
            <mod>55</mod>
            <serie>1</serie>
            <nNF>10</nNF>
            <dhEmi>2026-08-20T10:00:00-03:00</dhEmi>
            <idDest>2</idDest>
            <indFinal>0</indFinal>
          </ide>

          <emit>
    <CNPJ>12345678000199</CNPJ>
    <xNome>EMPRESA EMITENTE</xNome>
    <enderEmit>
        <xMun>SAO PAULO</xMun>
        <UF>SP</UF>
    </enderEmit>
    <CRT>3</CRT>
</emit>

<dest>
    <CNPJ>98765432000199</CNPJ>
    <xNome>EMPRESA DESTINATARIA</xNome>
    <enderDest>
        <xMun>SALVADOR</xMun>
        <UF>BA</UF>
    </enderDest>
</dest>

          <det nItem="1">
            <prod>
              <cProd>001</cProd>
              <xProd>PEIXE CONGELADO</xProd>
              <NCM>03038990</NCM>
              <CEST>0300100</CEST>
              <CFOP>6102</CFOP>
              <uCom>KG</uCom>
              <qCom>10.0000</qCom>
              <vUnCom>20.0000</vUnCom>
              <vProd>200.00</vProd>
            </prod>

            <imposto>
              <ICMS>
                <ICMS00>
                  <orig>0</orig>
                  <CST>00</CST>
                  <modBC>3</modBC>
                  <vBC>200.00</vBC>
                  <pICMS>7.00</pICMS>
                  <vICMS>14.00</vICMS>
                </ICMS00>
              </ICMS>

              <PIS>
                <PISAliq>
                  <CST>01</CST>
                  <vBC>200.00</vBC>
                  <pPIS>1.65</pPIS>
                  <vPIS>3.30</vPIS>
                </PISAliq>
              </PIS>

                             <COFINS>
                    <COFINSAliq>
                        <CST>01</CST>
                        <vBC>200.00</vBC>
                        <pCOFINS>7.60</pCOFINS>
                        <vCOFINS>15.20</vCOFINS>
                    </COFINSAliq>
                </COFINS>

                <IBSCBS>
                    <CST>000</CST>
                    <cClassTrib>000001</cClassTrib>
                    <vBC>200.00</vBC>

                    <gIBSUF>
                        <pIBSUF>0.10</pIBSUF>
                        <vIBSUF>0.20</vIBSUF>
                    </gIBSUF>

                    <gIBSMun>
                        <pIBSMun>0.00</pIBSMun>
                        <vIBSMun>0.00</vIBSMun>
                    </gIBSMun>

                    <gCBS>
                        <pCBS>0.90</pCBS>
                        <vCBS>1.80</vCBS>
                    </gCBS>
                </IBSCBS>
                  
            </imposto>
          </det>
        </infNFe>
      </NFe>
    </nfeProc>
    """

    header, items = parse_nfe(xml)

    # ---------------------------------------------------------
    # Cabeçalho
    # ---------------------------------------------------------
    assert header.numero == "10"
    assert header.serie == "1"
    assert header.emit_uf == "SP"
    assert header.dest_uf == "BA"
    assert header.natureza_operacao == "VENDA"

    # ---------------------------------------------------------
    # Quantidade de itens
    # ---------------------------------------------------------
    assert len(items) == 1

    item = items[0]

    # ---------------------------------------------------------
    # Produto
    # ---------------------------------------------------------
    assert item.codigo == "001"
    assert item.descricao == "PEIXE CONGELADO"
    assert item.ncm == "03038990"
    assert item.cest == "0300100"
    assert item.cfop == "6102"

    assert item.quantidade == 10.0
    assert item.valor_unitario == 20.0
    assert item.valor_produto == 200.0

    # ---------------------------------------------------------
    # ICMS
    # ---------------------------------------------------------
    assert item.origem == "0"
    assert item.cst_icms == "00"
    assert item.bc_icms == 200.0
    assert item.aliq_icms == 7.0
    assert item.valor_icms == 14.0

    # ---------------------------------------------------------
    # PIS
    # ---------------------------------------------------------
    assert item.cst_pis == "01"
    assert item.bc_pis == 200.0
    assert item.aliq_pis == 1.65
    assert item.valor_pis == 3.30

    # ---------------------------------------------------------
    # COFINS
    # ---------------------------------------------------------
    assert item.cst_cofins == "01"
    assert item.bc_cofins == 200.0
    assert item.aliq_cofins == 7.60
    assert item.valor_cofins == 15.20
    # --------------------------------------------------
    # IBS / CBS
    # --------------------------------------------------
    assert item.cst_ibscbs == "000"
    assert item.cclasstrib == "000001"
    assert item.bc_ibscbs == 200.0

    assert item.aliq_ibs_uf == 0.10
    assert item.valor_ibs_uf == 0.20

    assert item.aliq_ibs_mun == 0.00
    assert item.valor_ibs_mun == 0.00

    assert item.valor_ibs == 0.20

    assert item.aliq_cbs == 0.90
    assert item.valor_cbs == 1.80
def test_interstate_base_rate():
    assert interstate_base_rate("SP", "BA") == 7.0
    assert interstate_base_rate("MG", "RJ") == 12.0
    assert interstate_base_rate("SP", "SP") is None
def test_imported_interstate_rate():
     # Sem informacao suficiente sobre industrializacao: nao concluir 4%
    assert imported_interstate_rate("1") is None
    # Importado sem industrializacao: 4%
    assert imported_interstate_rate(
        "1",
        industrializado=False
    ) == 4.0

    # Industrializado com conteudo de importacao superior a 40%: 4%
    assert imported_interstate_rate(
        "3",
        industrializado=True,
        conteudo_importacao=41.0
    ) == 4.0

    # Exatamente 40%: nao aplica automaticamente 4%
    assert imported_interstate_rate(
        "3",
        industrializado=True,
        conteudo_importacao=40.0
    ) is None

    # Produto enquadrado como sem similar nacional: nao aplica automaticamente
    assert imported_interstate_rate(
        "1",
        industrializado=False,
        sem_similar_nacional=True
    ) is None

    # Origem 2 - estrangeira adquirida no mercado interno
    assert imported_interstate_rate(
        "2",
        industrializado=False
    ) == 4.0

    # PPB: nao aplicar automaticamente 4%
    assert imported_interstate_rate(
        "1",
        industrializado=False,
        ppb=True
    ) is None

    # Gas natural importado: nao aplicar automaticamente 4%
    assert imported_interstate_rate(
        "1",
        industrializado=False,
        gas_natural=True
    ) is None
def test_knowledge_base_pescado():
    kb = KnowledgeBase(Path(__file__).parent / "base_tributaria")

    regras = kb.find_ncm("03038990")
    assert regras

    regra = regras[0]
    assert regra.ncm == "03038990"
    assert regra.anexo == "I"
    assert regra.permitido is True
    assert regra.cclasstrib == "200003"

    info = kb.cclass_info("200003")
    assert info is not None
    assert info["cst"] == "200"
    assert info["pred_ibs"] == 100
    assert info["pred_cbs"] == 100
def test_audit_item_pescado():
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
  <NFe>
    <infNFe Id="NFe123">
      <ide>
        <cUF>35</cUF>
        <natOp>VENDA</natOp>
        <mod>55</mod>
        <serie>1</serie>
        <nNF>10</nNF>
        <dhEmi>2026-08-20T10:00:00-03:00</dhEmi>
        <idDest>2</idDest>
        <indFinal>0</indFinal>
      </ide>

      <emit>
        <CNPJ>12345678000199</CNPJ>
        <xNome>EMPRESA EMITENTE</xNome>
        <enderEmit>
          <xMun>SAO PAULO</xMun>
          <UF>SP</UF>
        </enderEmit>
        <CRT>3</CRT>
      </emit>

      <dest>
        <CNPJ>98765432000199</CNPJ>
        <xNome>EMPRESA DESTINATARIA</xNome>
        <enderDest>
          <xMun>SALVADOR</xMun>
          <UF>BA</UF>
        </enderDest>
      </dest>

      <det nItem="1">
        <prod>
          <cProd>001</cProd>
          <xProd>PEIXE CONGELADO</xProd>
          <NCM>03038990</NCM>
          <CEST>0300100</CEST>
          <CFOP>6102</CFOP>
          <uCom>KG</uCom>
          <qCom>10.0000</qCom>
          <vUnCom>20.0000</vUnCom>
          <vProd>200.00</vProd>
        </prod>

        <imposto>
          <ICMS>
            <ICMS00>
              <orig>0</orig>
              <CST>00</CST>
              <vBC>200.00</vBC>
              <pICMS>7.00</pICMS>
              <vICMS>14.00</vICMS>
            </ICMS00>
          </ICMS>

          <IBSCBS>
            <CST>000</CST>
            <cClassTrib>000001</cClassTrib>
            <vBC>200.00</vBC>
            <gIBSUF>
              <pIBSUF>0.10</pIBSUF>
              <vIBSUF>0.20</vIBSUF>
            </gIBSUF>
            <gIBSMun>
              <pIBSMun>0.00</pIBSMun>
              <vIBSMun>0.00</vIBSMun>
            </gIBSMun>
            <gCBS>
              <pCBS>0.90</pCBS>
              <vCBS>1.80</vCBS>
            </gCBS>
          </IBSCBS>
        </imposto>
      </det>
    </infNFe>
  </NFe>
</nfeProc>
"""

    header, items = parse_nfe(xml)
    item = items[0]

    kb = KnowledgeBase(Path(__file__).parent / "base_tributaria")

    resultado = audit_item(header, item, kb)

    assert resultado["NCM"] == "03038990"
    assert resultado["Pescado?"] == "SIM"
    assert resultado["CST IBS/CBS esperado"] == "200"
    assert resultado["cClassTrib esperado"] == "200003"
    assert resultado["Redução IBS %"] == 100
    assert resultado["Redução CBS %"] == 100
    assert "cClassTrib divergente" in resultado["Alertas"]
    assert "CST IBS/CBS divergente" in resultado["Alertas"]
if __name__ == "__main__":
    test_parse_nfe_basico()
    test_interstate_base_rate()
    test_imported_interstate_rate()
    test_knowledge_base_pescado()
    test_audit_item_pescado()
    print("OK - xml_parser.py e regras interestaduais passaram no smoke test.")
