# Changelog

Formato: o que mudou e **por quê**, não a lista de commits. Versão segue
`.claude-plugin/plugin.json`.

---

## 3.4.0

### O 3D sabia ficar rápido e não sabia ficar certo

As nove skills tratavam cena WebGL como problema de custo. Nenhuma delas —
verificado por busca — mencionava `readPixels`, timer query ou depuração de
shader. Quando a cena renderiza, roda a 60 fps e está **errada**, o acervo não
tinha nada a dizer, e o conserto no olho é o caminho que todo mundo pega.

**Novo: §15 da `kit-otimizar-3d`, "When the scene is wrong, not slow".** O método
é o do `shader-debugging` do [vgpu](https://github.com/vercel-labs/vgpu) (MIT),
reescrito para WebGL2/GLSL: partir a conta em funções puras, renderizar os
internos num alvo 8×1 com um slot por pixel e um valor por canal, ler de volta com
`readPixels`, e diferenciar contra uma reimplementação em JS com tolerância
declarada — `2/255` para valor armazenado em 8 bits, o epsilon do algoritmo para
grandeza derivada. Mais: despejar **todo** alvo intermediário em PNG, porque num
encadeamento os números podem estar certos e a imagem errada por um passe que lê o
anexo trocado. E cinco regras de determinismo, sem as quais a evidência não é
evidência. O vgpu não virou dependência — é WebGPU/WGSL, e o acervo é three.js.

**Corrigido no §0, que estava publicado errado.** A nota dizia que no Linux a
captura sai preta "sem SwiftShader configurado". A armadilha é mais afiada: mesmo
com o software rendering funcionando, o headless captura o canvas preto — é
limitação upstream, e a saída é navegador *headed* em display virtual (Xvfb), não
outra flag de adaptador.

**Novo no §0: por que cronômetro em volta do draw não mede nada.** `performance.now()`
em volta do `drawArrays` mede a submissão; o driver grava comandos, não os executa.
Passe caro lê ~0 ms e você otimiza a coisa errada. Milissegundo de GPU de verdade
só com `EXT_disjoint_timer_query_webgl2` — e onde ele não existe (Safari), a
resposta é "não é mensurável aqui", nunca um cronômetro.

**`capturar.py` ganhou o veto de DOM.** O screenshot volta com sucesso mesmo quando
o render morreu: o Chrome grava o cartaz de "WebGL is not supported" com o mesmo
zelo com que gravaria a cena, e cartaz é colorido — medido, o cartaz vermelho passou
na variação de cor com 5 cores e brilho 68. O `--dump-dom` sai de graça na mesma
execução e o `erro_na_pagina()` veta depois do pixel. O `<noscript>` e o
`<template>` saem antes da busca, senão toda cena bem-comportada seria recusada
pelo próprio fallback que ela carrega escrito.

**O portão do `publicar.py` passou a medir o `description`.** Ele conferia os
nomes dos campos e não o tamanho — e o teto de 1024 chars da spec também é erro
duro no `skills add`. Ligado, ele achou na hora uma coisa que já estava publicada:
a `kit-montar` estava em **1095 chars desde a 3.2.0**. Na sua máquina funcionava;
quem tentasse instalar por `npx skills add` batia num erro que nós nunca veríamos.
Aparada para 995. É a mesma lição da v3.3.0: o erro que só aparece na máquina dos
outros tem que aparecer no export.

---

## 3.3.0

### O acervo deixou de ser só texto

A `kit-buscar` carregava esta frase desde a v1: *"o acervo guarda texto e código,
**não imagem** — é a lacuna estrutural dele"*. Com 5 mil peças, escolher entre duas
parecidas significava abrir arquivo.

**Novo: `scripts/capturar.py`.** Peça que roda sozinha ganha `preview.png` ao lado
da ficha — família `html`, e `animacao`/`template` com `index.html`. São 159 peças
hoje, e as 130 animações são onde mais dói, porque animação é justamente o que não
se descreve. O `indexar.py` acha o sidecar sozinho, como já fazia com
`armadilhas.json` e `tags_funcao.json`; o `painel.py` mostra a miniatura.

Usa o Chrome da máquina em headless. Sem Playwright, sem dependência nova.

**A captura é julgada antes de ser gravada.** PNG válido não prova nada: canvas que
não inicializou, página que não carregou e loader que nunca saiu geram imagem
perfeita e inútil. O script mede variação de cor e brilho e recusa com o motivo
escrito.

Duas coisas medidas nesta máquina, e não copiadas de documentação:

- **macOS captura WebGL certo** em headless (canvas de teste vermelho volta
  vermelho). No Linux sem GPU a mesma captura volta preta e nada avisa — está
  registrado na `kit-otimizar-3d`, porque lá é onde alguém concluiria "a cena
  quebrou" olhando uma imagem preta que só descreve o ambiente de captura.
- **O Chrome grava o screenshot e não sai.** Com `rAF` rodando ou requisição
  pendurada ele fica vivo indefinidamente, e um `subprocess.run(timeout=)` mata a
  captura que já estava pronta no disco. O script espera o **arquivo**, não o
  processo.

### `kit-montar` 7.9 — verificação virou laço, e olha o render

O passo 7.9 pedia sete testes sobre o que a página comunica, e o agente os aplicava
lendo o próprio JSX. Ler o código que você acabou de escrever e concluir que a
hierarquia está boa é a forma mais confiável de aprovar a própria página: você não vê
o que escreveu, vê o que quis escrever.

Agora captura primeiro, em **dois viewports no mínimo** — metade das falhas de
hierarquia só existe num dos dois, e a que sobrevive à mudança de largura é a que era
real. Havendo referência visual (print do cliente, `preview_url` do GetLayers), abre
lado a lado: "está bom?" vira "onde diverge?", que é respondível.

E fecha o laço: corrigiu, captura de novo e roda os mesmos testes, **no máximo três
voltas**. Na quarta o problema não é execução, é a decisão que gerou a página.

Padrão emprestado do [VIGA](https://github.com/Fugtemypt123/VIGA) — gerador escreve,
verificador olha o render de vários pontos de vista e devolve correção acionável.

### `allowed-tools` nas nove skills — e o campo que eu quase pus

Cada skill agora declara o que precisa: `kit-cor` pede `Read` e o Python dela;
`kit-montar` pede Write e Edit porque constrói site. Menos prompt de permissão no
meio do trabalho.

`argument-hint` e `context: fork` ficaram de fora **de propósito**. São campos do
Claude Code, e a spec do Agent Skills aceita seis: `name`, `description`, `license`,
`compatibility`, `metadata`, `allowed-tools`. Campo extra não é ignorado lá fora —
`npx skills add` e a Skills API **falham com erro duro**. O plugin promete rodar
igual em Codex, Gemini CLI e Cursor, e esses dois campos custariam exatamente isso.

`publicar.py` ganhou `conferir_frontmatter()`: recusa exportar se algum SKILL.md
sair da spec. O erro passa a acontecer aqui, e não na máquina de quem instalou.

---

## 3.2.0

### A peça que não sobrevive à própria cópia

A `kit-agendamento` já tinha derrubado um build inteiro por isso: o import relativo
estava escrito para o layout **do acervo**, não para o layout onde a peça vive depois
de copiada. Virou armadilha, e ficou por lá — como se fosse caso isolado.

Não era. `curar.py` ganhou a **seção 7, contrato de cópia**, e ela achou **165 peças**
com 333 imports que não resolvem dentro da própria pasta. Todas quebram no projeto de
destino com `Module not found`, que parece falta de pacote npm e manda você procurar
no lugar errado.

Em cerca de 85% dos casos o alvo **já está no acervo com outro id**, então o relatório
imprime o de-para (`./button -> wml-button`) e a correção é uma linha de
`precisa_componentes` no `item.json`. Mídia fica de fora de propósito: ela mora no
projeto de origem, e as seções 5 e 6 já cuidam dela.

### Os autotestes — o motor tinha 27 scripts e nenhuma verificação

`publicar.py` é fronteira de segurança: a função dele é **recusar** exportar quando
material privado escapa para o destino. Ele rodava sem teste nenhum, e falha ali é
silenciosa — peça de cliente vai para repositório público e ninguém percebe.

A rede virou a função `vazamentos(destino)`, e `--autoteste` exercita os quatro casos.
Incluindo o que um filtro ingênuo quebra: `seed/acervo/` **não** é vazamento (é a peça
de exemplo, e ela precisa viajar junto), `acervo/` na raiz é.

Dois furos apareceram no caminho: a lista proibia `cannonball.config.json`, mas o
arquivo se chama `sitekit.config.json` — nome antigo, e ele guarda o caminho absoluto
da máquina. E `_podados/` também não estava coberto. Os dois entraram.

`curar.py --autoteste` faz o mesmo pelo detector de import: monta uma peça falsa e
verifica os cinco casos (resolve, sumiu, declarado, mídia, pacote npm).

### A cobertura de armadilha, dita como porcentagem

`perfil.py` imprimia `85 armadilhas em 35 peças`. Soa saudável — e soa igual num
acervo de 50 peças e num de 5000. Em porcentagem soa como o que é: **0,7%**.

As outras 99% são catálogo comum, e catálogo comum se acha em qualquer registry. A
armadilha é a única coisa aqui que nenhum catálogo externo tem: catálogo descreve o
que a peça faz, só o seu acervo sabe onde ela já te derrubou.

### `kit-montar` — o portão do passo 8

O passo 8 é o único do fluxo **sem resultado visível**: ninguém percebe se foi pulado,
e por isso era pulado. Agora exige uma de duas saídas, dita em voz alta ao usuário:
*"registrei N armadilhas"* (com o script rodado), ou *"nada quebrou"* **seguido do que
foi conferido** — build de produção, contraste, mobile real, `prefers-reduced-motion`,
asset externo respondendo.

Sem essa lista não é "nada quebrou", é "não olhei", e as duas se pareciam demais para
continuarem com o mesmo nome. Não existe terceira saída.

### `kit-ingerir` — o que separa ficha forte de ficha fraca

`curar.py` sempre soube dizer que uma ficha é **curta**. Nunca soube dizer que ela é
**vaga**, que é o defeito que realmente some da busca. Quatro testes novos, aplicados
na hora de escrever:

1. **O mecanismo numa frase** — a coisa que, removida, faz o efeito parar. Sem ela
   você tem um visual, não uma peça, e vai guardar outra variação do mesmo.
2. **Três pilhas** — mecanismo, encenação, incidental. Guarde só a primeira. Encenação
   descrita como mecanismo produz tag que casa com tudo e não seleciona nada.
3. **Regra ancorada na falha que evita** — "varie a rotação pra ficar natural" é
   decoração; "90° fora de fase, senão lê como bug de easing" é verificável. É o
   mesmo material de `armadilhas.py`, escrito **antes** de tropeçar.
4. **Números, não adjetivos** — "sutil" é inutilizável, `0.3–0.5` é ponto de partida.

Vem do [`web-technique-to-skill`](https://github.com/MengTo/skills) do Meng To (MIT),
traduzido para o vocabulário do acervo.

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
