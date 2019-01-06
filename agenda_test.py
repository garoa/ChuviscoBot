def test_replace_wikilink():
  from agenda import replace_wikilink
  given = "hoje tem [[Noite do Arduino]] no Garoa"
  want = "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"
  got = replace_wikilink(given)
  assert want == got


def test_replace_external_link():
  from agenda import replace_external_link
  given = "[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"
  want = "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"
  got = replace_external_link(given)
  assert want == got
