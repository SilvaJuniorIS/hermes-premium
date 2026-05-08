# Dashboard demo do Hermes Premium

Esta pasta contem uma versao estatica do dashboard para publicacao no GitHub Pages.

## Publicar no GitHub Pages

1. Envie a pasta `docs/` para o repositorio no GitHub.
2. No GitHub, acesse `Settings`.
3. Entre em `Pages`.
4. Em `Build and deployment`, escolha `Deploy from a branch`.
5. Selecione a branch principal e a pasta `/docs`.
6. Salve.

O GitHub vai gerar uma URL publica para a demonstracao.

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
