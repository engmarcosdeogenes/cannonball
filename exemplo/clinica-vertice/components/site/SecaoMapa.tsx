"use client";

import Mapa, { rotaGoogle, rotaWaze } from "@/components/kit-mapa/Mapa";

const LOCAL = { lat: -23.5613, lng: -46.6565, zoom: 16 };

export default function SecaoMapa() {
  return (
    <section id="onde" className="secao-mapa">
      <div className="envelope">
        <p className="rotulo">Onde estamos</p>
        <h2 style={{ fontSize: "var(--t-4)", maxWidth: "16ch", marginBottom: "2.5rem" }}>
          Alameda Santos, a duas quadras do metrô
        </h2>
        <Mapa
          local={LOCAL}
          titulo="Clínica Vértice"
          endereco={"Alameda Santos, 1200 — cj. 84\nCerqueira César, São Paulo"}
          descricao="Mapa mostrando a localização da Clínica Vértice na Alameda Santos"
          acoes={[
            { rotulo: "Como chegar", href: rotaGoogle(LOCAL), primaria: true },
            { rotulo: "Waze", href: rotaWaze(LOCAL) },
            { rotulo: "Ligar", href: "tel:+551133334444" },
          ]}
        />
      </div>
    </section>
  );
}
