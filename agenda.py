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
    com_link = f"{a}<a href='{URL_WIKI}/wiki/{pagename}'>{title}</a>{c}"
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
    com_link = f"{a}<a href='{url}'>{title}</a>{c}"
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
    if recorrencia:
      self.parse_evento_regular(line, recorrencia)
    else:
      self.parse_evento(line)

  def date_string(self):
    dia = str(self.dia)
    h = str(self.hora)
    m = str(self.minuto)
    if self.dia < 10: dia = f"0{dia}"
    if self.hora < 10: h = f"0{h}"
    if self.minuto < 10: m = f"0{m}"
    mes = MESES[self.mes - 1]
    data = f"{self.dia_da_semana}, {dia}/{mes}/{self.ano} {h}:{m}"
    return data

  def to_html(self):
    data = self.date_string()
    if self.recorrencia:
      return f"<strong>{data}:</strong> {self.nome} ({self.recorrencia})"
    else:
      return f"<strong>{data}:</strong> {self.nome}"

  def to_wikicode(self):
    data = self.date_string()
    if self.recorrencia:
      return f"*'''{data}:''' {self.nome} ({self.recorrencia})"
    else:
      return f"*'''{data}:''' {self.nome}"

  def parse_evento(self, line):
    head, tail = line.strip().split(":'''")

    self.nome = replace_links(tail)
    self.recorrencia = None
    self.data = head.split("*'''")[1]
    self.parse_data_de_evento()


  def parse_evento_regular(self, line, recorrencia):
    head, tail = line.strip().split(":'''")

    self.nome = replace_links(tail)
    self.recorrencia = recorrencia
    self.data = head.split("*'''")[1]
    a, b = self.data.split("-feira do mês, ")
    ordem, d = a.split()
    self.ordem = int(ordem[0])
    self.dia_da_semana = d[0].upper() + d[1:]
    h, m = b.split("h")
    self.hora = int(h)
    self.minuto = int(m)

  def parse_data_de_evento(self):
    self.dia_da_semana = self.data.split(", ")[0].strip()
    _, data, hora = self.data.split()
    dia, mes, ano = data.split("/")
    self.dia = int(dia)
    self.mes = 1 + MESES.index(mes)
    self.ano = int(ano)
    h, m = hora.split(":")
    self.hora = int(h)
    self.minuto = int(m)


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
          print(f"Falha ao tentar parsear linha da página 'Eventos Regulares':\n===\n{line}\n===")


  def load_Proximos_Eventos(self):
    from pywikibot import Page
    self.page_proximos = Page(self.site, "Próximos Eventos")
    self.proximos = []
    for line in self.page_proximos.text.split('\n'):
      if line.startswith("*'''"):
        try:
          self.proximos.append(Evento(line))
        except:
          print(f"Falha ao tentar parsear linha da página 'Próximos Eventos':\n===\n{line}\n===")
