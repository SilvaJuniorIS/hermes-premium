# Dashboard demo do Hermes Premium

Esta pasta contem uma versao estatica do dashboard para publicacao no GitHub Pages.

## AtlasNex (empresa-mae)

A vitrine institucional da **AtlasNex** (holding do ecossistema) esta em:

```text
docs/atlasnex.html
```

No GitHub Pages, a URL tipica sera `.../atlasnex.html`. A pagina inclui a identidade visual premium (paleta, Exo 2, slogan) e links para a vitrine do Hermes e para o dashboard operacional (URL configuravel).

Para apontar o botao do dashboard para um ambiente publico ou tunel, use query string:

```text
atlasnex.html?hermes_dashboard=https://seu-subdominio.trycloudflare.com
```

O script da pagina atualiza os links do dashboard automaticamente.

O GitHub Pages publica apenas arquivos estaticos. O sistema real do Hermes
usa FastAPI, SQLite, autenticacao por cookie, chamadas ao PNCP e rotinas Python,
por isso deve rodar em um servidor separado ou em uma demo local com tunel.

## Publicar no GitHub Pages

1. Envie a pasta `docs/` para o repositorio no GitHub.
2. No GitHub, acesse `Settings`.
3. Entre em `Pages`.
4. Em `Build and deployment`, escolha `Deploy from a branch`.
5. Selecione a branch principal e a pasta `/docs`.
6. Salve.

O GitHub vai gerar uma URL publica para a demonstracao.

## Link para o sistema real

Quando a versao real estiver hospedada, ajuste o botao principal em
`docs/index.html`:

```html
<a class="btn primary" href="https://app.seudominio.com" target="_blank" rel="noopener">Acessar sistema</a>
```

Troque `https://app.seudominio.com` pelo dominio definitivo do backend.

## Inserir seu logo

Salve o arquivo do logo em:

```text
docs/assets/logo-hermes.png
```

O `index.html` ja esta preparado para carregar essa imagem automaticamente:

```html
<img class="logo-img" src="assets/logo-hermes.png" alt="Logo Hermes">
```

Se o arquivo ainda nao existir, a pagina mostra um fallback escrito `SEU LOGO`.

## Publicar alteracoes

Depois de ajustar a pagina ou trocar o logo:

```powershell
git add docs
git commit -m "Atualiza dashboard demo do Hermes"
git push
```

O GitHub Pages publica novamente em alguns minutos.
