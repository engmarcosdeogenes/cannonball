"use client";

import { useEffect, useState } from "react";
import Agendamento from "@/components/kit-agendamento/Agendamento";
import {
  gerarHorarios, diaAtende, limiteDaJanela,
  type Regras, type Servico,
} from "@/components/kit-agendamento/regras";

// ---- TROQUE: os serviços do cliente ----
const SERVICOS: Servico[] = [
  { id: "aval", nome: "Avaliação", duracao: 30, preco: "Gratuita",
    descricao: "Exame clínico, radiografia panorâmica e plano de tratamento." },
  { id: "limpeza", nome: "Limpeza e profilaxia", duracao: 60, preco: "R$ 280" },
  { id: "clarea", nome: "Clareamento", duracao: 90, preco: "a partir de R$ 900",
    descricao: "Sessão em consultório com moldeira personalizada.",
    dias: [2, 4] },
];

// ---- TROQUE: o expediente ----
const REGRAS: Regras = {
  expediente: {
    1: [["09:00", "12:00"], ["13:30", "18:00"]],
    2: [["09:00", "12:00"], ["13:30", "18:00"]],
    3: [["09:00", "12:00"], ["13:30", "18:00"]],
    4: [["09:00", "12:00"], ["13:30", "18:00"]],
    5: [["09:00", "12:00"], ["13:30", "17:00"]],
    6: [["09:00", "13:00"]],
  },
  passo: 30,
  antecedencia: 120,
  janelaDias: 60,
};

export default function SecaoAgendamento() {
  // ARMADILHA (crítica, registrada em kit-agendamento):
  // o componente lê "que dia é hoje" durante a renderização. Num Next com
  // servidor em UTC e visitante em UTC−3, das 21h à meia-noite os dois
  // discordam sobre a data: o HTML do servidor sai com um dia bloqueado e o do
  // cliente com outro, e a hidratação quebra. Só montar depois do primeiro
  // efeito, com um esqueleto de altura fixa antes para não pular layout.
  // Nada se perde em SEO — formulário de reserva não é conteúdo indexável.
  const [montado, setMontado] = useState(false);
  useEffect(() => setMontado(true), []);

  return (
    <section id="agendar" className="secao-kit">
      <div className="envelope secao-agendamento">
        <p className="rotulo">Agende</p>
        <h2 style={{ fontSize: "var(--t-4)", maxWidth: "18ch" }}>
          Escolha o horário que <em style={{ fontStyle: "italic", color: "var(--acento)" }}>cabe</em> no seu dia
        </h2>
        <p className="lead" style={{ marginTop: "1rem" }}>
          Confirmação na hora. Se precisar remarcar, é um telefonema.
        </p>

        <div style={{ marginTop: "2.5rem" }}>
          {montado ? (
            <Agendamento
              servicos={SERVICOS}
              carregarHorarios={(data, s) => gerarHorarios(data, s, REGRAS)}
              diaDisponivel={(iso) => SERVICOS.some((s) => diaAtende(iso, s, REGRAS))}
              maxData={limiteDaJanela(REGRAS)}
              textos={{
                tituloQuando: "Qual o melhor dia?",
                confirmar: "Quero este horário",
                semHorario: "Esse dia lotou. Escolha outro que a gente encaixa.",
                // ARMADILHA (registrada em kit-agendamento): o formatador padrão
                // arredonda para uma casa decimal — 75min vira "1.3h" e 90min vira
                // "1.5h". Ninguém lê "1.3h" como uma hora e quinze, e em pt-BR hora
                // quebrada não usa ponto decimal. Formate em h/min.
                duracao: (min) =>
                  min < 60
                    ? `${min}min`
                    : min % 60 === 0
                      ? `${min / 60}h`
                      : `${Math.floor(min / 60)}h${String(min % 60).padStart(2, "0")}`,
              }}
              onConfirmar={async (m) => {
                await fetch("/api/agendar", {
                  method: "POST",
                  headers: { "content-type": "application/json" },
                  body: JSON.stringify(m),
                });
              }}
            />
          ) : (
            <div className="esqueleto" aria-hidden />
          )}
        </div>
      </div>
    </section>
  );
}
