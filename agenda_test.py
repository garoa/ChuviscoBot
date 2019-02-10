from pytest import mark

@mark.parametrize("given,want", [
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


@mark.parametrize("given,want", [
  # Substitui um link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
])
def test_replace_external_links(given, want):
  from agenda import replace_external_links
  got = replace_external_links(given)
  assert want == got


@mark.parametrize("given,want", [
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


@mark.parametrize("given,want", [
   # Um caso típico:
  ("*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Quinta",
            "local": None,
              "dia": 17,
              "mes": 1,
              "ano": 2019,
             "hora": 19,
           "minuto": 30}),

   # com dia e hora menores que dez:
  ("*'''Sábado, 7/DEZ/2019 9:00:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Sábado",
            "local": None,
              "dia": 7,
              "mes": 12,
              "ano": 2019,
             "hora": 9,
           "minuto": 0}),

   # com dia e hora menores que dez (com um zero à esquerda):
  ("*'''Sábado, 07/DEZ/2019 09:00:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Sábado",
            "local": None,
              "dia": 7,
              "mes": 12,
              "ano": 2019,
             "hora": 9,
           "minuto": 0}),

   # Com tag <br/>:
  ("*'''Quinta, 17/JAN/2019 19:30:'''<br/>[[Noite do Arduino]]",
   {"dia_da_semana": "Quinta",
            "local": None,
              "dia": 17,
              "mes": 1,
              "ano": 2019,
             "hora": 19,
           "minuto": 30}),

   # Contendo 'a partir das' em evento de data fixa:
   ("*'''Sábado, 12/MAR/2020 a partir das 16:00:''' [[Ctf_no_garoa|Capture The Flag]]",
   {"dia_da_semana": "Sábado",
            "local": None,
              "dia": 12,
              "mes": 3,
              "ano": 2020,
	 "a_partir": True,
             "hora": 16,
           "minuto": 00}),

  # Incluindo local:
  ("*'''Domingo, 10/FEV/2019 16:00:''' <small>(sala multi-uso)</small> Cine Garoa: [[Cine Garoa|\"GATTACA\"]]",
   {"dia_da_semana": "Domingo",
            "local": "sala multi-uso",
              "dia": 10,
              "mes": 2,
              "ano": 2019,
             "hora": 16,
           "minuto": 00}),
])
def test_parse_evento(given, want):
  from agenda import Evento
  got = Evento(given)
  assert want["dia_da_semana"] == got.dia_da_semana
  assert want["local"] == got.local
  assert want["dia"] == got.dia
  assert want["mes"] == got.mes
  assert want["ano"] == got.ano
  assert want["hora"] == got.hora
  assert want["minuto"] == got.minuto


@mark.parametrize("given,want", [
  # Evento pontual:
  ({"dia_da_semana": "Sexta",
             "nome": "Festa!",
              "dia": 27,
              "mes": 7,
              "ano": 2021,
             "hora": 13,
           "minuto": 0},
  "<strong>Sexta, 27/JUL/2021 13:00:</strong> Festa!"),

  # Evento regular mensal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>2ª sexta-feira do mês, 13h00:</strong>\nFesta!"),

  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>2º sábado do mês, 13h00:</strong>\nFesta!"),

  # Evento regular mensal na última semana:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Última sexta-feira do mês, 13h00:</strong>\nFesta!"),

  # Evento regular mensal - no último final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Último sábado do mês, 13h00:</strong>\nFesta!"),

  # Evento regular semanal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>6as-feiras, 13h00:</strong>\nFesta!"),

  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Sábados, 13h00:</strong>\nFesta!"),

  # Evento contendo "a partir das" no horário semanal:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Semanal",
             "nome": "Capture The Flag",
         "a_partir": True,
             "hora": 16,
           "minuto": 0},
  "<strong>Sábados, a partir das 16h00:</strong>\nCapture The Flag"),

  # Evento contendo "a partir das" no horário mensal:
  ({"dia_da_semana": "Sábado",
	    "ordem": -1,
      "recorrencia": "Mensal",
             "nome": "Atividade",
         "a_partir": True,
             "hora": 13,
           "minuto": 0},
  "<strong>Último sábado do mês, a partir das 13h00:</strong>\nAtividade"),

  # Evento contendo "a partir das" no horário de data fixa:
  ({"dia_da_semana": "Sábado",
              "dia": 30,
              "mes": 10,
              "ano": 2019,
             "nome": "Alguma coisa legal...",
         "a_partir": True,
             "hora": 14,
           "minuto": 30},
  "<strong>Sábado, 30/OUT/2019 a partir das 14:30:</strong> Alguma coisa legal..."),

  # Evento incluindo local:
  ({"dia_da_semana": "Sábado",
            "local": "sala multi-uso",
              "dia": 30,
              "mes": 10,
              "ano": 2019,
             "nome": "Alguma coisa legal...",
         "a_partir": True,
             "hora": 14,
           "minuto": 30},
  "<strong>Sábado, 30/OUT/2019 a partir das 14:30:</strong> (sala multi-uso) Alguma coisa legal..."),
])
def test_evento_to_html(given, want):
  FOO_WIKICODE = "*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]"
  from agenda import Evento
  e = Evento(FOO_WIKICODE)
  e.dia_da_semana = given.get("dia_da_semana")
  e.local = given.get("local")
  e.dia = given.get("dia")
  e.mes = given.get("mes")
  e.ano = given.get("ano")
  e.a_partir = given.get("a_partir")
  e.hora = given.get("hora")
  e.minuto = given.get("minuto")
  e.nome = given.get("nome")
  e.ordem = given.get("ordem")
  e.recorrencia = given.get("recorrencia")
  got = e.to_html()
  assert want == got


