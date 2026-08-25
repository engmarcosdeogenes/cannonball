#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exporta a versao publica do plugin: o MOTOR, sem o acervo.

O repositorio de trabalho guarda duas coisas que nao podem ser publicadas
juntas. O motor (scripts, skills, referencias) e generico e e o que faz sentido
compartilhar. O acervo e material do usuario — peca de terceiro, projeto de
cliente, prompt comprado — e nao e dele para redistribuir.

Este script deriva o repo publico do de trabalho. Ele NAO mexe no seu: nada e
apagado, nada sai do git local. Voce continua editando aqui e re-exportando.

    python scripts/publicar.py --para ../cannonball-publico
    python scripts/publicar.py --para ../cannonball-publico --listar   # so mostra
"""

import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caminhos import REPO_LOCAL, saida_utf8  # noqa: E402

saida_utf8()

# O motor. Generico, sem material de ninguem dentro.
PUBLICO = ["scripts", "skills", "references", "seed", "exemplo", ".claude-plugin",
           "README.md", "LICENSE", ".gitignore", ".gitattributes"]

# O acervo do usuario. So na RAIZ: seed/acervo e o exemplo que vai de proposito.
NUNCA_NA_RAIZ = ("acervo", "_fonte", "cannonball.config.json", "INSTALAR.md")

# Artefatos de importacao em massa. Carregam material bruto — em lugar nenhum.
NUNCA_EM_LUGAR_NENHUM = ("_extract", "_enriquecimento", "_lote", "_armadilhas_",
                         "_tags_funcao", "_digest", "_duplicatas")

IGNORA = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--para", required=True, help="pasta de destino do repo público")
    ap.add_argument("--listar", action="store_true", help="mostra o que iria, sem copiar")
    args = ap.parse_args()

    destino = os.path.abspath(os.path.expanduser(args.para))
    if os.path.abspath(REPO_LOCAL) == destino:
        sys.exit("destino é o próprio repositório de trabalho. Escolha outra pasta.")

    plano = [n for n in PUBLICO if os.path.exists(os.path.join(REPO_LOCAL, n))]
    faltando = [n for n in PUBLICO if n not in plano]

    if args.listar:
        print(f"iria para {destino}:")
        for n in plano:
            print(f"  {n}")
        if faltando:
            print("não existe aqui (será pulado): " + ", ".join(faltando))
        print("\nfica de fora sempre: " + ", ".join(NUNCA_NA_RAIZ + NUNCA_EM_LUGAR_NENHUM))
        print("(seed/acervo vai de propósito: são as peças de exemplo do cannonball)")
        return

    for nome in plano:
        origem = os.path.join(REPO_LOCAL, nome)
        alvo = os.path.join(destino, nome)
        if os.path.isdir(origem):
            shutil.rmtree(alvo, ignore_errors=True)
            shutil.copytree(origem, alvo, ignore=IGNORA)
        else:
            os.makedirs(destino, exist_ok=True)
            shutil.copy2(origem, alvo)
        print(f"  {nome}")

    # Rede de seguranca: se algo proibido chegou la, e bug — grite antes do commit.
    vazou = [n for n in os.listdir(destino) if n.startswith(NUNCA_NA_RAIZ)]
    for raiz, dirs, arqs in os.walk(destino):
        if ".git" in raiz.replace("\\", "/").split("/"):
            continue
        for n in list(dirs) + arqs:
            if n.startswith(NUNCA_EM_LUGAR_NENHUM):
                vazou.append(os.path.relpath(os.path.join(raiz, n), destino))
    if vazou:
        sys.exit("VAZOU material privado para o destino:\n  " + "\n  ".join(sorted(set(vazou))))

    print(f"\nmotor exportado para {destino}")
    print("acervo NÃO copiado — ele é seu e fica aqui.")
    print("seed/ foi junto: são as peças de exemplo originais do cannonball.\n")
    print("para publicar a primeira vez:")
    print(f"  cd {destino}")
    print("  git init && git add -A")
    print('  git commit -m "cannonball: motor do acervo"')
    print("  gh repo create cannonball --public --source=. --push")


if __name__ == "__main__":
    main()
