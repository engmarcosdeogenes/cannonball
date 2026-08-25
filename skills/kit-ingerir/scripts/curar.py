#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saude do acervo: duplicatas, arquivos vazios, fichas fracas, assets que ja caíram.

    python scripts/curar.py                # relatorio completo
    python scripts/curar.py --assets       # testa as URLs externas (rede, demora)
    python scripts/curar.py --assets --n 20
"""

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caminhos import ACERVO, RAIZ, exigir_indice, saida_utf8  # noqa: E402

saida_utf8()

GENERICO = (
    "Nenhuma restrição registrada.",
    "", "-", "n/a", "nao registrado", "não registrado",
)


def carregar():
    return exigir_indice()


def secao(titulo):
    print(f"\n{'=' * 62}\n{titulo}\n{'=' * 62}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--assets", action="store_true", help="testa URLs externas (usa rede)")
    p.add_argument("--n", type=int, default=10, help="quantos itens testar com --assets")
    args = p.parse_args()

    itens = carregar()
    print(f"acervo: {len(itens)} itens")

    secao("1. Conteúdo duplicado ou vazio")
    hashes, vazios = defaultdict(list), []
    for i in itens:
        caminho = os.path.join(RAIZ, i["caminho"].replace("/", os.sep))
        if not os.path.exists(caminho):
            continue
        if os.path.isdir(caminho):
            # templates e animacoes apontam para uma PASTA de codigo, nao um arquivo:
            # o hash sai do conteudo concatenado dos arquivos, em ordem estavel
            h = hashlib.md5()
            algum = False
            for r, dirs, files in sorted(os.walk(caminho)):
                for f in sorted(files):
                    try:
                        with open(os.path.join(r, f), "rb") as fh:
                            h.update(fh.read())
                        algum = True
                    except OSError:
                        pass
            if not algum:
                vazios.append(i["id"])
                continue
            hashes[h.hexdigest()].append(i["id"])
            continue
        with open(caminho, "rb") as fh:
            dados = fh.read()
        if len(dados.strip()) == 0:
            vazios.append(i["id"])
        hashes[hashlib.md5(dados).hexdigest()].append(i["id"])
    dups = [v for v in hashes.values() if len(v) > 1]
    if dups:
        for grupo in dups:
            print(f"  duplicados: {' == '.join(grupo)}")
    else:
        print("  nenhuma duplicata exata")
    if vazios:
        print(f"  VAZIOS (candidatos a remoção): {', '.join(vazios)}")

    secao("2. Fichas fracas — a busca não vai achar estes")
    fracos = []
    for i in itens:
        problemas = []
        if len(i["quando_usar"]) < 40:
            problemas.append("quando_usar curto")
        if i["nao_usar_quando"].strip().lower() in [g.lower() for g in GENERICO]:
            problemas.append("sem contraindicação")
        if len(i["tags"]) < 3:
            problemas.append("poucas tags")
        if problemas:
            fracos.append((i["id"], problemas))
    if fracos:
        for pid, probs in fracos[:20]:
            print(f"  {pid}: {', '.join(probs)}")
        if len(fracos) > 20:
            print(f"  ... e mais {len(fracos) - 20}")
    else:
        print("  todas as fichas estão completas")

    secao("3. Marcados como rascunho ou descarte")
    for i in itens:
        if i["qualidade"] in ("rascunho", "descartar"):
            print(f"  [{i['qualidade']}] {i['id']} — {i['titulo']}")

    secao("4. Dependências que o projeto precisa ter")
    deps = Counter()
    for i in itens:
        deps.update(i["deps"])
    for dep, n in deps.most_common(12):
        alerta = "  <- exige arquivo no projeto, não é pacote npm" if dep.startswith("@/") else ""
        print(f"  {n:3d}  {dep}{alerta}")

    secao("4b. Dependências entre componentes do acervo")
    por_origem = {}
    for i in itens:
        if i.get("arquivo_origem", "").startswith("@"):
            por_origem[i["arquivo_origem"].split("/")[-1]] = i["id"]
    faltantes = {}
    for i in itens:
        for p in i.get("precisa_componentes", []):
            if p not in por_origem:
                faltantes.setdefault(p, []).append(i["id"])
    if faltantes:
        print("  puxados por itens do acervo mas AUSENTES dele:")
        for p, quem in sorted(faltantes.items(), key=lambda kv: -len(kv[1])):
            amostra = ", ".join(quem[:3]) + ("…" if len(quem) > 3 else "")
            print(f"    {p:26s} ({len(quem)}x) — ex: {amostra}")
        print("  (primitivos do shadcn base costumam ser esperados aqui)")
    else:
        print("  todas as dependências internas estão no acervo")

    secao("5. Projetos referenciados — onde moram os assets")
    referenciados = [i for i in itens if i.get("projeto_origem")]
    if referenciados:
        quebrados = [i for i in referenciados if not os.path.isdir(i["projeto_origem"])]
        peso = sum(i.get("peso_assets_mb", 0) for i in referenciados)
        print(f"  {len(referenciados)} itens referenciam projeto externo ({peso:.0f} MB de assets)")
        if quebrados:
            print("  CAMINHO QUEBRADO — o código está no acervo mas a mídia sumiu:")
            for i in quebrados:
                print(f"    {i['id']}: {i['projeto_origem']}")
        else:
            print("  todos os caminhos ainda existem")
    else:
        print("  nenhum item referencia projeto externo")

    secao("6. Assets externos perecíveis")
    com_assets = [i for i in itens if i["assets_pereciveis"]]
    print(f"  {len(com_assets)} de {len(itens)} itens dependem de assets externos")
    print("  (figma.site / cloudfront / higgs.ai — buckets temporários)")

    if args.assets:
        import urllib.error
        import urllib.request
        print(f"\n  testando os {args.n} primeiros...")
        for i in com_assets[: args.n]:
            caminho = os.path.join(RAIZ, i["caminho"].replace("/", os.sep))
            with open(caminho, encoding="utf-8", errors="replace") as fh:
                texto = fh.read()
            urls = re.findall(r'https?://[^\s"\'`)\]<>]+', texto)
            urls = [u for u in urls if "fonts.g" not in u][:1]
            for u in urls:
                try:
                    req = urllib.request.Request(u, method="HEAD")
                    with urllib.request.urlopen(req, timeout=8) as r:
                        estado = f"ok {r.status}"
                except urllib.error.HTTPError as e:
                    estado = f"MORTO {e.code}"
                except Exception as e:
                    estado = f"FALHA {type(e).__name__}"
                print(f"    {i['id']:22s} {estado}")
    else:
        print("  use --assets para testar se as URLs ainda respondem")

    secao("Resumo")
    print(f"  duplicatas: {len(dups)}   vazios: {len(vazios)}   fichas fracas: {len(fracos)}")
    print(f"  dependentes de asset externo: {len(com_assets)}")


if __name__ == "__main__":
    main()
