# CST PIS/Pasep e COFINS - Regras para Auditoria

## Objetivo

Esta base contém os Códigos de Situação Tributária - CST utilizados
nas operações de saída para PIS/Pasep e COFINS.

O Auditor deve utilizar esta tabela em conjunto com a legislação
específica aplicável ao produto e à operação.

O CST não deve ser determinado apenas pelo NCM.

Primeiro deve ser identificado o tratamento tributário previsto na
legislação e, em seguida, comparado o CST esperado com o CST informado
no XML da NF-e.

---

## CST 01 - Operação Tributável com Alíquota Básica

Código:

01

Descrição:

Operação Tributável com Alíquota Básica.

Aplicação:

Utilizado quando a receita da operação estiver normalmente sujeita
às alíquotas básicas do PIS/Pasep e da COFINS.

No regime cumulativo, as alíquotas básicas são normalmente:

- PIS/Pasep: 0,65%
- COFINS: 3,00%

No regime não cumulativo, as alíquotas básicas são normalmente:

- PIS/Pasep: 1,65%
- COFINS: 7,60%

IMPORTANTE:

O Auditor não deve aplicar CST 01 automaticamente apenas porque
determinado produto não está contemplado por uma regra de alíquota zero.

Deve pesquisar previamente outro tratamento tributário aplicável.

---

## CST 02 - Operação Tributável com Alíquota Diferenciada

Código:

02

Descrição:

Operação Tributável com Alíquota Diferenciada.

Aplicação:

Utilizado quando legislação específica determinar tributação por
alíquota diferente da alíquota básica.

---

## CST 03 - Operação Tributável por Unidade de Medida de Produto

Código:

03

Descrição:

Operação Tributável por Unidade de Medida de Produto.

Aplicação:

Utilizado nas hipóteses em que a contribuição é determinada com base
em quantidade ou unidade de medida, conforme legislação específica.

---

## CST 04 - Operação Tributável Monofásica - Revenda a Alíquota Zero

Código:

04

Descrição:

Operação Tributável Monofásica - Revenda a Alíquota Zero.

Aplicação:

Utilizado nas receitas decorrentes da revenda de produtos submetidos
à tributação concentrada ou monofásica na etapa anterior.

IMPORTANTE:

Não confundir CST 04 com CST 06.

CST 04 depende da existência de regime monofásico específico.

---

## CST 05 - Operação Tributável por Substituição Tributária

Código:

05

Descrição:

Operação Tributável por Substituição Tributária.

Aplicação:

Utilizado quando houver regime de substituição tributária das
contribuições previsto em legislação específica.

---

## CST 06 - Operação Tributável a Alíquota Zero

Código:

06

Descrição:

Operação Tributável a Alíquota Zero.

Aplicação:

Utilizado quando a legislação reduz expressamente a zero as alíquotas
do PIS/Pasep e da COFINS incidentes sobre a receita da operação.

Resultado esperado:

- CST PIS: 06
- CST COFINS: 06
- Alíquota PIS: 0%
- Alíquota COFINS: 0%

### Aplicação aos pescados da Lei 12.839/2013

Quando atendidas as condições previstas na legislação específica:

- 0302, exceto 03029000
- 0303
- 0304

o tratamento esperado desta base é:

- PIS: ALÍQUOTA ZERO
- COFINS: ALÍQUOTA ZERO
- CST PIS esperado: 06
- CST COFINS esperado: 06

Fundamento:

Lei nº 10.925/2004, art. 1º, inciso XX,
com redação dada pela Lei nº 12.839/2013.

---

## CST 07 - Operação Isenta das Contribuições

Código:

07

Descrição:

Operação Isenta das Contribuições.

Aplicação:

Utilizado quando houver hipótese legal de ISENÇÃO.

IMPORTANTE:

ISENÇÃO não é equivalente a ALÍQUOTA ZERO.

Portanto:

- CST 06 = alíquota zero
- CST 07 = isenção

Se a legislação aplicável determinar redução da alíquota a zero e
o XML apresentar CST 07, o Auditor deverá apontar divergência,
salvo existência de outro fundamento legal que justifique a isenção.

---

## CST 08 - Operação sem Incidência das Contribuições

Código:

08

Descrição:

Operação sem Incidência das Contribuições.

Aplicação:

