# Roteiro e prompt para gerar as imagens do carrossel Hermes (outro assistente)

Use este ficheiro como **briefing único**: pode colar a secção [Prompt pronto para colar](#prompt-pronto-para-colar) noutro chat, ou seguir o roteiro slide a slide.

---

## 1. Objetivo

Gerar **cinco ilustrações vetoriais** no formato **16:9**, estilo **UI conceitual / wireframe de produto**, para o carrossel comercial do site estático Hermes.  
Formato de saída: **SVG** (um ficheiro por slide), prontos para substituir os existentes no repositório.

**Caminho-alvo no projeto (após gerar):**

- `docs/assets/hermes-comercial/slide-01-visao.svg`
- `docs/assets/hermes-comercial/slide-02-score.svg`
- `docs/assets/hermes-comercial/slide-03-comercial.svg`
- `docs/assets/hermes-comercial/slide-04-export.svg`
- `docs/assets/hermes-comercial/slide-05-coleta.svg`

---

## 2. Identidade visual (obrigatório)

| Uso | Cor | Notas |
|-----|-----|--------|
| Marca / fundo escuro | `#0a2342` | Azul Hermes principal |
| Marca secundária | `#163a66` | Degradê com o anterior |
| Destaque / CTA | `#f7931e` | Laranja accent |
| Fundo da página / canvas | `#f5f7fa` | Cinza muito claro |
| Superfície cartão | `#ffffff` | Branco |
| Linhas / bordas suaves | `#d7dee8`, `#e2e8f0`, `#cbd5e1` | Hierarquia de cinzas |
| Texto secundário | `#64748b` | Rodapés, legendas |
| Destaque suave laranja | `#fff1df`, `#fff7ed` | Fundos de destaque |
| Azul claro (e-mail / info) | `#e0f2fe`, `#38bdf8`, `#0ea5e9` | Slide exportação (lado direito) |

**Tipografia em `<text>` (SVG):**

- Títulos fortes: `font-family="Poppins,system-ui,sans-serif"` quando disponível; caso contrário `system-ui,sans-serif`.
- Corpo / legendas: `font-family="system-ui,sans-serif"`, `font-size="12"`–`14"`, `fill="#64748b"`.

**Estilo gráfico:**

- Formas com **cantos arredondados** (`rx` em retângulos).
- **Sem fotografias**; apenas formas, listas fictícias, barras, círculos de progresso, áreas de “conteúdo” em cinza.
- Aparência **profissional B2G / SaaS**, não infantil.

---

## 3. Especificação técnica do SVG (obrigatório)

Cada ficheiro deve cumprir **todos** os pontos abaixo. Se falhar um, o browser pode **não mostrar a imagem** no carrossel.

1. **Raiz**

   ```xml
   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" role="img" aria-labelledby="tN">
   ```

   Substituir `tN` por `t1` … `t5` conforme o slide.

2. **Título acessível** (obrigatório, primeiro filho recomendado):

   ```xml
   <title id="tN">…</title>
   ```

3. **Encoding:** ficheiro gravado em **UTF-8** (preferencialmente **sem BOM**).

4. **Proibido em texto XML:**

   - Qualquer **carácter de controlo** ASCII (U+0000–U+001F), exceto tab, LF, CR. Em especial **nunca** usar o byte `0x14` nem outros controlo “invisíveis” copiados de Word.
   - **Não** misturar Windows-1252 com UTF-8 no mesmo ficheiro.

5. **Travessões e pontuação:** usar apenas Unicode explícito no ficheiro UTF-8, por exemplo:

   - Travessão médio: `–` (U+2013) ou `—` (U+2014)
   - Meio-ponto / separador: `·` (U+00B7)

   Ou usar **ASCII** (`-`, `|`) se quiser máxima simplicidade.

6. **Caracteres portugueses:** `ç`, `ã`, `õ`, `é`, `ê`, etc. como **UTF-8 multibyte correcto** (ex.: “classificação”, “exportação”).

7. **IDs únicos** dentro de cada SVG: gradientes e filtros (`id="g1"`, `id="sh"`, etc.) não devem colidir com uso interno; entre ficheiros diferentes pode repetir.

8. **Validação sugerida** (para o assistente ou para ti, após gerar):

   ```bash
   python -c "import xml.etree.ElementTree as ET; ET.parse('slide-01-visao.svg')"
   ```

9. **Não** depender de fontes externas via `@import` ou URL (o carrossel usa `<img src="…svg">`; fontes web em SVG como imagem podem não carregar).

---

## 4. Roteiro por slide (conteúdo e composição)

### Slide 1 — `slide-01-visao.svg`

- **`<title>`:** `Hermes – visão unificada de oportunidades`
- **Mensagem:** painel executivo com oportunidades priorizadas.
- **Composição sugerida:** fundo `#f5f7fa`; grande cartão com degradê `#0a2342` → `#163a66` e sombra suave (`feDropShadow`); faixa de “filtros” no topo (um chip laranja `#f7931e`, outros chips brancos semi-transparentes); à esquerda bloco de lista fictícia; à direita área branca com linhas de placeholder e uma linha destacada com fundo `#fff1df` e borda laranja.
- **Rodapé (texto em y ≈ 520):** `Painel · oportunidades priorizadas`

### Slide 2 — `slide-02-score.svg`

- **`<title>`:** `Hermes – score e classificação estratégica`
- **Mensagem:** score numérico e lista de razões / classes.
- **Composição:** cartão branco com borda `#d7dee8`; à esquerda **donut** ou arco grosso: círculo base `#e2e8f0`, arco de progresso laranja `#f7931e` com `stroke-dasharray`; número grande **87** ao centro; label “Score”; à direita barra escura `#0a2342` com segmento laranja e três filas de “cards” com linhas placeholder; um card com fundo `#fff7ed`.
- **Rodapé:** `Inteligência · ALTA · MÉDIA · BAIXA`

### Slide 3 — `slide-03-comercial.svg`

- **`<title>`:** `Hermes – funil comercial e acompanhamento`
- **Mensagem:** funil de vendas e campos de acompanhamento.
- **Composição:** título “Acompanhamento comercial”; chips de estado (um laranja, outros cinza); **funil** simplificado (trapézio ou path) em azul muito transparente com nós circulares; painel escuro `#0a2342` à esquerda com linhas placeholder e checklist fictício com quadrado laranja.
- **Rodapé:** `Funil · status · favoritos · anotações`

### Slide 4 — `slide-04-export.svg`

- **`<title>`:** `Hermes – exportação e continuidade`
- **Mensagem:** exportação + e-mail com contexto.
- **Composição:** **metade esquerda** fundo `#0a2342` com zona de “tabela” e dois botões (primário laranja, secundário contorno branco); **metade direita** cartão branco com ícone de e-mail simplificado em azul claro (`#e0f2fe` / `#0ea5e9`); bloco de texto placeholder; caixa âmbar `#fff7ed` com texto pequeno explicando resumo de filtros no corpo do e-mail.
- **Rodapé:** `Exportação · Excel · e-mail contextual`

### Slide 5 — `slide-05-coleta.svg`

- **`<title>`:** `Hermes – coleta PNCP por perfil e coleta geral`
- **Mensagem:** perfis, fila de coleta, área de resultados.
- **Composição:** cartão branco; topo com campo de pesquisa fictício, chip “perfil” em `#fff1df`, botão escuro com detalhe laranja; fila horizontal de **segmentos** (barras arredondadas) simulando progresso de vários perfis; área grande inferior com linhas horizontais tipo tabela/lista.
- **Rodapé:** `PNCP · perfis · coleta geral · histórico`

---

## 5. Referência de layout (slide 1)

O slide 1 actual segue esta lógica de coordenadas (podes pedir ao outro assistente para **manter proporções semelhantes** ou reinterpretar mantendo cores e hierarquia):

- Canvas `960×540`, margens ~48 px.
- Cartão principal central ~864×460, `rx="16"`.

---

## Prompt pronto para colar

Copie o bloco abaixo (entre as linhas) para outro assistente que gere código/SVG.

```
És um designer front-end e vais produzir 5 ficheiros SVG para um carrossel comercial do produto "Hermes" (inteligência em licitações públicas, AtlasNex).

REQUISITOS GERAIS
- viewBox="0 0 960 540", xmlns SVG 2000, role="img", aria-labelledby apontando para <title id="tN"> com N=1..5.
- Estética: UI wireframe B2G, cantos arredondados, sem fotos.
- Paleta: fundo #f5f7fa; azuis #0a2342, #163a66; accent #f7931e; branco #ffffff; cinzas #d7dee8, #e2e8f0, #cbd5e1, #64748b; destaques #fff1df / #fff7ed.
- Ficheiros UTF-8 válidos. PROIBIDO: caracteres de controlo (ex.: byte 0x14), XML inválido, mistura Windows-1252 com UTF-8.
- Usa travessões Unicode (U+2013 ou U+2014) ou ASCII; português correcto (ç, ã, é).
- Não uses fontes remotas por URL.
- Entrega o CONTEÚDO COMPLETO de cada ficheiro, um após o outro, com cabeçalho de ficheiro antes de cada um.

NOMES DOS FICHEIROS
1) slide-01-visao.svg — title: Hermes – visão unificada de oportunidades — painel priorizado; rodapé: Painel · oportunidades priorizadas
2) slide-02-score.svg — title: Hermes – score e classificação estratégica — donut score 87, lista; rodapé: Inteligência · ALTA · MÉDIA · BAIXA
3) slide-03-comercial.svg — title: Hermes – funil comercial e acompanhamento — funil + painel escuro; rodapé: Funil · status · favoritos · anotações
4) slide-04-export.svg — title: Hermes – exportação e continuidade — metade escura export + metade e-mail; rodapé: Exportação · Excel · e-mail contextual
5) slide-05-coleta.svg — title: Hermes – coleta PNCP por perfil e coleta geral — perfis + fila + lista; rodapé: PNCP · perfis · coleta geral · histórico

No fim, indica validação XML, por exemplo:
python -c "import xml.etree.ElementTree as ET, pathlib; [ET.parse(p) for p in pathlib.Path('.').glob('slide-*.svg')]"
(executar na pasta onde gravaste os cinco SVG.)
```

*(Nota: na última linha do prompt, o outro assistente deve completar o comando de validação com os cinco nomes de ficheiro exactos.)*

---

## 6. Depois de receber os SVG

1. Grava os cinco ficheiros em `docs/assets/hermes-comercial/` (substituindo os actuais).
2. Valida XML (comando acima ou abrir num browser: arrastar o SVG para um separador).
3. Abre `docs/index.html` localmente e confirma que o carrossel mostra as imagens.
4. `git add` + commit + push se integrares no repositório.

---

## 7. Alternativa: PNG

Se o outro assistente gerar **PNG** em vez de SVG, será preciso **alterar o HTML** do carrossel em `docs/index.html` (`<img src="…">` para `.png`) e manter proporção **960×540** (ou 1920×1080 com `width`/`height` coerentes). O projecto actual espera **SVG**.
