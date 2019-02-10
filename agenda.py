#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ChuviscoBot.py
#  
#  (c)2018 Priscila Gutierres <priscila.gutierres@gmail.com>
#  (c)2018 Felipe Correa da Silva Sanches <juca@members.fsf.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
URL_WIKI = "https://garoa.net.br"


def replace_wikilinks(original):
  if "[[" not in original or "]]" not in original:
    return original

  try:
    parts = original.split("[[")
    a = parts.pop(0)
    b = "[[".join(parts)

    parts = b.split("]]")
    b = parts.pop(0)
    c = "]]".join(parts)

    pagename = b
    title = b
    if "|" in b:
      pagename, title = b.split("|")
    com_link = "{}<a href='{}/wiki/{}'>{}</a>{}".format(a, URL_WIKI, pagename, title, c)
    if "[[" in com_link and "]]" in com_link:
      return replace_wikilinks(com_link)
    else:
      return com_link
  except:
    return original


def replace_external_links(original):
  if "[" not in original or "]" not in original:
    return original

  try:
    parts = original.split("[")
    a = parts.pop(0)
    b = "[".join(parts)

    parts = b.split("]")
    b = parts.pop(0)
    c = "]".join(parts)
    
    x = b.split()
    url = x.pop(0)
    title = " ".join(x)
    com_link = "{}<a href='{}'>{}</a>{}".format(a, url, title, c)
    if "[" in com_link and "]" in com_link:
      return replace_external_links(com_link)
    else:
      return com_link
  except:
    return original


def replace_links(txt):
  txt = replace_wikilinks(txt)
  txt = replace_external_links(txt)
  return txt

MESES = ["JAN", "FEV", "MAR", "ABR",
         "MAI", "JUN", "JUL", "AGO",
         "SET", "OUT", "NOV", "DEZ"]

