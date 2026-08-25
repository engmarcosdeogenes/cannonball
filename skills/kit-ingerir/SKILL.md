---
name: kit-ingerir
description: >
  Alimenta o acervo pessoal de sites com material novo — prompts, componentes,
  efeitos, design systems, projetos inteiros ou catálogos servidos por MCP —
  classificando por conteúdo e escrevendo a ficha que torna a peça encontrável
  depois. Aceita arquivo, texto colado, pasta de projeto, registro shadcn ou
  servidor MCP. Use quando o usuário disser "guarda isso", "coloquei mais
  arquivos na pasta", "adicionei uns códigos", "conectei um MCP",
  "adiciona no acervo", "salva esse componente", "quero indexar esse projeto",
  mostrar um código ou prompt que queira reaproveitar, ou invocar /kit-ingerir.
  Use também, proativamente, quando ele criar algo bom durante um projeto e valer
  a pena guardar para reutilizar.
---

# kit-ingerir — alimentar o acervo

## Antes da primeira ingestão: onde isso vai morar?

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/vincular.py"
```

Se a resposta for *"quem manda: o padrão, porque nada foi vinculado"*, **pergunte ao
usuário onde ele quer o acervo antes de gravar a primeira peça.** O padrão é
`~/.cannonball`, que funciona mas quase nunca é o que ele quer a longo prazo — e mover
depois é trabalho manual, com o índice para regerar.

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/vincular.py" --para "<pasta>"
```

Sugira uma pasta versionada num repositório **privado**: o acervo guarda material de
terceiros e de clientes, e não é dele para redistribuir.

Pergunte uma vez por máquina, não a cada ingestão.

Um item mal descrito é um item perdido. O acervo já provou isso: os nomes originais
eram `bend`, `peel`, `vex`, `oyla`, `skiper52` — nenhum diz o que faz. O valor não
está em guardar o arquivo, está em escrever **quando usar** e **quando não usar**.

## Primeiro: analise, não pergunte

O script detecta sozinho família, stack, dependências, fontes, assets externos e
marca. Rode antes de perguntar qualquer coisa ao usuário:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir.py" <arquivo> --analisar
```

Ele classifica **por conteúdo, não por extensão** — isso importa: 30 dos arquivos
originais do acervo eram `.md` contendo TSX puro. Confie no que ele detectou.

## Depois: escreva a ficha

Você preenche o que a máquina não infere. Proponha tudo você mesmo lendo o arquivo,
e pergunte ao usuário só o que não conseguir deduzir com segurança:

| Campo | O que é |
|---|---|
| `--id` | slug curto e descritivo. **Não** use o nome original se for opaco |
| `--titulo` | frase que identifica a peça de relance |
| `--resumo` | uma linha do que ela faz |
| `--setor` | vertical, ou `generico` se serve para qualquer um |
| `--estrutura` | `hero` `lp-completa` `scroll-cinematica` `signup` `404` `efeito-wrapper` `componente-ui` `efeito-objeto-3d` |
| `--tags` | características visuais, separadas por vírgula |
| `--quando-usar` | **o critério de escolha.** Concreto: setor, público, condição |
| `--nao-usar-quando` | **a contraindicação.** É o que evita entregar a peça errada |
| `--qualidade` | `favorito` `producao` `rascunho` |

Use `--listar setor` e `--listar tag` do `buscar.py` para reaproveitar o vocabulário
que já existe em vez de inventar termos novos — vocabulário fragmentado quebra a busca.

Duas regras para o par `quando_usar` / `nao_usar_quando`:

- **Concreto vence genérico.** "Clínica odontológica que quer destacar um
  procedimento específico" serve. "Sites modernos e bonitos" não serve para nada.
- **A contraindicação precisa ser real.** "Mobile — depende de cursor", "Marca que
  vende estabilidade e confiança", "Sem GLB decente o resultado é pobre". Se não
  houver restrição verdadeira, procure melhor: quase toda peça tem uma.

Depois:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir.py" <arquivo> --id ... --titulo ... \
  --setor ... --estrutura ... --tags ... --quando-usar "..." --nao-usar-quando "..."
python "${CLAUDE_PLUGIN_ROOT}/scripts/indexar.py"
```

O `indexar.py` no fim é obrigatório — sem ele a peça existe no disco mas não aparece
na busca.

## Catálogo servido por MCP — indexe a ficha, não o código

