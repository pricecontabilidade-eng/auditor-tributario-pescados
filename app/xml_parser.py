from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional
from lxml import etree


def _local(el):
    return etree.QName(el).localname if el is not None else None


def _find_first(node, name):
    if node is None:
        return None
    for el in node.iter():
        if _local(el) == name:
            return el
    return None


def _text(node, name, default=None):
    el = _find_first(node, name)
    return (el.text or '').strip() if el is not None and el.text is not None else default


def _num(node, name):
    v = _text(node, name)
    if v in (None, ''):
        return None
    try:
        return float(v.replace(',', '.'))
    except Exception:
        return None


def _child_by_local(node, name):
    if node is None:
        return None
    for c in node:
        if _local(c) == name:
            return c
    return None


@dataclass
class InvoiceHeader:
    chave: Optional[str]
    numero: Optional[str]
    serie: Optional[str]
    data_emissao: Optional[str]
    natureza_operacao: Optional[str]
    emit_cnpj: Optional[str]
    emit_nome: Optional[str]
    emit_uf: Optional[str]
    emit_crt: Optional[str]
    dest_doc: Optional[str]
    dest_nome: Optional[str]
    dest_uf: Optional[str]
    dest_ind_ie: Optional[str]
    consumidor_final: Optional[str]
    id_dest: Optional[str]


@dataclass
class Item:
    item: str
    codigo: Optional[str]
    descricao: Optional[str]
    ncm: Optional[str]
    cest: Optional[str]
    cfop: Optional[str]
    unidade: Optional[str]
    quantidade: Optional[float]
    valor_unitario: Optional[float]
    valor_produto: Optional[float]
    origem: Optional[str]
    cst_icms: Optional[str]
    csosn: Optional[str]
    bc_icms: Optional[float]
    aliq_icms: Optional[float]
    valor_icms: Optional[float]
    cst_pis: Optional[str]
    bc_pis: Optional[float]
    aliq_pis: Optional[float]
    valor_pis: Optional[float]
    cst_cofins: Optional[str]
    bc_cofins: Optional[float]
    aliq_cofins: Optional[float]
    valor_cofins: Optional[float]
    cst_ibscbs: Optional[str]
    cclasstrib: Optional[str]
    bc_ibscbs: Optional[float]
    aliq_ibs_uf: Optional[float]
    aliq_ibs_mun: Optional[float]
    valor_ibs: Optional[float]
    aliq_cbs: Optional[float]
    valor_cbs: Optional[float]


def parse_nfe(xml_bytes: bytes):
    parser = etree.XMLParser(remove_blank_text=True, recover=True, huge_tree=True)
    root = etree.fromstring(xml_bytes, parser=parser)
    inf = _find_first(root, 'infNFe')
    if inf is None:
        raise ValueError('XML não contém grupo infNFe de uma NF-e reconhecível.')

    ide = _child_by_local(inf, 'ide')
    if ide is None: ide = _find_first(inf, 'ide')
    emit = _child_by_local(inf, 'emit')
    if emit is None: emit = _find_first(inf, 'emit')
    dest = _child_by_local(inf, 'dest')
    if dest is None: dest = _find_first(inf, 'dest')
    emit_ender = _find_first(emit, 'enderEmit')
    dest_ender = _find_first(dest, 'enderDest')

    raw_id = inf.get('Id') or ''
    chave = raw_id[3:] if raw_id.startswith('NFe') else raw_id or None
    header = InvoiceHeader(
        chave=chave,
        numero=_text(ide, 'nNF'),
        serie=_text(ide, 'serie'),
        data_emissao=_text(ide, 'dhEmi') or _text(ide, 'dEmi'),
        natureza_operacao=_text(ide, 'natOp'),
        emit_cnpj=_text(emit, 'CNPJ') or _text(emit, 'CPF'),
        emit_nome=_text(emit, 'xNome'),
        emit_uf=_text(emit_ender, 'UF'),
        emit_crt=_text(emit, 'CRT'),
        dest_doc=_text(dest, 'CNPJ') or _text(dest, 'CPF') or _text(dest, 'idEstrangeiro'),
        dest_nome=_text(dest, 'xNome'),
        dest_uf=_text(dest_ender, 'UF'),
        dest_ind_ie=_text(dest, 'indIEDest'),
        consumidor_final=_text(ide, 'indFinal'),
        id_dest=_text(ide, 'idDest'),
    )

    items = []
    for det in [x for x in inf if _local(x) == 'det']:
        prod = _child_by_local(det, 'prod')
        if prod is None: prod = _find_first(det, 'prod')
        imposto = _child_by_local(det, 'imposto')
        if imposto is None: imposto = _find_first(det, 'imposto')
        icms_container = _find_first(imposto, 'ICMS')
        icms = None
        if icms_container is not None:
            for c in icms_container:
                if _local(c).startswith('ICMS') or _local(c).startswith('ICMSSN'):
                    icms = c
                    break
        pis_container = _find_first(imposto, 'PIS')
        pis = next(iter(pis_container), None) if pis_container is not None and len(pis_container) else None
        cof_container = _find_first(imposto, 'COFINS')
        cof = next(iter(cof_container), None) if cof_container is not None and len(cof_container) else None
        ibs = _find_first(imposto, 'IBSCBS')
        if ibs is None: ibs = _find_first(det, 'IBSCBS')

        orig = _text(icms, 'orig')
        cst = _text(icms, 'CST')
        csosn = _text(icms, 'CSOSN')
        items.append(Item(
            item=det.get('nItem') or str(len(items)+1),
            codigo=_text(prod, 'cProd'), descricao=_text(prod, 'xProd'), ncm=_text(prod, 'NCM'),
            cest=_text(prod, 'CEST'), cfop=_text(prod, 'CFOP'), unidade=_text(prod, 'uCom'),
            quantidade=_num(prod, 'qCom'), valor_unitario=_num(prod, 'vUnCom'), valor_produto=_num(prod, 'vProd'),
            origem=orig, cst_icms=cst, csosn=csosn,
            bc_icms=_num(icms, 'vBC'), aliq_icms=_num(icms, 'pICMS'), valor_icms=_num(icms, 'vICMS'),
            cst_pis=_text(pis, 'CST'), bc_pis=_num(pis, 'vBC'), aliq_pis=_num(pis, 'pPIS'), valor_pis=_num(pis, 'vPIS'),
            cst_cofins=_text(cof, 'CST'), bc_cofins=_num(cof, 'vBC'), aliq_cofins=_num(cof, 'pCOFINS'), valor_cofins=_num(cof, 'vCOFINS'),
            cst_ibscbs=_text(ibs, 'CST'), cclasstrib=_text(ibs, 'cClassTrib'), bc_ibscbs=_num(ibs, 'vBC'),
            aliq_ibs_uf=_num(ibs, 'pIBSUF'), aliq_ibs_mun=_num(ibs, 'pIBSMun'), valor_ibs=_num(ibs, 'vIBS'),
            aliq_cbs=_num(ibs, 'pCBS'), valor_cbs=_num(ibs, 'vCBS'),
        ))
    return header, items
