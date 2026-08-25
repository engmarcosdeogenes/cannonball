# seed — o que vem numa instalação nova

Três peças, e elas são o **exemplo do formato**: o que uma ficha bem escrita
parece, o que é uma contraindicação real, o que é uma armadilha registrada.

São originais, escritas para o cannonball, e obedecem a uma regra que vale para tudo
que você guardar aqui: **nada fixo**. Cor, fonte, raio, texto, regra de negócio e
campos saem de variável CSS (`--kit-*`, com fallback nos tokens do site e,
por último, em `currentColor`/`inherit`) ou de prop. Nenhum literal dentro do
componente. Trocar de cliente é trocar configuração.

O `acervo/` do usuário recebe uma **cópia** disto na primeira vez que qualquer
script roda. Depois disso a pasta é dele: editar, melhorar ou apagar é decisão
dele, e nada aqui volta a sobrescrever.

Para regerar o índice depois de mexer nas peças:

    CANNONBALL_ACERVO="$(pwd)" python3 ../scripts/indexar.py