Quando a fonte é um servidor MCP que **gera** o componente sob medida (stack,
styling, TypeScript, presets, tweaks), copiar um snapshot joga fora exatamente o
que o MCP tem de melhor, e o snapshot envelhece. Indexe só a ficha, com ponteiro:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_mcp.py" \
  --catalogo <catalogo>.json --fonte originkit --analisar

python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_mcp.py" \
  --catalogo <catalogo>.json --fonte originkit --prefixo ok- \
  --julgamentos <julgamentos>.json
```

O `--julgamentos` é um mapa `{nome_ou_categoria: quando_usar}`. O resto o script
deriva do catálogo, incluindo a contraindicação — e ela é derivada de **sinal real**
(tags, dependências, descrição), não de texto genérico: `three`/`ogl` vira aviso de
GPU, `cursor`/`hover` vira aviso de mobile, `canvas` vira aviso de CPU e bateria.

Use isso quando o código é gerado sob demanda. Quando o registro serve um arquivo
final e estável, prefira `ingerir_registro.py` — ali vale guardar.

## Componente de um registro shadcn

Se o material vem de um registro (smoothui, shadcn/ui, ou qualquer `@namespace`),
**busque do registro em vez de rodar `shadcn add` num projeto descartável.** O JSON
do registro já traz título, descrição oficial, dependências npm e o grafo de
dependências entre componentes — nada precisa ser inferido do código, e você não
precisa de projeto nem de `node_modules`.

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_registro.py" \
  --url https://smoothui.dev/r/siri-orb.json --analisar

python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_registro.py" --arquivo cache/siri-orb.json \
  --id sui-siri-orb --registro smoothui --estrutura componente-ai \
  --quando-usar "..." --nao-usar-quando "..."
```

O campo `registryDependencies` do JSON vira `precisa_componentes` no índice, e a
busca imprime isso como `PRECISA JUNTO:`. Preserve — é o que evita colar um
componente que quebra por falta do que ele importa.

Prefixe os ids com a sigla do registro (`sui-` para smoothui) para não colidir.

## Design system no formato "Style Reference"

Se o arquivo começa com `# <Nome> — Style Reference` e tem `**Theme:**`, use o parser
dedicado. Esse formato é rígido o bastante para que quase toda a ficha saia por
extração — nome, tagline, tema, paleta completa, fontes e marcas similares:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_design.py" <arquivo> --analisar
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_design.py" <arquivo> --id ds-<nome> \
  --setor <setor> --quando-usar "..." --nao-usar-quando "..." --tags "..."
```

Você só escreve o julgamento. Para o `quando_usar`, descreva o **caráter visual** e
o tipo de marca que ele serve — é assim que a busca vai ser feita depois. Para o
`nao_usar_quando`, procure a restrição técnica real: peso 100 que quebra em tamanho
pequeno, tipo a 13px sobre preto, sistema de três cores sem espaço para estados
semânticos, dependência de fotografia cara.

Prefixe os ids com `ds-` para não colidir com outras famílias.

Para uma pasta inteira, gere primeiro o digest e escreva as fichas a partir dele:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_design.py" <pasta> --digest
```

## Projeto inteiro é outra unidade — use o outro script

Uma animação de scroll vive espalhada entre `script.js` + `styles.css` + `index.html`.
Separar em arquivos destrói a peça. Quando a unidade é a **pasta**, use:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_projeto.py" <pasta> --analisar
python "${CLAUDE_PLUGIN_ROOT}/scripts/ingerir_projeto.py" <pasta> --id ... \
  --familia template --titulo ... --estrutura template-multipagina \
  --quando-usar "..." --nao-usar-quando "..."
```

Ele detecta rotas, componentes, dependências (lendo `package.json`, bem mais confiável
que regex) e técnicas de animação. Copia **só o código** para o acervo e referencia o
projeto original para os assets — num template típico, 99% do peso é imagem e vídeo,
que não cabem no git e são trocados por material do cliente de qualquer forma.

Duas famílias: `template` (site completo e rodável) e `animacao` (técnica isolada).
Estruturas: `template-multipagina`, `template-single-page`, `animacao-scroll`,
`animacao-reveal`, `animacao-hover`, `transicao-pagina`, `componente-animado`.

Para muitos projetos de uma vez, escreva um arquivo de lote e rode:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/lote.py" <lote>.json --simular
python "${CLAUDE_PLUGIN_ROOT}/scripts/lote.py" <lote>.json
```

Sempre `--simular` antes: ele confere se todos os caminhos resolvem sem gravar nada.

## Varrer um projeto para extrair peças soltas

Diferente do acima: aqui você quer **componentes individuais** de dentro de um projeto,
não o projeto como unidade. Quando o usuário apontar uma pasta de projeto já
entregue:

