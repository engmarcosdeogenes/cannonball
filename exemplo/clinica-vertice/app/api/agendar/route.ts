// O kit-agendamento entrega a marcação e para. O que acontece depois é seu:
// aqui vai o e-mail, o CRM, o webhook. Este endpoint só ecoa, porque o exemplo
// não tem para onde mandar.
export async function POST(req: Request) {
  const marcacao = await req.json();
  console.log("marcação recebida:", marcacao);
  return Response.json({ ok: true, marcacao });
}