class Evento:
  def __init__(self, line, recorrencia=False):
    self.a_partir = None
    if recorrencia:
      self.parse_evento_regular(line, recorrencia)
    else:
      self.parse_evento(line)

  def date_string(self, sep=":", a_partir_das=""):
    dia = str(self.dia)
    h = str(self.hora)
    m = str(self.minuto)
    if self.dia < 10: dia = "0{}".format(dia)
    if self.hora < 10: h = "0{}".format(h)
    if self.minuto < 10: m = "0{}".format(m)
    mes = MESES[self.mes - 1]
    data = "{}, {}/{}/{} {}{}{}{}".format(self.dia_da_semana,
                                          dia, mes, self.ano,
                                          a_partir_das,
                                          h, sep, m)
    return data

  def to_html(self):
    # o parser de HTML do Telegram não entende a tag "<br/>"
    # então vou substituir por um espaço:
    nome = " ".join(self.nome.split("<br/>"))

    if self.a_partir:
      a_partir_das = "a partir das "
    else:
      a_partir_das = ""

    if self.recorrencia == "Semanal":
      dia = self.dia_da_semana.lower()
      dia = dia[0].upper() + dia[1:]
      DIAS_DA_SEMANA = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
      ]
      if dia not in ["Sábado", "Domingo"]:
        dia = "{}as-feira".format(DIAS_DA_SEMANA.index(dia)+2)

      h = str(self.hora)
      m = str(self.minuto)
      if self.hora < 10: h = "0{}".format(h)
      if self.minuto < 10: m = "0{}".format(m)

      return "<strong>{}s, {}{}h{}:</strong>\n{}".format(dia, a_partir_das, h, m, nome)
    elif self.recorrencia == "Mensal":
      if self.dia_da_semana in ["Sábado", "Domingo"]:
        dia_da_semana = self.dia_da_semana.lower()
        if self.ordem == -1:
          ordem = "Último"
        else:
          ordem = "{}º".format(self.ordem)
      else:
        dia_da_semana = "{}-feira".format(self.dia_da_semana.lower())
        if self.ordem == -1:
          ordem = "Última"
        else:
          ordem = "{}ª".format(self.ordem)

      h = str(self.hora)
      m = str(self.minuto)
      if self.hora < 10: h = "0{}".format(h)
      if self.minuto < 10: m = "0{}".format(m)
      return "<strong>{} {} do mês, {}{}h{}:</strong>\n{}".format(ordem,
                                                                  dia_da_semana,
                                                                  a_partir_das, h, m,
                                                                  nome)
    else:
      return "<strong>{}:</strong> {}".format(self.date_string(sep=':', a_partir_das=a_partir_das),
                                              nome)


  def to_wikicode(self):
    # o parser de HTML do Telegram não entende a tag "<br/>"
    # então vou substituir por um espaço:
    nome = " ".join(self.nome.split("<br/>"))

    if self.a_partir:
      a_partir_das = "a partir das "
    else:
      a_partir_das = ""

    if self.recorrencia == "Semanal":
      dia = self.dia_da_semana.lower()
      dia = dia[0].upper() + dia[1:]
      DIAS_DA_SEMANA = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
      ]
      if dia not in ["Sábado", "Domingo"]:
        dia = "{}as-feira".format(DIAS_DA_SEMANA.index(dia)+2)

      h = str(self.hora)
      m = str(self.minuto)
      if self.hora < 10: h = f"0{h}"
      if self.minuto < 10: m = f"0{m}"
      return "*'''{}s, {}{}h{}:'''<br/>{}".format(dia,
                                                  a_partir_das, h, m,
                                                  nome)
    elif self.recorrencia == "Mensal":
      if self.dia_da_semana in ["Sábado", "Domingo"]:
        dia_da_semana = self.dia_da_semana.lower()
        if self.ordem == -1:
          ordem = "Último"
        else:
          ordem = "{}º".format(self.ordem)
      else:
        dia_da_semana = "{}-feira".format(self.dia_da_semana.lower())
        if self.ordem == -1:
          ordem = "Última"
        else:
          ordem = "{}ª".format(self.ordem)

      h = str(self.hora)
      m = str(self.minuto)
      if self.hora < 10: h = "0{}".format(h)
      if self.minuto < 10: m = "0{}".format(m)
      return "*'''{} {} do mês, {}{}h{}:'''<br/>{}".format(ordem,
                                                    dia_da_semana,
                                                    a_partir_das, h, m,
                                                    nome)
    else:
      return "*'''{}:''' {}".format(self.date_string(sep=':', a_partir_das=a_partir_das),
                                    nome)


  def parse_evento(self, line):
    head, tail = line.strip().split(":'''")

    self.nome = replace_links(tail).strip()
    self.recorrencia = None
    self.data = head.split("*'''")[1]
    self.parse_data_de_evento()


  def parse_evento_regular(self, line, recorrencia):
    head, tail = line.strip().split(":'''")

    self.nome = replace_links(tail)
    self.recorrencia = recorrencia
    self.data = head.split("*'''")[1]
    if recorrencia == "Mensal":
      a, b = self.data.split(" do mês, ")
      ordem, d = a.split()
      if "-feira" in d:
        d = d.split("-feira")[0]
      if "ltim" in ordem:
        self.ordem = -1
      else:
        self.ordem = int(ordem[0])
      self.dia_da_semana = d[0].upper() + d[1:]
    elif recorrencia == "Semanal":
      a, b = self.data.split(", ")
      self.ordem = None
      DIAS = {
        "2as-feiras": "Segunda",
        "3as-feiras": "Terça",
        "4as-feiras": "Quarta",
        "5as-feiras": "Quinta",
        "6as-feiras": "Sexta",
        "Sábados": "Sábado",
        "Domingos": "Domingo"
      }
      self.dia_da_semana = DIAS[a]

    if "a partir das" in b:
      self.a_partir = True
      b = b.split("a partir das")[1]

    h, m = b.split("h")
    self.hora = int(h)
    self.minuto = int(m)

  def parse_data_de_evento(self):
    self.dia_da_semana = self.data.split(", ")[0].strip()
    partes = self.data.split()
    _ = partes.pop(0)
    data = partes.pop(0)
    hora = " ".join(partes)

    if "a partir das" in hora:
      self.a_partir = True
      hora = hora.split("a partir das")[1]

    dia, mes, ano = data.split("/")
    self.dia = int(dia)
    self.mes = 1 + MESES.index(mes)
    self.ano = int(ano)
    h, m = hora.split(":")
    self.hora = int(h)
    self.minuto = int(m)


  def dias_para_o_evento(self):
    """ Calcula quantos dias falta para a data
        de um evento agendado. Esse cálculo é
	"impreciso" porém reflete a interpretação
	mais comum que as pessoas esperam,
	desconsiderando a qunatidade exata de horas
	entre o agora exato e o horário do evento.
    """
    import datetime
    hoje = datetime.datetime.today()
    event_time = datetime.datetime(self.ano,
                                   self.mes,
                                   self.dia,
                                   23, 59) # 1 minuto antes da meia-noite
                                           # de modo a se ter resultados
                                           # coerentes, independente do horário
                                           # do dia em que o método é chamado
                                           # (ou seja, não importam os horários)
    falta = event_time - hoje
    return falta.days