Utilizado quando a receita estiver fora do campo de incidência das
contribuições, conforme legislação aplicável.

Exemplo geral:

- determinadas operações de exportação.

IMPORTANTE:

Não confundir não incidência com isenção ou alíquota zero.

---

## CST 09 - Operação com Suspensão das Contribuições

Código:

09

Descrição:

Operação com Suspensão das Contribuições.

Aplicação:

Utilizado quando legislação específica determinar a suspensão da
exigência do PIS/Pasep e da COFINS.

IMPORTANTE:

Suspensão não significa alíquota zero nem isenção.

---

## CST 49 - Outras Operações de Saída

Código:

49

Descrição:

Outras Operações de Saída.

Aplicação:

Utilizado nas hipóteses próprias previstas na tabela CST quando a
operação de saída não se enquadrar nos códigos anteriores.

O Auditor não deve utilizar CST 49 como solução automática para
operações sem regra identificada.

---

# Regras de comparação do Auditor

## REGRA CST_PISCOFINS_001

Se:

- legislação aplicável = ALÍQUOTA ZERO

Então:

- CST PIS esperado = 06
- CST COFINS esperado = 06

Se XML = 06:

STATUS = CORRETO

Se XML diferente de 06:

STATUS = DIVERGENTE

ALERTA:

CST informado incompatível com tratamento legal de alíquota zero.

---

## REGRA CST_PISCOFINS_002

Se:

- legislação aplicável = ISENÇÃO

Então:

- CST esperado = 07

Não utilizar CST 06 apenas porque o valor da contribuição é zero.

---

## REGRA CST_PISCOFINS_003

Se:

- legislação aplicável = NÃO INCIDÊNCIA

Então:

- CST esperado = 08

---

## REGRA CST_PISCOFINS_004

Se:

- legislação aplicável = SUSPENSÃO

Então:

- CST esperado = 09

---

## REGRA CST_PISCOFINS_005

Se:

- produto submetido a regime monofásico
- operação caracterizada como revenda a alíquota zero

Então:

- CST esperado = 04

Exigir fundamento legal específico.

---

# Regra especial para pescados

Para NCM iniciado por:

- 0302, exceto 03029000
- 0303
- 0304

quando a operação estiver abrangida pela regra de alíquota zero da
Lei nº 10.925/2004, art. 1º, XX:

- CST PIS esperado = 06
- CST COFINS esperado = 06
- PIS esperado = 0%
- COFINS esperado = 0%

Se o XML apresentar CST 07:

STATUS:

DIVERGENTE

ALERTA:

Operação enquadrada em alíquota zero, porém XML utiliza CST 07
(Isenção). Validar e corrigir para CST 06 quando confirmado o
enquadramento legal.

---

# Crustáceos e moluscos

Para:

- 0306 - crustáceos
- 0307 - moluscos

não aplicar automaticamente CST 06 com fundamento exclusivo na
Lei nº 12.839/2013.

Exemplos:

- camarão
- lagosta
- caranguejo
- siri
- lula
- polvo
- mexilhão
- ostra

O Auditor deverá pesquisar outra base legal aplicável antes de
determinar o CST esperado.

Na ausência de fundamento suficiente:

STATUS:

PENDENTE DE VALIDACAO

Não presumir automaticamente CST 01.

---

# Hierarquia de decisão

O Auditor deverá seguir esta ordem:

1. Identificar NCM.
2. Verificar descrição do produto.
3. Identificar natureza da operação.
4. Identificar regime tributário aplicável.
5. Pesquisar legislação específica do produto/operação.
6. Determinar tratamento do PIS/Pasep e COFINS.
7. Determinar CST esperado.
8. Comparar com CST informado no XML.
9. Gerar status e alerta.

---

# Resultado visual

CORRETO:

- Verde

DIVERGENTE:

- Vermelho

PENDENTE DE VALIDACAO:

- Amarelo

---

# Observação de segurança tributária

O valor zero de PIS ou COFINS no XML não é suficiente para determinar
o CST correto.

O Auditor deve distinguir juridicamente:

- alíquota zero;
- isenção;
- não incidência;
- suspensão;
- tributação monofásica;
- substituição tributária.

A classificação final deverá ser baseada no fundamento legal aplicável
à operação e na legislação vigente na data de emissão do documento.
