from __future__ import annotations

from dataclasses import dataclass
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


def _find_all(node, name):
    if node is None:
        return []

    return [el for el in node.iter() if _local(el) == name]


def _child_by_local(node, name):
    if node is None:
        return None

    for child in node:
        if _local(child) == name:
            return child

    return None


def _text(node, name, default=None):
    el = _find_first(node, name)

    if el is None or el.text is None:
        return default

    value = el.text.strip()

    return value if value else default


def _num(node, name):
    value = _text(node, name)

    if value in (None, ""):
        return None

    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def _first_tax_child(container):
    if container is None:
        return None

    for child in container:
        return child

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

    modelo: Optional[str] = None
    tipo_operacao: Optional[str] = None
    finalidade_nfe: Optional[str] = None
    indicador_presenca: Optional[str] = None
    municipio_emitente: Optional[str] = None
    municipio_destinatario: Optional[str] = None


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

    cbenef: Optional[str] = None

    bc_icms_st: Optional[float] = None
    aliq_icms_st: Optional[float] = None
    valor_icms_st: Optional[float] = None

    bc_fcp: Optional[float] = None
    aliq_fcp: Optional[float] = None
    valor_fcp: Optional[float] = None

    bc_fcp_st: Optional[float] = None
    aliq_fcp_st: Optional[float] = None
    valor_fcp_st: Optional[float] = None

    percentual_reducao_bc_icms: Optional[float] = None
    valor_icms_desonerado: Optional[float] = None

    bc_uf_dest: Optional[float] = None
    aliq_fcp_uf_dest: Optional[float] = None
    aliq_icms_uf_dest: Optional[float] = None
    aliq_icms_inter: Optional[float] = None
    percentual_partilha: Optional[float] = None

    valor_fcp_uf_dest: Optional[float] = None
    valor_icms_uf_dest: Optional[float] = None
    valor_icms_uf_remet: Optional[float] = None

    cst_pis: Optional[str] = None
    bc_pis: Optional[float] = None
    aliq_pis: Optional[float] = None
    valor_pis: Optional[float] = None

    cst_cofins: Optional[str] = None
    bc_cofins: Optional[float] = None
    aliq_cofins: Optional[float] = None
    valor_cofins: Optional[float] = None

    cst_ibscbs: Optional[str] = None
    cclasstrib: Optional[str] = None
    bc_ibscbs: Optional[float] = None

    aliq_ibs_uf: Optional[float] = None
    aliq_ibs_mun: Optional[float] = None
    valor_ibs: Optional[float] = None

    aliq_cbs: Optional[float] = None
    valor_cbs: Optional[float] = None

    valor_ibs_uf: Optional[float] = None
    valor_ibs_mun: Optional[float] = None

    reducao_ibs_uf: Optional[float] = None
    reducao_ibs_mun: Optional[float] = None
    reducao_cbs: Optional[float] = None

    aliq_efetiva_ibs_uf: Optional[float] = None
    aliq_efetiva_ibs_mun: Optional[float] = None
    aliq_efetiva_cbs: Optional[float] = None

    valor_diferido_ibs_uf: Optional[float] = None
    valor_diferido_ibs_mun: Optional[float] = None
    valor_diferido_cbs: Optional[float] = None

    valor_credito_presumido_ibs: Optional[float] = None
    valor_credito_presumido_cbs: Optional[float] = None

    desconto: Optional[float] = None
    frete: Optional[float] = None
    seguro: Optional[float] = None
    outras_despesas: Optional[float] = None


def _tax_value(group, *names):
    for name in names:
        value = _num(group, name)

        if value is not None:
            return value

    return None


