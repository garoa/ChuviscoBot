from pytest import mark

@mark.parametrize("given,want",[
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"),
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"),
])
def test_replace_wikilink(given, want):
  from agenda import replace_wikilink
  got = replace_wikilink(given)
  assert want == got


@mark.parametrize("given,want",[
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem [[Noite do Arduino]] no Garoa")
])
def test_replace_external_link(given, want):
  from agenda import replace_external_link
  got = replace_external_link(given)
  assert want == got
