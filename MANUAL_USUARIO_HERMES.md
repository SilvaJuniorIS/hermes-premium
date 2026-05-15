# Manual do usuario HERMES

## 1. O que e o HERMES

O HERMES e uma plataforma de inteligencia em licitacoes publicas. Ele coleta
oportunidades do PNCP, aplica filtros por perfil comercial, calcula score,
prioriza oportunidades com abertura futura e ajuda o time comercial a acompanhar
oportunidades ate a tomada de decisao.

Proposta central:

```text
Transformar dados publicos em oportunidades estrategicas.
```

## 2. Acesso ao sistema

1. Abra o endereco informado pelo responsavel pela demo ou servidor.
2. Na demo local, o endereco costuma ser:

```text
http://127.0.0.1:8000
```

3. Informe usuario e senha.
4. Clique em `Entrar`.

Se o acesso for por link temporario de demo, mantenha o link apenas com pessoas
autorizadas.

## 3. Tela principal

A tela inicial mostra:

- fonte de dados;
- perfil em uso;
- ultima atualizacao;
- total de registros filtrados;
- oportunidades com abertura futura;
- maior valor estimado;
- oportunidades de alta prioridade.

Por padrao, o HERMES prioriza licitacoes com **abertura futura**. Isso evita que
editais ja vencidos atrapalhem a analise comercial.

## 4. Perfis de busca

Um perfil representa um segmento comercial, por exemplo:

- limpeza e higiene;
- equipamentos de TI;
- moveis corporativos;
- medicamentos;
- manutencao predial.

Para trocar o perfil:

1. Abra a tela `Oportunidades`.
2. Use o seletor de perfil.
3. Aguarde a tabela atualizar.

## 5. Rodar uma coleta

1. Selecione o perfil desejado.
2. Clique em `Rodar coleta`.
3. Aguarde o processamento.
4. Ao final, a tabela sera atualizada com novas oportunidades.

Durante a coleta, o sistema consulta o PNCP, aplica regras do perfil, calcula o
score e grava os registros no banco local.

## 6. Entender o score

O score indica prioridade comercial.

Leitura recomendada:

- `ALTA`: avaliar primeiro.
- `MEDIA`: validar aderencia e prazo.
- `BAIXA`: manter em monitoramento ou descartar.

O score considera fatores como:

- palavras-chave encontradas;
- termos fortes;
- termos positivos ou negativos;
- valor estimado;
- aderencia ao perfil;
- janela comercial.

## 7. Filtros da tabela

Use os filtros para reduzir a lista:

- perfil;
- classificacao;
- prazo;
- status comercial;
- favoritos;
- estado;
- texto livre;
- valor minimo;
- valor maximo.

Filtro de prazo:

- `Abertura futura`: mostra oportunidades ainda acionaveis.
- `Todas as datas`: mostra futuras primeiro e vencidas depois.
- `Ja passaram`: mostra apenas oportunidades vencidas para analise historica.

## 8. Abrir detalhe da oportunidade

1. Na tabela, clique em `Detalhe`.
2. Confira:
   - score;
   - classe;
   - valor;
   - estado e municipio;
   - acao recomendada;
   - janela comercial;
   - origem;
   - objeto;
   - motivo do score;
   - dados comerciais;
   - link da fonte.

Use essa tela para decidir se a oportunidade merece acao comercial.

## 9. Acompanhamento comercial

No detalhe da oportunidade, registre:

- status comercial;
- favorito;
- anotacoes internas.

Status disponiveis:

- `Novo`;
- `Em analise`;
- `Proposta`;
- `Monitorar`;
- `Descartado`.

Exemplo de anotacao:

```text
Validar edital, cotar fornecedor e falar com representante local.
```

Depois de editar, clique em `Salvar acompanhamento`.

## 10. Exportar CSV

1. Ajuste os filtros desejados.
2. Clique em `Exportar CSV`.
3. O navegador baixara um arquivo com os registros filtrados.

Use CSV para analise rapida em planilhas ou sistemas externos.

## 11. Exportar Excel

1. Ajuste os filtros desejados.
2. Clique em `Exportar Excel`.
3. O sistema gera a planilha na pasta `output/`.
4. A mensagem no topo informa o nome do arquivo.

A planilha inclui:

- acao recomendada;
- status comercial;
- favorito;
- score;
- classificacao;
- objeto;
- estado;
- municipio;
- orgao;
- valor estimado;
- oportunidade;
- data de abertura;
- janela comercial;
- motivos do score;
- anotacoes;
- link da fonte.

## 12. Enviar planilha por e-mail

1. Ajuste os filtros desejados.
2. Clique em `Enviar por e-mail`.
3. Informe o e-mail do destinatario.
4. Confirme.

O HERMES envia:

- a planilha Excel em anexo;
- um texto explicativo sobre oportunidades;
- orientacao sobre score;
- destaques da lista;
- recomendacao comercial.

Se o envio falhar, confirme com o responsavel tecnico se as variaveis SMTP estao
configuradas.

## 13. Historico de coletas

Abra a aba `Historico` para visualizar:

- ID da execucao;
- perfil usado;
- status;
- inicio;
- fim;
- quantidade coletada;
- quantidade salva;
- observacoes.

Essa tela ajuda a demonstrar recorrencia operacional.

## 14. Agendamento

Abra a aba `Agendamento` para configurar uma coleta diaria.

1. Escolha `Ativo`.
2. Escolha o perfil.
3. Defina o horario diario.
4. Clique em `Salvar agendamento`.

Importante:

O agendamento local funciona enquanto o HERMES estiver rodando no computador ou
servidor.

## 15. Roteiro recomendado de uso diario

1. Abrir o dashboard.
2. Conferir filtro `Abertura futura`.
3. Selecionar o perfil comercial.
4. Rodar coleta ou atualizar tabela.
5. Abrir oportunidades de maior score.
6. Marcar status e favoritos.
7. Registrar anotacoes.
8. Exportar ou enviar planilha.
9. Revisar historico.
10. Confirmar agendamento.

## 16. Roteiro recomendado para apresentacao

1. Abra o HERMES.
2. Mostre o problema: muitos editais, pouco tempo e risco de perder prazo.
3. Mostre oportunidades com abertura futura.
4. Abra uma oportunidade de alta prioridade.
5. Explique score, valor, prazo, orgao e fonte.
6. Registre status comercial e anotacao.
7. Exporte Excel.
8. Envie por e-mail.
9. Mostre agendamento.
10. Convide para piloto acompanhado.

## 17. Cuidados

- Nao compartilhe senha.
- Nao exponha link temporario publicamente.
- Use senha forte em demo externa.
- Feche tuneis temporarios ao final da apresentacao.
- Revise oportunidades antes de enviar a clientes.
- Nunca prometa que o HERMES garante vitoria em licitacao.

## 18. Suporte

Em caso de problema, informe:

- horario do erro;
- tela onde aconteceu;
- perfil usado;
- filtro usado;
- mensagem exibida;
- se havia coleta em andamento.