def parse_nfe(xml_bytes: bytes):
    parser = etree.XMLParser(
        remove_blank_text=True,
        recover=True,
        huge_tree=True,
    )

    root = etree.fromstring(xml_bytes, parser=parser)

    inf = _find_first(root, "infNFe")

    if inf is None:
        raise ValueError(
            "XML não contém grupo infNFe de uma NF-e reconhecível."
        )

    ide = _child_by_local(inf, "ide")
    if ide is None:
        ide = _find_first(inf, "ide")

    emit = _child_by_local(inf, "emit")
    if emit is None:
        emit = _find_first(inf, "emit")

    dest = _child_by_local(inf, "dest")
    if dest is None:
        dest = _find_first(inf, "dest")

    emit_ender = _find_first(emit, "enderEmit")
    dest_ender = _find_first(dest, "enderDest")

    raw_id = inf.get("Id") or ""

    if raw_id.startswith("NFe"):
        chave = raw_id[3:]
    else:
        chave = raw_id or None

    header = InvoiceHeader(
        chave=chave,
        numero=_text(ide, "nNF"),
        serie=_text(ide, "serie"),
        data_emissao=_text(ide, "dhEmi") or _text(ide, "dEmi"),
        natureza_operacao=_text(ide, "natOp"),

        emit_cnpj=_text(emit, "CNPJ") or _text(emit, "CPF"),
        emit_nome=_text(emit, "xNome"),
        emit_uf=_text(emit_ender, "UF"),
        emit_crt=_text(emit, "CRT"),

        dest_doc=(
            _text(dest, "CNPJ")
            or _text(dest, "CPF")
            or _text(dest, "idEstrangeiro")
        ),
        dest_nome=_text(dest, "xNome"),
        dest_uf=_text(dest_ender, "UF"),
        dest_ind_ie=_text(dest, "indIEDest"),

        consumidor_final=_text(ide, "indFinal"),
        id_dest=_text(ide, "idDest"),

        modelo=_text(ide, "mod"),
        tipo_operacao=_text(ide, "tpNF"),
        finalidade_nfe=_text(ide, "finNFe"),
        indicador_presenca=_text(ide, "indPres"),

        municipio_emitente=_text(emit_ender, "xMun"),
        municipio_destinatario=_text(dest_ender, "xMun"),
    )

    items = []

    dets = [
        child
        for child in inf
        if _local(child) == "det"
    ]

    if not dets:
        dets = _find_all(inf, "det")

    for pos, det in enumerate(dets, start=1):

        prod = _child_by_local(det, "prod")
        if prod is None:
            prod = _find_first(det, "prod")

        imposto = _child_by_local(det, "imposto")
        if imposto is None:
            imposto = _find_first(det, "imposto")

        icms_container = _find_first(imposto, "ICMS")
        icms = None

        if icms_container is not None:
            for child in icms_container:
                name = _local(child)

                if name and (
                    name.startswith("ICMS")
                    or name.startswith("ICMSSN")
                ):
                    icms = child
                    break

        difal = _find_first(imposto, "ICMSUFDest")

        pis_container = _find_first(imposto, "PIS")
        pis = _first_tax_child(pis_container)

        cofins_container = _find_first(imposto, "COFINS")
        cofins = _first_tax_child(cofins_container)

        ibscbs = _find_first(imposto, "IBSCBS")

        if ibscbs is None:
            ibscbs = _find_first(det, "IBSCBS")

        g_ibs_uf = _find_first(ibscbs, "gIBSUF")
        g_ibs_mun = _find_first(ibscbs, "gIBSMun")
        g_cbs = _find_first(ibscbs, "gCBS")

        valor_ibs_uf = _tax_value(
            g_ibs_uf,
            "vIBSUF",
            "vIBS",
        )

        valor_ibs_mun = _tax_value(
            g_ibs_mun,
            "vIBSMun",
            "vIBS",
        )

        if (
            valor_ibs_uf is not None
            or valor_ibs_mun is not None
        ):
            valor_ibs = (
                (valor_ibs_uf or 0.0)
                + (valor_ibs_mun or 0.0)
            )
        else:
            valor_ibs = _num(ibscbs, "vIBS")

        valor_credito_presumido_ibs = _tax_value(
            ibscbs,
            "vCredPresIBS",
            "vCredPres",
        )

        valor_credito_presumido_cbs = _tax_value(
            ibscbs,
            "vCredPresCBS",
        )

        item = Item(
            item=det.get("nItem") or str(pos),

            codigo=_text(prod, "cProd"),
            descricao=_text(prod, "xProd"),
            ncm=_text(prod, "NCM"),
            cest=_text(prod, "CEST"),
            cfop=_text(prod, "CFOP"),

            unidade=_text(prod, "uCom"),
            quantidade=_num(prod, "qCom"),
            valor_unitario=_num(prod, "vUnCom"),
            valor_produto=_num(prod, "vProd"),

            origem=_text(icms, "orig"),

            cst_icms=_text(icms, "CST"),
            csosn=_text(icms, "CSOSN"),

            bc_icms=_num(icms, "vBC"),
            aliq_icms=_num(icms, "pICMS"),
            valor_icms=_num(icms, "vICMS"),

            cbenef=_text(det, "cBenef"),

            bc_icms_st=_num(icms, "vBCST"),
            aliq_icms_st=_num(icms, "pICMSST"),
            valor_icms_st=_num(icms, "vICMSST"),

            bc_fcp=_num(icms, "vBCFCP"),
            aliq_fcp=_num(icms, "pFCP"),
            valor_fcp=_num(icms, "vFCP"),

            bc_fcp_st=_num(icms, "vBCFCPST"),
            aliq_fcp_st=_num(icms, "pFCPST"),
            valor_fcp_st=_num(icms, "vFCPST"),

            percentual_reducao_bc_icms=_num(
                icms,
                "pRedBC",
            ),

            valor_icms_desonerado=_num(
                icms,
                "vICMSDeson",
            ),

            bc_uf_dest=_num(
                difal,
                "vBCUFDest",
            ),

            aliq_fcp_uf_dest=_num(
                difal,
                "pFCPUFDest",
            ),

            aliq_icms_uf_dest=_num(
                difal,
                "pICMSUFDest",
            ),

            aliq_icms_inter=_num(
                difal,
                "pICMSInter",
            ),

            percentual_partilha=_num(
                difal,
                "pICMSInterPart",
            ),

            valor_fcp_uf_dest=_num(
                difal,
                "vFCPUFDest",
            ),

            valor_icms_uf_dest=_num(
                difal,
                "vICMSUFDest",
            ),

            valor_icms_uf_remet=_num(
                difal,
                "vICMSUFRemet",
            ),

            cst_pis=_text(
                pis,
                "CST",
            ),

            bc_pis=_num(
                pis,
                "vBC",
            ),

            aliq_pis=_tax_value(
                pis,
                "pPIS",
                "vAliqProd",
            ),

            valor_pis=_num(
                pis,
                "vPIS",
            ),

            cst_cofins=_text(
                cofins,
                "CST",
            ),

            bc_cofins=_num(
                cofins,
                "vBC",
            ),

            aliq_cofins=_tax_value(
                cofins,
                "pCOFINS",
                "vAliqProd",
            ),

            valor_cofins=_num(
                cofins,
                "vCOFINS",
            ),

            cst_ibscbs=_text(
                ibscbs,
                "CST",
            ),

            cclasstrib=_text(
                ibscbs,
                "cClassTrib",
            ),

            bc_ibscbs=_num(
                ibscbs,
                "vBC",
            ),

            aliq_ibs_uf=_tax_value(
                g_ibs_uf,
                "pIBSUF",
                "pIBS",
            ),

            aliq_ibs_mun=_tax_value(
                g_ibs_mun,
                "pIBSMun",
                "pIBS",
            ),

            valor_ibs=valor_ibs,

            aliq_cbs=_num(
                g_cbs,
                "pCBS",
            ),

            valor_cbs=_num(
                g_cbs,
                "vCBS",
            ),

            valor_ibs_uf=valor_ibs_uf,
            valor_ibs_mun=valor_ibs_mun,

            reducao_ibs_uf=_tax_value(
                g_ibs_uf,
                "pRedAliq",
                "pRedIBS",
            ),

            reducao_ibs_mun=_tax_value(
                g_ibs_mun,
                "pRedAliq",
                "pRedIBS",
            ),

            reducao_cbs=_tax_value(
                g_cbs,
                "pRedAliq",
                "pRedCBS",
            ),

            aliq_efetiva_ibs_uf=_tax_value(
                g_ibs_uf,
                "pAliqEfet",
                "pAliqEfetiva",
            ),

            aliq_efetiva_ibs_mun=_tax_value(
                g_ibs_mun,
                "pAliqEfet",
                "pAliqEfetiva",
            ),

            aliq_efetiva_cbs=_tax_value(
                g_cbs,
                "pAliqEfet",
                "pAliqEfetiva",
            ),

            valor_diferido_ibs_uf=_tax_value(
                g_ibs_uf,
                "vDif",
                "vDifIBS",
            ),

            valor_diferido_ibs_mun=_tax_value(
                g_ibs_mun,
                "vDif",
                "vDifIBS",
            ),

            valor_diferido_cbs=_tax_value(
                g_cbs,
                "vDif",
                "vDifCBS",
            ),

            valor_credito_presumido_ibs=(
                valor_credito_presumido_ibs
            ),

            valor_credito_presumido_cbs=(
                valor_credito_presumido_cbs
            ),

            desconto=_num(prod, "vDesc"),
            frete=_num(prod, "vFrete"),
            seguro=_num(prod, "vSeg"),
            outras_despesas=_num(prod, "vOutro"),
        )

        items.append(item)

    return header, items