class Agenda():
  # As rotinas de parsing abaixo são um tanto estritas e só entendem uma formatação bem específica
  # Pare tornar esse código mais tolerante a pequenas variações tipicamente introduzidas por edições humanas,
  # será provavelmente necessário utilizar expressões regulares.
  # Por enquanto as rotinas abaixo são suficientes como prova de conceito.

  def __init__(self):
    from pywikibot import Site
    from pywikibot.config2 import register_family_file
    register_family_file('garoa', URL_WIKI)
    self.site = Site()
    self.page_regulares = None
    self.page_proximos = None
    self.load_Proximos_Eventos()
    self.load_Eventos_Regulares()

  def load_Eventos_Regulares(self):
    from pywikibot import Page
    self.page_regulares = Page(self.site, "Eventos Regulares")
    self.regulares = []
    comment = False
    for line in self.page_regulares.text.split('\n'):
      line = line.strip()
      if comment:
        if line.endswith("-->"):
          comment = False
        else:
          # TODO: salvar conteudo dos comentarios aqui
          continue

      if line.startswith("<!--"):
        comment = True
        # Existe a possibilidade de ser um comentário de uma única linha.
        # Portanto precisamos checar novamente:
        if line.endswith("-->"):
          comment = False

      elif line.startswith("==") and line.endswith("=="):
        if "Semanais" in line:
          recorrencia = "Semanal"
        elif "Quinzenais" in line:
          recorrencia = "Quinzenal"
        elif "Mensais" in line:
          recorrencia = "Mensal"
        else:
          recorrencia = None

      elif line.startswith("*'''"):
        try:
          self.regulares.append(Evento(line, recorrencia))
        except:
          print("Falha ao tentar parsear linha da página 'Eventos Regulares':\n===\n{}\n===".format(line))


  def load_Proximos_Eventos(self):
    from pywikibot import Page
    self.page_proximos = Page(self.site, "Próximos Eventos")
    self.proximos = []
    for line in self.page_proximos.text.split('\n'):
      if line.startswith("*'''"):
        try:
          self.proximos.append(Evento(line))
        except:
          print("Falha ao tentar parsear linha da página 'Próximos Eventos':\n===\n{}\n===".format(line))


  def regulares_to_html(self):
    return "\n".join(["  - {}".format(evento.to_html()) for evento in self.regulares])


  def proximos_to_html(self):
    return "\n".join(["  - {}".format(evento.to_html())
                      for evento in self.proximos
                      if evento.dias_para_o_evento() >= 0])
