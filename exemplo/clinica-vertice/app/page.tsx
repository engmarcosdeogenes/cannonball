import SecaoAgendamento from "@/components/site/SecaoAgendamento";
import SecaoMapa from "@/components/site/SecaoMapa";

const SERVICOS = [
  { nome: "Avaliação", preco: "Gratuita",
    texto: "Exame clínico, panorâmica e um plano de tratamento por escrito. Sem compromisso." },
  { nome: "Limpeza e profilaxia", preco: "R$ 280",
    texto: "Remoção de tártaro, polimento e aplicação de flúor. Uma hora, uma sessão." },
  { nome: "Clareamento", preco: "a partir de R$ 900",
    texto: "Em consultório, com moldeira personalizada. Terças e quintas." },
];

export default function Pagina() {
  return (
    <main>
      {/* Hero TIPOGRÁFICO — a escolha do passo 2.2 da kit-montar.
          Sem imagem, sem vídeo, sem canvas: nada para carregar, nada para
          expirar, e nenhuma máquina em que ele deixe de renderizar. É o tipo
          que a skill recomenda quando o cliente ainda não tem material. */}
      <header className="hero">
        <div className="envelope">
          <p className="rotulo">Odontologia · São Paulo</p>
          <h1>
            Um sorriso que <em>não parece</em> trabalho de dentista
          </h1>
          <p className="lead">
            Avaliação gratuita, plano por escrito e preço fechado antes de começar.
            Sem pacote, sem surpresa na segunda consulta.
          </p>
          <div className="acoes">
            <a className="botao botao--forte" href="#agendar">Agendar avaliação</a>
            <a className="botao" href="#onde">Onde estamos</a>
          </div>
        </div>
      </header>

      <section id="servicos">
        <div className="envelope">
          <p className="rotulo">O que fazemos</p>
          <h2 style={{ fontSize: "var(--t-4)", maxWidth: "18ch" }}>
            Três coisas, bem feitas
          </h2>
          <div className="grade">
            {SERVICOS.map((s) => (
              <article className="cartao" key={s.nome}>
                <h3>{s.nome}</h3>
                <p>{s.texto}</p>
                <span className="preco">{s.preco}</span>
              </article>
            ))}
          </div>
        </div>
      </section>

      <SecaoAgendamento />
      <SecaoMapa />

      <footer>
        <div className="envelope">
          <p style={{ margin: 0 }}>
            Clínica Vértice · CRO-SP 00000 · Alameda Santos, 1200 — São Paulo
          </p>
          <p style={{ margin: "0.5rem 0 0" }}>
            Clínica fictícia. Exemplo do{" "}
            <a href="https://github.com/harebeats/cannonball">cannonball</a>, montado
            com as três peças que vêm na instalação.
          </p>
        </div>
      </footer>
    </main>
  );
}
