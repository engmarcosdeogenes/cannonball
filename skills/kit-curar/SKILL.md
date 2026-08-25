---
name: kit-curar
description: >
  Verifica a saúde do acervo pessoal de sites — duplicatas, arquivos vazios, fichas
  mal escritas que a busca nunca vai encontrar, dependências exigidas e assets
  externos que já expiraram. Use quando o usuário perguntar o estado do acervo,
  reclamar que a busca não acha o que deveria, quiser limpar ou revisar o que está
  guardado, antes de uma leva grande de ingestão, ou invocar /kit-curar.
---

# kit-curar — saúde do acervo

## Antes de qualquer comando: resolva o `SKILL_DIR`

Todo comando abaixo roda um script que viaja junto desta skill, em
`SKILL_DIR/scripts/`. Defina `SKILL_DIR` como o **caminho absoluto da pasta que
contém ESTE SKILL.md que você acabou de ler** — o seu harness informou esse caminho
no resultado da leitura. Funciona em qualquer hospedeiro, sem depender de variável
de ambiente de nenhum agente específico:

```
~/.claude/plugins/cache/cannonball/cannonball/<v>/skills/<nome>/SKILL.md
~/.codex/skills/<nome>/SKILL.md
~/.gemini/skills/<nome>/SKILL.md
~/.agents/skills/<nome>/SKILL.md
```

Em todos, `SKILL_DIR` é a pasta do `SKILL.md`, e `SKILL_DIR/scripts/` está ao lado.

```bash
python "${SKILL_DIR}/scripts/perfil.py"                  # o retrato de agora
python "${SKILL_DIR}/scripts/curar.py"
python "${SKILL_DIR}/scripts/curar.py" --assets --n 20   # testa URLs (usa rede)
```

O `perfil.py` vem primeiro porque dá a escala: ele reporta o total, as lacunas de
função e três contadores que dizem onde a curadoria vale mais — peças sem
contraindicação escrita, peças com asset já morto, peças com fonte não entregável.

**Acervo vazio não precisa de curadoria.** Se o perfil disser que não há nada,
mande o usuário para `/kit-ingerir` em vez de rodar o relatório.

O relatório cobre cinco frentes. O que fazer com cada uma:

## 1. Duplicatas e vazios

Duplicata exata significa o mesmo conteúdo em dois ids — os dois competem na busca e
nenhum ganha. Mantenha o de melhor ficha, apague o outro.

Arquivo vazio é lixo puro. Confirme com o usuário e remova a pasta.

## 2. Fichas fracas — o problema mais importante

São itens com `quando_usar` curto demais, sem contraindicação, ou com menos de três
tags. **Estes itens existem no acervo mas são invisíveis para a busca.** É a causa
número um de "eu sei que tenho isso mas não acho".

Corrigir vale mais que ingerir coisa nova. Para cada item fraco: leia o arquivo,
reescreva `quando_usar` e `nao_usar_quando` com critério concreto, e edite o
`meta.yaml` (ou `item.json`) da pasta. Depois rode `indexar.py`.

## 3. Rascunhos e descartes

`rascunho` = incompleto, use com ressalva. `descartar` = candidato a remoção.

Decida com o usuário: completar a ficha, ou apagar. Deixar apodrecendo no meio-termo
é o pior dos casos, porque continua aparecendo em busca sem servir para nada.

## 4. Dependências

A lista mostra o que os projetos vão precisar ter instalado. Repare especialmente nas
que começam com `@/` — **não são pacotes npm, são arquivos que precisam existir no
projeto**. `@/lib/utils` (a função `cn`) é exigida por boa parte deles; sem ela, o
import quebra.

## 5. Assets externos

Boa parte do acervo aponta para vídeos e imagens em `cloudfront.net`, `figma.site` e
`higgs.ai` — buckets temporários que expiram. Uma peça cujo asset caiu ainda gera
código válido, mas a página nasce com mídia quebrada.

`--assets` testa as URLs de verdade. O que voltar `MORTO` precisa de substituição
antes de ser usado em cliente. Registre isso no `nao_usar_quando` da peça para não
descobrir de novo no próximo projeto.

## Ordem recomendada

Vazios e duplicatas primeiro (rápido e definitivo), fichas fracas depois (é o que
mais melhora a busca), assets por último (depende de rede e muda com o tempo).

Sempre rode `indexar.py` depois de qualquer edição de ficha.
