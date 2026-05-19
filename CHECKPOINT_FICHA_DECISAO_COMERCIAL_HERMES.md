# Checkpoint - Ficha de decisao comercial Hermes

Data: 2026-05-19

## Objetivo

Implantar o primeiro diferencial pratico recomendado no plano de alavancagem: transformar o detalhe da oportunidade em uma ficha de decisao comercial, e nao apenas uma visualizacao basica de edital.

## O que foi implementado

No `dashboard.html`, o modal de detalhe da oportunidade passou a exibir:

1. Resumo executivo da oportunidade.
2. Tese comercial baseada em score, valor, prazo e keyword.
3. Proximos passos recomendados.
4. Sinais de risco automaticos.
5. Checklist documental inicial.
6. Fontes e rastreabilidade.
7. Botoes separados para:
   - abrir PNCP;
   - abrir origem externa.

## Regras iniciais

### Resumo executivo

Combina:

- classificacao;
- orgao;
- municipio/UF;
- valor estimado;
- janela comercial.

### Tese comercial

Varia conforme score:

- score alto: analise prioritaria;
- score medio/alto: avaliacao na semana;
- score medio: monitoramento e validacao;
- score baixo: manter no radar.

### Riscos

O Hermes sinaliza automaticamente:

- abertura ja passou;
- prazo muito curto;
- data ausente;
- valor ausente;
- link PNCP nao calculavel;
- origem externa ausente ou instavel.

### Checklist documental

Checklist base:

- edital;
- anexos;
- termo de referencia;
- habilitacao juridica;
- regularidade fiscal/trabalhista;
- qualificacao economico-financeira;
- atestados tecnicos;
- prazo para esclarecimentos.

Regras complementares por objeto:

- servicos/manutencao/limpeza: planilha de custos, encargos, equipe e local de execucao;
- TI/equipamentos: especificacoes, garantia, suporte e compatibilidade;
- saude/higiene/saneantes: registros, licencas, laudos e exigencias sanitarias.

## Valor comercial

Esse ajuste diferencia o Hermes de uma lista de oportunidades porque ajuda o usuario a responder rapidamente:

- vale olhar agora?
- por que esta oportunidade apareceu?
- qual e o proximo passo?
- qual e o risco?
- onde esta a fonte oficial?
- o que preciso validar antes de propor?

## Como testar

1. Rodar o sistema localmente:

```powershell
.\scripts\start_demo.ps1
```

2. Acessar:

```text
http://127.0.0.1:8000
```

3. Abrir uma oportunidade em `Detalhe`.

4. Verificar se aparecem:

- Resumo executivo;
- Proximos passos;
- Sinais de risco;
- Checklist documental;
- Fontes e rastreabilidade;
- botao PNCP;
- botao Origem externa.

5. Testar uma oportunidade demo e uma oportunidade PNCP real.

## Proximos refinamentos

1. Levar a ficha de decisao para o backend/API, permitindo exportar os mesmos campos.
2. Incluir os campos no Excel.
3. Criar pesos configuraveis por perfil.
4. Criar resumo por IA quando houver edital/anexo disponivel.
5. Criar campo "decisao recomendada": participar, monitorar, descartar ou pedir esclarecimento.
