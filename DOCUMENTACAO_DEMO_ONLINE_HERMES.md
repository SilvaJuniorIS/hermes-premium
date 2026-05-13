# Documentacao da demo online do Hermes Premium

Data de referencia: 11/05/2026

Este documento descreve o processo completo para publicar a vitrine estatica do
Hermes Premium e expor temporariamente a versao real do sistema para uma
demonstracao acompanhada.

## 1. Visao geral

O Hermes Premium possui duas camadas diferentes:

1. Vitrine publica estatica:
   - pasta `docs/`;
   - arquivo principal `docs/index.html`;
   - logo em `docs/assets/logo-hermes.png`;
   - publicacao via GitHub Pages;
   - dados ficticios para demonstracao comercial.

2. Sistema real:
   - FastAPI em `api.py`;
   - dashboard real em `dashboard.html`;
   - banco SQLite em `data/hermes.sqlite3`;
   - login com cookie;
   - coleta no PNCP;
   - scoring e rotinas Python;
   - execucao local ou em servidor backend.

GitHub Pages nao executa Python, FastAPI ou SQLite. Por isso, ele deve ser usado
como vitrine publica, enquanto o sistema real deve rodar localmente, em servidor
proprio ou em plataforma de hospedagem backend.

## 1.1. Direcao de marca

A marca deve ser apresentada como:

```text
HERMES
Inteligencia em Licitacoes Publicas
```

Posicionamento:

```text
Assistente estrategico de inteligencia licitatoria.
```

Proposito:

```text
Transformar dados publicos em oportunidades estrategicas.
```

Paleta aplicada:

- Azul Profundo: `#0A2342`
- Laranja Hermes: `#F7931E`
- Branco Gelo: `#F5F7FA`
- Cinza Grafite: `#2D3748`

Referencia completa:

```text
IDENTIDADE_MARCA_HERMES.md
```

## 2. Arquivos principais

- `docs/index.html`: pagina estatica para GitHub Pages.
- `docs/README.md`: instrucoes da vitrine estatica.
- `docs/assets/logo-hermes.png`: logo exibido na vitrine.
- `api.py`: backend FastAPI do Hermes real.
- `dashboard.html`: dashboard operacional protegido por login.
- `data/hermes.sqlite3`: banco local do sistema.
- `scripts/start_demo.ps1`: inicializador da demo operacional.
- `INICIAR_DEMO_HERMES.bat`: atalho Windows para iniciar a demo.
- `DEMO_HERMES.md`: roteiro curto de apresentacao.
- `IMPLANTACAO_ONLINE_HERMES.md`: orientacao de implantacao online.

## 3. Publicar a vitrine no GitHub Pages

### 3.1. Confirmar arquivos da vitrine

Verifique se existem:

```text
docs/index.html
docs/README.md
docs/assets/logo-hermes.png
docs/.nojekyll
```

### 3.2. Enviar alteracoes para o GitHub

Depois de revisar os arquivos:

```powershell
git status
git add .
git commit -m "Atualiza vitrine online do Hermes"
git push
```

### 3.3. Ativar GitHub Pages

No GitHub:

1. Abra o repositorio.
2. Acesse `Settings`.
3. Entre em `Pages`.
4. Em `Build and deployment`, selecione `Deploy from a branch`.
5. Escolha a branch principal.
6. Escolha a pasta `/docs`.
7. Salve.

O GitHub Pages vai gerar uma URL publica em alguns minutos.

### 3.4. Link para o sistema real

O botao principal da vitrine fica em `docs/index.html`.

Enquanto nao existir servidor definitivo, o placeholder e:

```html
<a class="btn primary" href="https://app.seudominio.com" target="_blank" rel="noopener">Acessar sistema</a>
```

Quando houver dominio real, trocar para algo como:

```html
<a class="btn primary" href="https://app.hermespremium.com.br" target="_blank" rel="noopener">Acessar sistema</a>
```

Para demonstracoes temporarias, tambem e possivel trocar esse link pela URL do
tunel Cloudflare, mas apenas durante uma apresentacao controlada.

## 4. Iniciar a demo real local

### 4.1. Abrir PowerShell na pasta do projeto

```powershell
cd C:\Projeto_Hermes_Premium
```

### 4.2. Definir usuario e senha

Use uma senha forte e propria para a apresentacao:

```powershell
$env:HERMES_ADMIN_USER="demo"
$env:HERMES_ADMIN_PASSWORD="troque-por-uma-senha-forte"
```

### 4.3. Iniciar o Hermes

