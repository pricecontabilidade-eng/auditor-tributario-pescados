from __future__ import annotations
from dataclasses import asdict
from datetime import datetime
import re

ORIGENS={
'0':'Nacional, exceto códigos específicos','1':'Estrangeira - importação direta','2':'Estrangeira - adquirida no mercado interno',
'3':'Nacional com conteúdo de importação superior a 40%','4':'Nacional - processo produtivo básico','5':'Nacional com conteúdo de importação inferior ou igual a 40%',
'6':'Estrangeira - importação direta, sem similar nacional (lista CAMEX)','7':'Estrangeira - adquirida no mercado interno, sem similar nacional (lista CAMEX)'
}
S_SE={'MG','PR','RJ','RS','SC','SP'}
DEST_7={'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MT','MS','PA','PB','PE','PI','RN','RO','RR','SE','TO'}

PROCESSED_WORDS=('EMPANAD','TEMPERAD','COZID','DEFUMAD','CONSERVA','MOLHO','PREPARAD','RECHEAD','ENLATAD','MARINAD')
IN_NATURA_HINTS=('FRESC','REFRIGERAD','CONGELAD','INTEIRO','EVISCERAD','SEM CABECA','SEM CABEÇA')
FISH_HINTS=('PEIX','PESCAD','CAMAR','LAGOST','SIRI','CARANGUE','POLVO','LULA','MOLUS','FILE','FILÉ','SALMAO','SALMÃO','ATUM','BACALHAU','TILAPIA','TILÁPIA')


def interstate_base_rate(orig_uf,dest_uf):
    if not orig_uf or not dest_uf or orig_uf==dest_uf: return None
    return 7.0 if orig_uf in S_SE and dest_uf in DEST_7 else 12.0
def imported_interstate_rate(
    origem,
    industrializado=None,
    conteudo_importacao=None,
    sem_similar_nacional=False,
    ppb=False,
    gas_natural=False,
):
    if origem not in {"1", "2", "3"}:
        return None

    if sem_similar_nacional or ppb or gas_natural:
        return None
    if industrializado is None:
        return None
    if not industrializado:
        return 4.0

    if conteudo_importacao is not None and conteudo_importacao > 40.0:
        return 4.0

    return None

def classify_product(item):
    n=(item.ncm or '').replace('.','')
    d=(item.descricao or '').upper()
    pescado=n.startswith('03') or n.startswith('1604') or n.startswith('1605') or any(k in d for k in FISH_HINTS)
    processed=any(k in d for k in PROCESSED_WORDS) or n.startswith('16')
    natura_hint=any(k in d for k in IN_NATURA_HINTS) and not processed
    return pescado,processed,natura_hint


