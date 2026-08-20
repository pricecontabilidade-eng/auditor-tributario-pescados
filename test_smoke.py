from app.xml_parser import parse_nfe
from app.knowledge import KnowledgeBase
from app.rules import audit_item
from pathlib import Path
XML=b'''<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe"><NFe><infNFe Id="NFe123"><ide><natOp>VENDA</natOp><serie>1</serie><nNF>10</nNF><dhEmi>2026-08-20T10:00:00-03:00</dhEmi><idDest>2</idDest></ide><emit><CNPJ>111</CNPJ><xNome>Emitente</xNome><CRT>3</CRT><enderEmit><UF>SP</UF></enderEmit></emit><dest><CNPJ>222</CNPJ><xNome>Dest</xNome><enderDest><UF>BA</UF></enderDest></dest><det nItem="1"><prod><cProd>1</cProd><xProd>PEIXE CONGELADO</xProd><NCM>03038990</NCM><CFOP>6102</CFOP><uCom>KG</uCom><qCom>10</qCom><vUnCom>20</vUnCom><vProd>200</vProd></prod><imposto><ICMS><ICMS00><orig>0</orig><CST>00</CST><vBC>200</vBC><pICMS>7</pICMS><vICMS>14</vICMS></ICMS00></ICMS><PIS><PISOutr><CST>49</CST><vBC>200</vBC><pPIS>0</pPIS><vPIS>0</vPIS></PISOutr></PIS><COFINS><COFINSOutr><CST>49</CST><vBC>200</vBC><pCOFINS>0</pCOFINS><vCOFINS>0</vCOFINS></COFINSOutr></COFINS></imposto></det></infNFe></NFe></nfeProc>'''
h,items=parse_nfe(XML)
kb=KnowledgeBase(Path(__file__).parent/'base_tributaria')
r=audit_item(h,items[0],kb)
assert r['NF-e']=='10'
assert r['UF Origem']=='SP' and r['UF Destino']=='BA'
assert r['Alíquota ICMS base esperada']==7.0
print('OK',r['NCM'],r['Status'],r['cClassTrib esperado'])