```powershell
.\scripts\start_demo.ps1
```

O terminal deve mostrar algo parecido com:

```text
Hermes Premium - demo operacional
URL:      http://127.0.0.1:8000
Usuario: demo
Senha:   ********
```

O servidor deve continuar aberto com Uvicorn rodando.

### 4.4. Acessar localmente

Abra no navegador:

```text
http://127.0.0.1:8000
```

Entre com:

```text
Usuario: demo
Senha: senha definida no PowerShell
```

## 5. Publicar temporariamente com Cloudflare Tunnel

Use este modo para demonstracao acompanhada. Ele cria uma URL HTTPS temporaria
apontando para o Hermes local.

### 5.1. Manter o Hermes aberto

Nao feche a janela em que aparece:

```text
Uvicorn running on http://127.0.0.1:8000
```

Essa mensagem nao e comando. Ela apenas confirma que o backend esta rodando.

### 5.2. Abrir uma segunda janela do PowerShell

Na segunda janela:

```powershell
cd C:\Projeto_Hermes_Premium
```

### 5.3. Baixar o Cloudflare Tunnel

Se `cloudflared` nao estiver instalado, baixe o executavel na pasta do projeto:

```powershell
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile ".\cloudflared.exe"
```

### 5.4. Iniciar o tunel

```powershell
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
```

Aguarde aparecer uma mensagem como:

```text
Your quick Tunnel has been created!
https://alguma-coisa.trycloudflare.com
```

Essa URL HTTPS e o acesso publico temporario da demo real.

### 5.5. Testar o acesso publico

Abra a URL `trycloudflare.com` no navegador.

Valide:

1. a tela de login aparece;
2. o login funciona;
3. o dashboard carrega;
4. os filtros respondem;
5. detalhes e exportacoes abrem normalmente.

### 5.6. Encerrar o tunel

No final da apresentacao, pressione `Ctrl+C` na janela do `cloudflared`.

Depois, se quiser parar o Hermes local, pressione `Ctrl+C` tambem na janela do
Uvicorn.

## 6. Alternativa com ngrok

O ngrok tambem pode ser usado, mas atualmente exige conta verificada e token.

### 6.1. Configurar token

1. Criar conta em `https://dashboard.ngrok.com/signup`.
2. Obter token em `https://dashboard.ngrok.com/get-started/your-authtoken`.
3. Rodar:

```powershell
.\ngrok.exe config add-authtoken SEU_TOKEN_AQUI
```

### 6.2. Abrir tunel

```powershell
.\ngrok.exe http 8000
```

Copie a URL HTTPS exibida no campo `Forwarding`.

## 7. Roteiro de apresentacao

Antes da reuniao:

1. Iniciar o Hermes local.
2. Iniciar o Cloudflare Tunnel.
3. Testar login pela URL publica.
4. Conferir se existem oportunidades recentes.
5. Separar 3 a 5 oportunidades fortes.
6. Testar exportacao CSV ou Excel.

Durante a reuniao:

1. Abrir a URL publica.
2. Fazer login.
3. Mostrar indicadores do dashboard.
4. Filtrar por perfil, estado, classificacao e texto.
5. Abrir uma oportunidade de alta prioridade.
6. Mostrar acao recomendada, janela comercial, origem e motivos do score.
7. Registrar status comercial, favorito e anotacoes internas.
8. Mostrar objeto, orgao, municipio, valor estimado, score e link da fonte.
9. Mostrar que o filtro padrao e `Abertura futura`.
10. Exportar dados.
11. Enviar a planilha por e-mail para demonstrar continuidade comercial.
12. Mostrar historico de coletas.
13. Mostrar a opcao Coleta geral no seletor de perfil (todos os perfis em sequencia).
14. Mostrar agendamento como rotina automatizada.

Depois da reuniao:

1. Fechar o tunel.
2. Parar o servidor local se nao for mais usar.
3. Trocar a senha antes da proxima demo.
4. Registrar feedbacks do cliente ou socio.

## 8. Enviar planilha por e-mail

O dashboard operacional possui o botao `Enviar por e-mail` na tela de
oportunidades.

Fluxo:

1. O usuario ajusta os filtros da tabela.
2. Clica em `Enviar por e-mail`.
3. O sistema solicita o e-mail do destinatario.
4. A API gera uma planilha Excel com os filtros atuais.
5. O Hermes envia o anexo usando `src/notifier.py`.
6. O corpo do e-mail explica o total de oportunidades, filtros usados, leitura
   do score, destaques e recomendacao comercial.

Endpoint usado:

