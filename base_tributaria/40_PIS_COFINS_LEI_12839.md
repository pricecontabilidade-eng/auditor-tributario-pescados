# PIS/COFINS - Lei 12.839/2013 - Pescados e Cesta Básica

## Fonte legal

Lei nº 12.839, de 9 de julho de 2013.

A Lei nº 12.839/2013 alterou o art. 1º da Lei nº 10.925/2004 e reduziu a zero
as alíquotas da Contribuição para o PIS/Pasep e da COFINS incidentes sobre
a receita decorrente da venda no mercado interno de determinados produtos
integrantes da cesta básica.

## Vigência da regra-base

- Publicação: 10/07/2013
- Regra legal: art. 1º da Lei nº 12.839/2013
- A Lei entra em vigor na data de sua publicação.
- Para documentos fiscais posteriores, a vigência material deve ser validada
  considerando alterações legislativas posteriores e regras de transição.

## Produtos de pescado abrangidos

### Posição 03.02

Peixes frescos ou refrigerados.

PERMITIDO para alíquota zero de PIS/COFINS, EXCETO:

- NCM 03029000

Regra:

- 0302, exceto 03029000 -> ALIQUOTA ZERO

### Posição 03.03

Peixes congelados.

Regra:

- 0303 -> ALIQUOTA ZERO

### Posição 03.04

Filés de peixes e outras carnes de peixes.

Regra:

- 0304 -> ALIQUOTA ZERO

## Produtos NÃO abrangidos por esta regra específica

A Lei nº 12.839/2013 não incluiu, no inciso XX analisado, as posições:

- 03.06 - Crustáceos
- 03.07 - Moluscos

Portanto, NÃO aplicar automaticamente a alíquota zero desta Lei aos produtos
classificados nessas posições.

### Exemplos de crustáceos - 03.06

- camarão
- lagosta
- caranguejo
- siri
- outros crustáceos

### Exemplos de moluscos - 03.07

- lula
- polvo
- mexilhão
- ostra
- outros moluscos

IMPORTANTE:

A ausência do produto nesta regra NÃO significa automaticamente que a operação
deva ser tributada pela alíquota básica.

Antes de concluir a tributação, verificar se existe:

- outra hipótese de alíquota zero;
- suspensão;
- isenção;
- não incidência;
- tributação monofásica;
- regime especial;
- tratamento específico por produto ou operação;
- alteração legislativa posterior aplicável à data do documento fiscal.

## CST esperado nas saídas abrangidas

Para venda interna efetivamente beneficiada com ALÍQUOTA ZERO de PIS/Pasep e
COFINS:

- CST PIS esperado: 06
- CST COFINS esperado: 06
- Alíquota PIS esperada: 0%
- Alíquota COFINS esperada: 0%

Descrição do CST 06:

Operação Tributável a Alíquota Zero.

## Diferença entre CST 06 e CST 07

CST 06:

- Operação Tributável a Alíquota Zero.

CST 07:

- Operação Isenta das Contribuições.

Não considerar CST 06 e CST 07 equivalentes.

Quando o fundamento legal for redução da alíquota a zero, o Auditor deverá
esperar CST 06, salvo existência de fundamento legal específico que caracterize
isenção.

## Regras operacionais para o Auditor

### REGRA PIS_COFINS_PESCADOS_001

Condição:

- NCM inicia por 0302
- NCM diferente de 03029000

Resultado esperado:

- Benefício: ALIQUOTA ZERO
- CST PIS esperado: 06
- CST COFINS esperado: 06
- PIS esperado: 0%
- COFINS esperado: 0%

Fundamento:

- Lei 10.925/2004, art. 1º, XX
- redação dada pela Lei 12.839/2013

### REGRA PIS_COFINS_PESCADOS_002

Condição:

- NCM inicia por 0303

Resultado esperado:

- Benefício: ALIQUOTA ZERO
- CST PIS esperado: 06
- CST COFINS esperado: 06
- PIS esperado: 0%
- COFINS esperado: 0%

Fundamento:

- Lei 10.925/2004, art. 1º, XX
- redação dada pela Lei 12.839/2013

### REGRA PIS_COFINS_PESCADOS_003

Condição:

- NCM inicia por 0304

Resultado esperado:

- Benefício: ALIQUOTA ZERO
- CST PIS esperado: 06
- CST COFINS esperado: 06
- PIS esperado: 0%
- COFINS esperado: 0%

Fundamento:

- Lei 10.925/2004, art. 1º, XX
- redação dada pela Lei 12.839/2013

### REGRA PIS_COFINS_PESCADOS_004

Condição:

- NCM igual a 03029000

Resultado:

- NÃO aplicar automaticamente a alíquota zero desta regra.
- Exigir validação de outro fundamento legal.

### REGRA PIS_COFINS_PESCADOS_005

Condição:

- NCM inicia por 0306

Resultado:

- CRUSTÁCEO
- NÃO abrangido automaticamente pela regra de alíquota zero deste arquivo.
- Exigir validação de outra base legal.

Exemplos:

- camarão
- lagosta
- caranguejo
- siri

### REGRA PIS_COFINS_PESCADOS_006

Condição:

- NCM inicia por 0307

Resultado:

- MOLUSCO
- NÃO abrangido automaticamente pela regra de alíquota zero deste arquivo.
- Exigir validação de outra base legal.

Exemplos:

- lula
- polvo
- mexilhão
- ostra

## Validação cruzada NCM x descrição

A classificação tributária deve utilizar prioritariamente o NCM.

A descrição comercial deve ser utilizada como mecanismo adicional de auditoria.

Exemplos de palavras indicativas:

### Crustáceos

- CAMARAO
- CAMARÃO
- LAGOSTA
- CARANGUEJO
- SIRI

### Moluscos

- LULA
- POLVO
- MEXILHAO
- MEXILHÃO
- OSTRA

Se a descrição indicar crustáceo ou molusco, mas o NCM informado estiver
classificado como peixe das posições 0302, 0303 ou 0304:

STATUS:

PENDENTE DE VALIDACAO

ALERTA:

Possível incompatibilidade entre descrição do produto e classificação NCM.

## Resultado visual recomendado

CORRETO:

- Verde

DIVERGENTE:

- Vermelho

PENDENTE DE VALIDACAO:

- Amarelo

## Observação de segurança tributária

O Auditor não deve concluir que um produto é tributado à alíquota básica apenas
porque não está incluído nesta Lei.

A ausência de enquadramento na Lei nº 12.839/2013 significa somente que o
benefício específico aqui analisado não pode ser aplicado automaticamente.

Antes de determinar CST ou alíquota diferente, pesquisar outros fundamentos
legais vigentes na data da operação.
