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

URL_WIKI = "https://garoa.net.br/wiki"
URL_EVENTOS_REGULARES = f"{URL_WIKI}/Eventos_Regulares"
URL_PROXIMOS_EVENTOS = f"{URL_WIKI}/Próximos_Eventos"


class Evento:
  def __init__(self, line, recorrencia=False):
    if recorrencia:
      self.parse_evento_regular(line, recorrencia)
    else:
      self.parse_evento(line)


  def __str__(self):
    return self.__repr__()


  def __repr__(self):
    if self.recorrencia:
      return f"<strong>{self.data}:</strong> {self.nome} ({self.recorrencia})"
    else:
      return f"<strong>{self.data}:</strong> {self.nome}"


  def replace_wikilink(self, original):
    try:
      a, b = original.split("[[")
      b, c = b.split("]]")
      pagename = b
      title = b
      if "|" in b:
        pagename, title = b.split("|")
      com_link = f"{a}<a href='{URL_WIKI}/{pagename}'>{title}</a>{c}"
      return com_link
    except:
      return original


  def replace_external_link(self, original):
    try:
      a, b = original.split("[")
      b, c = b.split("]")
      x = b.split()
      url = x.pop(0)
      title = " ".join(x)
      com_link = f"{a}<a href='{url}'>{title}</a>{c}"
      return com_link
    except:
      return original


  def replace_links(self, txt):
    txt = self.replace_wikilink(txt)
    txt = self.replace_external_link(txt)
    return txt


  def parse_evento(self, line):
    head, tail = line.strip().split(":'''")

    self.nome = self.replace_links(tail)
    self.recorrencia = None
    self.data = head.split("*'''")[1]


  def parse_evento_regular(self, line, recorrencia):
    head, tail = line.strip().split(":'''")

    self.nome = self.replace_links(tail)
    self.recorrencia = recorrencia
    self.data = head.split("*'''")[1]