@mark.parametrize("given,want", [
  # Evento pontual:
  ({"dia_da_semana": "Sexta",
             "nome": "Festa!",
              "dia": 27,
              "mes": 7,
              "ano": 2021,
             "hora": 13,
           "minuto": 0},
  "*'''Sexta, 27/JUL/2021 13:00:''' Festa!"),

  # Evento regular mensal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''2ª sexta-feira do mês, 13h00:'''<br/>Festa!"),

  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''2º sábado do mês, 13h00:'''<br/>Festa!"),

  # Evento regular mensal na última semana:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''Última sexta-feira do mês, 13h00:'''<br/>Festa!"),

  # Evento regular mensal - no último final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''Último sábado do mês, 13h00:'''<br/>Festa!"),

  # Evento regular semanal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''6as-feiras, 13h00:'''<br/>Festa!"),

  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "*'''Sábados, 13h00:'''<br/>Festa!"),

  # Evento contendo "a partir das" no horário semanal:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Semanal",
             "nome": "Capture The Flag",
         "a_partir": True,
             "hora": 16,
           "minuto": 0},
  "*'''Sábados, a partir das 16h00:'''<br/>Capture The Flag"),

  # Evento contendo "a partir das" no horário mensal:
  ({"dia_da_semana": "Sábado",
	    "ordem": -1,
      "recorrencia": "Mensal",
             "nome": "Atividade",
         "a_partir": True,
             "hora": 13,
           "minuto": 0},
  "*'''Último sábado do mês, a partir das 13h00:'''<br/>Atividade"),

  # Evento contendo "a partir das" no horário de data fixa:
  ({"dia_da_semana": "Sábado",
              "dia": 30,
              "mes": 10,
              "ano": 2019,
             "nome": "Alguma coisa legal...",
         "a_partir": True,
             "hora": 14,
           "minuto": 30},
  "*'''Sábado, 30/OUT/2019 a partir das 14:30:''' Alguma coisa legal..."),

  # Evento contendo informação de local:
  ({"dia_da_semana": "Sábado",
            "local": "sala multi-uso",
              "dia": 30,
              "mes": 10,
              "ano": 2019,
             "nome": "Alguma coisa legal...",
         "a_partir": True,
             "hora": 14,
           "minuto": 30},
  "*'''Sábado, 30/OUT/2019 a partir das 14:30:''' <small>(sala multi-uso)</small> Alguma coisa legal..."),
])
def test_evento_to_wikicode(given, want):
  FOO_WIKICODE = "*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]"
  from agenda import Evento
  e = Evento(FOO_WIKICODE)
  e.dia_da_semana = given.get("dia_da_semana")
  e.local = given.get("local")
  e.dia = given.get("dia")
  e.mes = given.get("mes")
  e.ano = given.get("ano")
  e.a_partir = given.get("a_partir")
  e.hora = given.get("hora")
  e.minuto = given.get("minuto")
  e.nome = given.get("nome")
  e.ordem = given.get("ordem")
  e.recorrencia = given.get("recorrencia")
  got = e.to_wikicode()
  assert want == got


@mark.parametrize("given,want", [
   # Atividade mensal:
   (("*'''3ª terça-feira do mês, 19h30:''' [[CMC|Reunião do Conselho Manda-Chuva]]", "Mensal"),
   {"dia_da_semana": "Terça",
            "ordem": 3,
             "hora": 19,
           "minuto": 30}),

   # Atividade mensal (na última semana):
   (("*'''Última terça-feira do mês, 19h30:''' [[Noite de Processing]]", "Mensal"),
   {"dia_da_semana": "Terça",
            "ordem": -1, # menos um representando "último"
             "hora": 19,
           "minuto": 30}),

   # Atividade mensal num sábado:
   (("*'''2.o sábado do mês, 14h00:''' [[Alguma Coisa]]", "Mensal"),
   {"dia_da_semana": "Sábado",
            "ordem": 2,
             "hora": 14,
           "minuto": 0}),

   # Atividade mensal num domingo:
   (("*'''3.o domingo do mês, 10h15:''' [[Alguma Coisa]]", "Mensal"),
   {"dia_da_semana": "Domingo",
            "ordem": 3,
             "hora": 10,
           "minuto": 15}),

   # Atividade semanal:
   (("*'''6as-feiras, 19h30:''' [[Turing_Clube/Oficina_de_Linguagens_de_Programação]]", "Semanal"),
   {"dia_da_semana": "Sexta",
             "hora": 19,
           "minuto": 30}),

   # Contendo <br/>:
   (("*'''5as-feiras, 19h30:'''<br/>[[Noite do Arduino]]", "Semanal"),
   {"dia_da_semana": "Quinta",
             "hora": 19,
           "minuto": 30}),

   # Contendo 'a partir das' em evento semanal:
   (("*'''Sábados, a partir das 16h00:''' [[Ctf_no_garoa|Capture The Flag]]", "Semanal"),
   {"dia_da_semana": "Sábado",
	 "a_partir": True,
             "hora": 16,
           "minuto": 00}),

   # Contendo 'a partir das' em evento mensal:
   (("*'''Último sábado do mês, a partir das 16h00:''' XYZ", "Mensal"),
   {"dia_da_semana": "Sábado",
	    "ordem": -1,
	 "a_partir": True,
             "hora": 16,
           "minuto": 00}),
])
def test_parse_evento_regular(given, want):
  from agenda import Evento
  nome, recorrencia = given
  got = Evento(nome, recorrencia)
  assert want.get("dia_da_semana") == got.dia_da_semana
  assert want.get("ordem") == got.ordem
  assert want.get("a_partir") == got.a_partir
  assert want.get("hora") == got.hora
  assert want.get("minuto") == got.minuto
