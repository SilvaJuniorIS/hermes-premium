# Site estatico do Hermes Premium (GitHub Pages)

Esta pasta publica **paginas estaticas** no GitHub Pages. O sistema completo
(FastAPI, SQLite, login, PNCP) roda em servidor separado ou localmente.

## Estrutura das paginas

| Arquivo | Funcao |
|---------|--------|
| `index.html` | **Apresentacao comercial**: dossiê por abas, carrossel com ilustrações SVG, proposta de valor, oferta e CTAs. |
| `assets/hermes-comercial/` | Ilustrações vetoriais 16:9 usadas no carrossel (substituíveis por capturas reais). |
| `vitrine.html` | **Demonstracao interativa** (layout tipo dashboard) com dados ficticios no navegador. |
| `atlasnex.html` | Pagina da **AtlasNex** (holding): ecossistema e links para Hermes. |

A URL raiz do Pages (`.../`) abre a **apresentacao**. A demo interativa fica em
`.../vitrine.html`.

## AtlasNex (empresa-mae)

```text
docs/atlasnex.html
```

Para apontar o botao do dashboard Hermes para tunel ou ambiente publico:

```text
atlasnex.html?hermes_dashboard=https://seu-subdominio.trycloudflare.com
```

## Link para o sistema real

Na **vitrine interativa** (`vitrine.html`), o botao **Acessar o Site** aponta para o
ambiente publicado via Cloudflare Tunnel (URL atual no HTML). Quando o túnel mudar,
atualize o `href` em `vitrine.html` e em `docs/index.html` (apresentacao).

## Logo Hermes

Arquivo usado na apresentacao, na vitrine e no dashboard operacional:

```text
docs/assets/hermes-product-logo.png
```

Servido em producao local como `/assets/hermes-product-logo.png` (pasta
`docs/assets` montada na API).

## Publicar no GitHub Pages

1. Envie a pasta `docs/` para o repositorio no GitHub.
2. **Settings** → **Pages** → **Deploy from a branch** → branch principal, pasta `/docs`.

## Publicar alteracoes

```powershell
git add docs
git commit -m "Atualiza site estatico do Hermes"
git push
```

O GitHub Pages republica em alguns minutos.