def audit_item(header,item,kb):
    pescado,processed,natura_hint=classify_product(item)
    ncm=(item.ncm or '').replace('.','').zfill(8) if item.ncm else None
    origem_desc=ORIGENS.get(item.origem,'Origem não mapeada/ausente')
    interna=bool(header.emit_uf and header.dest_uf and header.emit_uf==header.dest_uf)
    base_icms=interstate_base_rate(header.emit_uf,header.dest_uf)
    icms_expected=None; icms_note=''
    if interna:
        icms_note='Operação interna: requer legislação da UF para alíquota e benefícios.'
    elif base_icms is not None:
        if item.origem in {'1','2','3'}:
            icms_note=f'Alíquota interestadual-base da matriz: {base_icms:.0f}%. Origem {item.origem} pode exigir análise da Resolução 13/2012 (4%); validar conteúdo de importação e exceções antes de concluir.'
        elif item.origem in {'6','7'}:
            icms_expected=base_icms
            icms_note=f'Origem sem similar nacional declarada; matriz interestadual-base indica {base_icms:.0f}%, sujeita à validação legal e estadual.'
        else:
            icms_expected=base_icms
            icms_note=f'Matriz interestadual-base indica {base_icms:.0f}%, antes de benefícios/regras estaduais.'

    rules=[r for r in kb.find_ncm(ncm) if r.permitido]
    # Legal priority for this MVP: Anexo I -> VII -> art.137 inferred only if no annex rule
    chosen=None; legal_note=''
    for an in ('I','VII'):
        c=[r for r in rules if r.anexo==an]
        if c:
            chosen=c[0]; break
    if chosen:
        ci=kb.cclass_info(chosen.cclasstrib)
        legal_note=f'NCM localizado como PERMITIDO no Anexo {chosen.anexo}; validar descrição legal, exclusões, operação e vigência. cClassTrib operacional: {chosen.cclasstrib}.'
    elif pescado and natura_hint:
        chosen_cc='200036'; ci=kb.cclass_info(chosen_cc)
        legal_note='Descrição sugere produto pesqueiro in natura. Aplicação do art. 137 depende de validação material da condição in natura. cClassTrib operacional candidato: 200036.'
        chosen=type('Tmp',(),{'anexo':'Art.137','cclasstrib':chosen_cc})()
    else:
        ci=None
        legal_note='Nenhum enquadramento automático seguro em Anexo I/VII; avaliar art. 137 e demais regimes conforme características materiais.'

    cst_expected=ci.get('cst') if ci else None
    cc_expected=chosen.cclasstrib if chosen else None
    red_ibs=ci.get('pred_ibs') if ci else None
    red_cbs=ci.get('pred_cbs') if ci else None

    flags=[]
    if not pescado: flags.append('Item não identificado como pescado com segurança')
        # Regra ICMS/RJ - crustaceos fora da regra geral de 7% da cesta basica
    crustaceo = bool(
        ncm
        and ncm.startswith("0306")
    )

    operacao_interna_rj = (
        header.emit_uf == "RJ"
        and header.dest_uf == "RJ"
    )

    if (
        operacao_interna_rj
        and crustaceo
        and item.aliq_icms is not None
        and abs(item.aliq_icms - 7.0) < 0.01
    ):
        flags.append(
            "ICMS RJ: crustaceo excluido da regra geral de 7% da cesta basica; "
            "validar beneficio ou enquadramento estadual especifico"
        )    
    if item.cclasstrib and cc_expected and item.cclasstrib.zfill(6)!=str(cc_expected).zfill(6): flags.append('cClassTrib divergente')
    if item.cst_ibscbs and cst_expected and item.cst_ibscbs.zfill(3)!=str(cst_expected).zfill(3): flags.append('CST IBS/CBS divergente')
    if item.aliq_icms is not None and icms_expected is not None and abs(item.aliq_icms-icms_expected)>0.01: flags.append('Alíquota ICMS difere da matriz-base (pode haver regra/benefício específico)')
    if item.origem in {'1','2','3'}: flags.append('Validar regra de 4% para importados antes de concluir ICMS')
    flags.append('Benefícios estaduais de ICMS não automatizados sem base normativa por UF')
    flags.append('PIS/COFINS: CST lido, mas enquadramento material exige base legal específica por produto/operação')

    status='CORRETO' if not [f for f in flags if 'divergente' in f.lower()] else 'DIVERGENTE'
    if any('Validar' in f or 'não automatizados' in f or 'exige base' in f for f in flags):
        if status=='CORRETO': status='PENDENTE DE VALIDAÇÃO'

    return {
      'NF-e':header.numero,'Chave':header.chave,'Data':header.data_emissao,'Item':item.item,'Produto':item.descricao,'NCM':ncm,'Pescado?':'SIM' if pescado else 'NÃO/INCERTO',
      'CFOP':item.cfop,'Origem código':item.origem,'Origem descrição':origem_desc,'UF Origem':header.emit_uf,'UF Destino':header.dest_uf,
      'CST/CSOSN ICMS XML':item.cst_icms or item.csosn,'Alíquota ICMS XML':item.aliq_icms,'Alíquota ICMS base esperada':icms_expected,'Nota ICMS':icms_note,
      'CST PIS XML':item.cst_pis,'PIS XML':item.valor_pis,'CST COFINS XML':item.cst_cofins,'COFINS XML':item.valor_cofins,
      'CST IBS/CBS XML':item.cst_ibscbs,'CST IBS/CBS esperado':cst_expected,'cClassTrib XML':item.cclasstrib,'cClassTrib esperado':cc_expected,
      'Redução IBS %':red_ibs,'Redução CBS %':red_cbs,'Enquadramento IBS/CBS':legal_note,'Status':status,'Alertas':' | '.join(flags)
    }