1. Localize os candidatos: componentes de seção (`Hero`, `Pricing`, `Footer`),
   efeitos, páginas. Ignore infraestrutura — configs, utils, tipos, testes.
2. **Apresente a lista antes de ingerir.** "Achei 7 candidatos: hero, nav, 3 seções,
   pricing, footer. Ingiro todos?" Deixe ele cortar.
3. Ingira em lote, um comando por peça.
4. Rode `indexar.py` uma vez no fim, não a cada peça.

Não ingira componente que só faz sentido dentro daquele projeto — algo amarrado a um
schema de dados específico não é reutilizável, é ruído no acervo.

## Depois de uma leva grande, audite a função

Descrever o que a peça **parece** é fácil; descrever o que ela **faz** costuma
escapar. Um template com carrinho e catálogo pode ficar invisível para quem busca
"grade de produtos" só porque a ficha fala de tipografia.

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/tags_funcao.py" --auditar
python "${CLAUDE_PLUGIN_ROOT}/scripts/tags_funcao.py" --lote _tags_funcao_propostas.json
python "${CLAUDE_PLUGIN_ROOT}/scripts/indexar.py"
```

Ele lê o **código**, não a ficha, e propõe etiquetas de função. Design system ganha
prefixo `spec-` porque especifica em vez de implementar — a distinção evita que
`--tag catalogo` devolva referência de estilo junto com código que roda.

## O cliente mandou o site dele, não um arquivo

Estes scripts só ingerem **arquivo ou pasta**. Quando a fonte é o site atual do
cliente, um print ou uma referência visual, não há caminho aqui — e é o caso mais
comum em projeto real.

A skill **design-dna** (`npx skills add zanwei/design-dna`) fecha isso: extrai de
imagem ou URL um JSON em três dimensões — tokens mensuráveis, estilo qualitativo
e **efeitos visuais** (WebGL, partícula, shader, scroll). As duas primeiras mapeiam
quase campo a campo no que um design system daqui já guarda; a terceira o acervo
não tem, e vale acrescentar ao `item.json` em vez de descartar.

```
site/print do cliente  ->  design-dna  ->  ficha ds-<cliente>  ->  ingerir_design.py
```

Isso corrige o viés que a `kit-cor` mede: design system extraído de marca famosa
converge para neutro e azul, e um acervo feito só disso empurra todo cliente para o
mesmo lugar. Ingerir a identidade dos **seus** clientes ataca o problema na raiz — e
é o tipo de peça que só o seu acervo pode ter.

Peça a ele os **tokens**, não a página — o padrão do design-dna é gerar HTML
autocontido, que não serve ao fluxo Next + GSAP.

## Antes de gravar, verifique se já existe

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/buscar.py" "<descrição da peça>"
```

Se já existe algo equivalente, o certo é melhorar a ficha do que existe, não criar um
gêmeo. Dois itens quase iguais dividem a relevância e nenhum dos dois ganha a busca.

## Texto colado

Se o usuário colar código ou prompt direto no chat, grave num arquivo primeiro
(pode ser no diretório de scratch) e ingira a partir dele. O script trabalha sobre
arquivo, e o original fica guardado em `_fonte/`.

## O que muda a cada peça guardada

Vale dizer isso ao usuário, porque não é óbvio e é a razão de a ingestão importar.
**Nenhuma skill do cannonball carrega uma lista fixa do que existe.** Todas leem o
acervo na hora, então ingerir não é só arquivar: é ensinar o conjunto inteiro.

Depois de `indexar.py`, sem você fazer mais nada:

- a **`kit-buscar`** passa a encontrar a peça, e a `perfil.py` a conta na família,
  no setor e na stack dela;
- se a peça implementa uma função que estava na lista de **lacunas**, a lacuna
  fecha — e a `kit-montar` para de construir aquilo do zero;
- se é design system, ela entra no viés que a **`kit-cor`** mede: ingerir a
  identidade dos seus clientes desloca o acervo para longe do neutro-e-azul de
  marca famosa;
- as fontes que ela nomeia entram na classificação de licença da **`kit-tipo`**;
- e toda **armadilha** que você registrar nela (`scripts/armadilhas.py`) passa a
  ser impressa na busca, para você e para qualquer projeto futuro.

Por isso a ficha vale mais que o arquivo, e por isso `quando_usar` e
`nao_usar_quando` escritos com preguiça envenenam o conjunto: a peça continua lá,
mas invisível — e invisível é o mesmo que não ter.