```text
POST /licitacoes/export/email
```

Configuracao SMTP:

O envio reaproveita a configuracao existente em `src/notifier.py`. Para
ambientes de demo ou producao, prefira variaveis de ambiente:

```powershell
$env:HERMES_SMTP_HOST="smtp.gmail.com"
$env:HERMES_SMTP_PORT="465"
$env:HERMES_SMTP_USER="seu-email@gmail.com"
$env:HERMES_SMTP_PASSWORD="sua-senha-de-app"
$env:HERMES_EMAIL_FROM="seu-email@gmail.com"
```

## 9. Acompanhamento comercial

O detalhe da oportunidade possui uma area de acompanhamento comercial.

Campos disponiveis:

- status comercial: `Novo`, `Em analise`, `Proposta`, `Monitorar` ou `Descartado`;
- favorito;
- anotacoes internas.

Uso recomendado na demo:

1. Abra uma oportunidade de alta prioridade.
2. Explique os motivos do score.
3. Marque como `Em analise` ou `Proposta`.
4. Ative favorito para destacar a oportunidade.
5. Escreva uma anotacao curta, como `validar edital e cotar fornecedor`.
6. Salve o acompanhamento.
7. Mostre que a tabela passa a refletir status e favorito.
8. Use filtros por status ou favoritos.

Esses campos entram nas exportacoes CSV/Excel e ajudam a demonstrar que o
Hermes apoia a rotina comercial depois da coleta.

## 10. Priorizacao por data de abertura

O dashboard prioriza oportunidades com data de abertura futura.

Comportamento:

- a tela usa `Abertura futura` como filtro padrao;
- o backend tambem recebe `prazo=futuras` por padrao na API de listagem;
- quando o usuario seleciona `Todas as datas`, oportunidades futuras aparecem
  antes das vencidas;
- oportunidades vencidas continuam disponiveis no filtro `Ja passaram`, mas
  deixam de competir com oportunidades acionaveis;
- CSV, Excel e envio por e-mail respeitam o filtro de prazo selecionado;
- as exportacoes incluem a coluna `janela_comercial` para indicar urgencia ou
  se a abertura ja passou.

## 11. Cuidados de seguranca

- Nao usar a senha padrao em tunel publico.
- Nao divulgar a URL do tunel fora da apresentacao.
- Fechar o tunel ao terminar.
- Usar base de demonstracao sem dados sensiveis de clientes.
- Trocar senha entre apresentacoes.
- Evitar deixar o computador desbloqueado durante a demo.
- Nao depender de tunel temporario para producao.
- Nao versionar senhas reais de SMTP em novos arquivos.

## 12. Caminho para piloto

Quando houver cliente piloto, migrar do tunel temporario para hospedagem real:

1. Contratar VPS ou plataforma backend.
2. Instalar Python 3.10+.
3. Copiar o projeto sem `venv`, `.git`, caches e backups antigos.
4. Criar ambiente virtual.
5. Instalar `requirements.txt`.
6. Definir `HERMES_ADMIN_USER` e `HERMES_ADMIN_PASSWORD`.
7. Rodar FastAPI como servico permanente.
8. Colocar HTTPS na frente com Nginx, Caddy, IIS ou proxy da plataforma.
9. Configurar backup automatico de `data/hermes.sqlite3`.
10. Atualizar o botao da vitrine para o dominio real.

## 13. Melhorias recomendadas

### Seguranca

- Ocultar a senha no terminal do `start_demo.ps1`.
- Limitar tentativas de login.
- Criar expiracao de sessao mais clara.
- Adicionar tela de troca de senha.
- Registrar logins e tentativas negadas.

### Produto

- Criar status comercial por oportunidade.
- Permitir favoritos.
- Permitir anotacoes internas.
- Criar funil: novo, em analise, proposta, descartado.
- Melhorar pagina de detalhe da licitacao.

### Demo comercial

- Criar botao para carregar base demo.
- Separar base demo de base real.
- Selecionar oportunidades fortes antes de cada apresentacao.
- Criar roteiro de apresentacao por segmento.

### Operacao

- Melhorar tela de agendamento.
- Exibir proxima coleta.
- Exibir ultima coleta e erros recentes.
- Adicionar alertas por e-mail ou WhatsApp.
- Criar backup automatico do SQLite.

### Producao

- Hospedar backend com dominio fixo.
- Usar HTTPS obrigatorio.
- Configurar monitoramento simples.
- Criar processo de deploy via Git.
- Planejar migracao futura de SQLite para PostgreSQL se houver multiplos usuarios.
