from pytest import mark

@mark.parametrize("given,want",[
  # Substitui um wikilink:
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"),
  # Mas preserva um link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"),
])
def test_replace_wikilinks(given, want):
  from agenda import replace_wikilinks
  got = replace_wikilinks(given)
  assert want == got


@mark.parametrize("given,want",[
  # Substitui um link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
])
def test_replace_external_links(given, want):
  from agenda import replace_external_links
  got = replace_external_links(given)
  assert want == got


@mark.parametrize("given,want",[
  # Substitui wikilink:
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"),
  # Substitui link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
  # Substitui wikilink e link externo:
  (("hoje tem [[Noite do Arduino]]"
    "e amanhã tem [https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"),
   ("hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a>"
    "e amanhã tem <a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>")),
  # Substitui múltiplos wikilinks:
  ("Temos [[Noite do Arduino]] e também [[CMC]] :-)",
   ("Temos <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a>"
    " e também <a href='https://garoa.net.br/wiki/CMC'>CMC</a> :-)")),
  # Substitui multiplos links externos:
  ("Links [http://exemplo.com um] e [http://exemplo.com dois]!",
   "Links <a href='http://exemplo.com'>um</a> e <a href='http://exemplo.com'>dois</a>!"),
])
def test_replace_links(given, want):
  from agenda import replace_links
  got = replace_links(given)
  assert want == got


@mark.parametrize("given,want",[
  # :
  ("*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]", {"dia_da_semana": "Quinta",
                                                              "dia": 17,
                                                              "mes": 1,
                                                              "ano": 2019,
                                                              "hora": 19,
                                                              "minuto": 30}),
])
def test_parse_evento(given, want):
  from agenda import Evento
  got = Evento(given)
  assert want["dia_da_semana"] == got.dia_da_semana
  assert want["dia"] == got.dia
  assert want["mes"] == got.mes
  assert want["ano"] == got.ano
  assert want["hora"] == got.hora
  assert want["minuto"] == got.minuto


FOO_WIKICODE = "*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]"
def test_evento_to_html():
  from agenda import Evento
  e = Evento(FOO_WIKICODE)
  e.dia_da_semana = "Sexta"
  e.dia = 27
  e.mes = 7
  e.ano = 2021
  e.hora = 13
  e.minuto = 0
  e.nome = "Festa!"
  got = e.to_html()
  assert "<strong>Sexta, 27/JUL/2021 13:00:</strong> Festa!" == got

  e.recorrencia = "Semanal"
  got = e.to_html()
  assert "<strong>Sexta, 27/JUL/2021 13:00:</strong> Festa! (Semanal)" == got

def test_evento_to_wikicode():
  from agenda import Evento
  e = Evento(FOO_WIKICODE, recorrencia=False)
  e.dia_da_semana = "Sexta"
  e.dia = 27
  e.mes = 7
  e.ano = 2021
  e.hora = 13
  e.minuto = 0
  e.nome = "Festa!"
  got = e.to_wikicode()
  assert "*'''Sexta, 27/JUL/2021 13:00:''' Festa!" == got

  e.recorrencia = "Semanal"
  got = e.to_wikicode()
  assert "*'''Sexta, 27/JUL/2021 13:00:''' Festa! (Semanal)" == got
