# Diagnostico - Fontes PNCP abrindo vazias ou com erro

Data: 2026-05-15

## Problema observado

Durante os testes, algumas oportunidades abriam links de fonte com erro, pagina vazia ou busca sem resultado.

## Causa principal

O Hermes salvava o campo `link` a partir de `linkSistemaOrigem` ou `linkProcessoEletronico`, quando estes vinham na resposta do PNCP. Esses campos podem vir vazios, apontar para sites externos instaveis ou abrir paginas do orgao que ja mudaram de endereco.

Quando o campo `link` estava vazio, o dashboard montava uma URL generica:

```text
https://pncp.gov.br/app/editais?q=<pncp_id>
```

Esse caminho depende da busca do portal. Em alguns casos ele abre sem conteudo visivel, mesmo quando o registro existe na base local.

Tambem havia registros demonstrativos com links falsos no formato `DEMO-*`, o que podia passar a impressao de erro em fonte oficial.

## Ajuste aplicado

1. O backend agora devolve dois links separados para cada oportunidade:
   - `link_pncp`: link publico do PNCP calculado pelo numero de controle.
   - `link_origem`: link externo informado pelo orgao, somente quando for uma URL HTTP/HTTPS valida.

2. O painel deixou de usar a busca generica `app/editais?q=...` como fallback.

3. A tabela agora mostra:
   - `PNCP`, quando existe link oficial calculavel.
   - `Origem`, quando existe link externo valido.
   - `Demo`, quando a oportunidade e demonstrativa.
   - `Sem link`, quando nao ha endereco confiavel.

4. A tela de detalhe agora prioriza o link oficial do PNCP. Se nao houver, usa a origem externa valida.

5. As exportacoes CSV e Excel agora incluem:
   - `link_pncp`
   - `link_origem`
   - `pncp_id`

6. A base demo deixou de gravar links falsos de PNCP para oportunidades `DEMO-*`.

## Como testar

1. Reinicie o Hermes se ele ja estiver aberto:

```powershell
.\scripts\start_demo.ps1
```

2. Acesse:

```text
http://127.0.0.1:8000
```

3. Abra a aba de oportunidades.

4. Na coluna `Fonte`, confira se aparecem links separados:
   - `PNCP`
   - `Origem`
   - `Demo`
   - `Sem link`

5. Clique em `PNCP` em uma oportunidade real.

6. Abra o detalhe da oportunidade e confirme se o botao final abre o PNCP ou a origem externa valida.

7. Exporte CSV ou Excel e confira se os campos `link_pncp` e `link_origem` aparecem separados.

## Observacao operacional

Se um link `Origem` continuar abrindo erro, isso normalmente indica problema no site do orgao comprador, nao no Hermes. O link `PNCP` deve ser usado como referencia principal na demo vendavel, porque ele e mais consistente para rastreabilidade publica.

## Proximo refinamento recomendado

Criar um validador de fontes que rode periodicamente e classifique cada oportunidade como:

- `PNCP ok`
- `Origem ok`
- `Origem instavel`
- `Sem link externo`

Esse status pode aparecer no painel e na planilha para aumentar a confiabilidade comercial da apresentacao.
