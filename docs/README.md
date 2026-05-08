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

No arquivo `index.html`, procure por:

```html
<div class="logo-slot">SEU<br>LOGO</div>
```

Troque por uma imagem, por exemplo:

```html
<img class="logo-img" src="assets/logo.png" alt="Logo da empresa">
```

Depois crie a pasta `docs/assets/` e coloque o arquivo `logo.png` dentro dela.

Se usar imagem, adicione este CSS:

```css
.logo-img {
    width: 54px;
    height: 54px;
    object-fit: contain;
    border-radius: 8px;
    background: #ffffff;
}
```

