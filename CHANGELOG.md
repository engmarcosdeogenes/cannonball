# Changelog

Formato: o que mudou e **por quê**, não a lista de commits. Versão segue
`.claude-plugin/plugin.json`.

---

## 3.1.0

### Critério, não só peças

O acervo responde *"o que eu já tenho pra isso"*. Nunca respondeu *"isso deveria
existir assim"* — e essa lacuna aparecia na prática como seção nova sempre caindo
na mesma pilha centralizada. Não por falta de peça: por falta de critério.

**Novo: [`references/fundamentos-visuais.md`](references/fundamentos-visuais.md)**
— o vocabulário que decide antes da peça e julga depois dela. As perguntas que
substituem "está bonito?", os cinco níveis de maturidade de um design, seis níveis
de movimento, nove tipos de contraste, cinco usos da cor, psicologia de forma, seis
técnicas de geração de conceito, e sete testes executáveis.

### `kit-montar` — passo 7.9, a revisão que não é técnica

O passo 8 sempre registrou o que **quebrou**: build, hidratação, contraste
reprovado, asset morto. Faltava o outro lado — o que **não quebra e mesmo assim
falha**. Nenhum destes dá erro no console; todos custam conversão.

Sete testes, os quatro primeiros obrigatórios antes de entregar. O resultado é
roteado: falha em troca estética ou apropriabilidade é **decisão de projeto** e vai
ao usuário (pode ser que o briefing peça conformidade mesmo); falha em 3 segundos,
ladrão de atenção ou passo atrás é **execução** e se conserta antes de entregar.

O mais útil deles inverte o instinto: cubra a mensagem principal, veja o que sobrou
roubando atenção, e **reduza antes de apagar**.

### `kit-montar` — briefing e hero

- **Passo 1** ganhou as duas leituras que decidem o resto e que ninguém fazia: em
  que estado emocional a pessoa chega, e que emoção ela leva embora — esta numa
  palavra só, escrita **antes** de escolher paleta ou template. É ela que julga a
  peça depois, no lugar do gosto.
- **Passo 2.2** passou a ler o tipo de hero como **escolha de nível de movimento**.
  Quando o briefing pede sofisticação, ela mora no ritmo (impacto → demora →
  pausa), não em mais efeito.

### As outras skills

| Skill | O que entrou |
|---|---|
| `kit-cor` | passo 0 com os cinco usos da cor; **a regra do acento único** — três ênfases não são três, são zero; peso visual e valor, que permitem equilibrar sem mexer em tamanho |
| `kit-tipo` | escala como **tempo**, em três degraus (hook → secundário → finisher), com a ressalva de que o maior nem sempre é o mais importante |
| `kit-prompt` | emoção-alvo como pergunta da entrevista **e** seção `## Emotional outcome` no template; seis técnicas de geração para briefing pobre |
| `kit-buscar` | ao apresentar candidatos, dizer qual **pertence ao cliente** e qual só **pertence ao setor** |
| `kit-adaptar` | prompt de fora nunca declara intenção — acrescentar a emoção-alvo ao adaptar |

### Corrigido — exportação apagava referência de skill

Regressão introduzida na 3.0.0 e presente em todo export desde então.

Ao tornar cada skill autocontida, o `publicar.py` copiava `references/` da raiz
**por cima** da pasta de cada skill. A `kit-otimizar-3d` tem referência própria ali,
e o `patterns.md` — que carrega o código de otimização 3D inteiro — era apagado. O
`SKILL.md` seguia citando ele em nove lugares, sem nada reclamar.

Dois consertos: a cópia agora **mescla** em vez de sobrescrever, e uma conferência
de integridade **recusa a exportação** se qualquer `SKILL.md` citar arquivo que não
viajou junto.

---

## 3.0.0 — roda em Codex, Gemini CLI, Cursor e no resto

Removida a única amarra ao Claude Code: as 100 ocorrências de
`${CLAUDE_PLUGIN_ROOT}`, que em outro agente expandiam para vazio e quebravam todo
comando. No lugar, `${SKILL_DIR}` — a pasta de onde o `SKILL.md` foi lido, que é
informação que todo harness dá.

Cada pasta de skill virou **autocontida**: carrega o `scripts/` que chama, o
`references/` que cita e o `seed/`. Os instaladores de skill copiam a pasta como
unidade, então o que ficasse só na raiz não viajaria.

Junto: manifesto do Codex, listagem para a CLI do Agent Skills, `AGENTS.md` como
ponto de entrada genérico, e as menções a ferramenta de pergunta do Claude Code
reescritas de forma neutra.

---

## 2.4.0 — `kit-prompt` e `kit-adaptar` em destaque

As duas viviam numa linha de rodapé em "fora do fluxo", o que as vendia mal: são as
portas de entrada e de saída do acervo, e as duas que já dão resultado no primeiro
dia com acervo vazio.

---

## 2.3.0 — exemplo real e página do repositório

O exemplo passou a ser um caso de uso real: loja de 81 produtos e 99 páginas
montada de três peças do acervo, com os quatro bugs que a montagem encontrou —
nenhum deles com erro visível, todos gravados como armadilha nas peças de origem.

---

## 2.2.0 — ordem de uso e vínculo de pasta

- **`scripts/vincular.py`** — diz qual pasta é o seu acervo. O ponteiro vai em
  `~/.cannonball/aonde`, **fora do plugin**, porque o plugin instalado é cache e
  some na atualização.
- `perfil.py` passou a terminar com **POR ONDE SEGUIR**, adaptado ao estado do
  acervo: instalação nova manda vincular e ingerir; acervo raso manda continuar
  ingerindo; acervo de pé mostra o fluxo dos seis passos.

---

## 2.1.0 — Higgsfield e a pergunta do hero

- **`kit-montar` passo 2.2** — perguntar **que tipo de hero** antes de escrever
  qualquer código. Oito tipos catalogados, cada um com a mídia que exige e onde
  procurar no acervo.
- **Higgsfield** como quarto MCP, para gerar imagem e vídeo do hero quando o cliente
  não tem material. É o único que gasta dinheiro por chamada, então vem por último e
  **com confirmação explícita**.

---

## 2.0.0 — o motor separado dos dados

O plugin e o acervo passaram a ser coisas separadas. O plugin é o motor e vem do
git; o acervo é material do usuário, mora fora do repositório e cresce por ingestão.

**Nenhuma skill carrega censo fixo.** Todas leem o acervo na hora, então o mesmo
motor se adapta a quem tem três peças e a quem tem mil.

- `scripts/perfil.py` — retrato do acervo agora: famílias, setores, stacks,
  cobertura por função, lacunas, armadilhas e avisos de saúde
- `scripts/publicar.py` — exporta só o motor e **recusa** se material privado
  escapar
- Acervo vazio virou estado normal, não erro
- `seed/` com três peças originais, para a primeira busca devolver alguma coisa
