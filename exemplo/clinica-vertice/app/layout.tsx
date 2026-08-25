import type { Metadata } from "next";
import { Instrument_Serif, Instrument_Sans } from "next/font/google";
import "./globals.css";

// Escolhidas por scripts/tipo.py --par "Instrument Serif": casam por desenho e
// as duas são Google Fonts, então podem ser SERVIDAS. O acervo está cheio de
// Aeonik e Suisse Int'l, que não podem.
const display = Instrument_Serif({
  weight: "400", style: ["normal", "italic"], subsets: ["latin"],
  variable: "--font-display", display: "swap",
});
const corpo = Instrument_Sans({
  subsets: ["latin"], variable: "--font-corpo", display: "swap",
});

export const metadata: Metadata = {
  title: "Clínica Vértice — odontologia",
  description:
    "Clínica odontológica em São Paulo. Avaliação, limpeza e clareamento com agendamento online.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${display.variable} ${corpo.variable}`}>
      <body>{children}</body>
    </html>
  );
}
