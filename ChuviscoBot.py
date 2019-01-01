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

import functools
import requests
import sys

from telegram.ext import CommandHandler, Updater
import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

URL_WIKI = "https://garoa.net.br/wiki"
URL_EVENTOS_REGULARES = f"{URL_WIKI}/Eventos_Regulares"
URL_PROXIMOS_EVENTOS = f"{URL_WIKI}/Próximos_Eventos"


class Evento:
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    if self.recorrencia:
      return f"<strong>{self.data}:</strong> {self.nome} ({self.recorrencia})"
    else:
      return f"<strong>{self.data}:</strong> {self.nome}"


def replace_wikilink(original):
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


def replace_external_link(original):
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


def replace_links(txt):
  txt = replace_wikilink(txt)
  txt = replace_external_link(txt)
  return txt


# As rotinas de parsing abaixo são um tanto estritas e só entendem uma formatação bem específica
# Pare tornar esse código mais tolerante a pequenas variações tipicamente introduzidas por edições humanas,
# será provavelmente necessário utilizar expressões regulares.
# Por enquanto as rotinas abaixo são suficientes como prova de conceito.

agenda = []
def parse_evento(line):
  global agenda
  head, tail = line.strip().split(":'''")

  e = Evento()
  e.nome = replace_links(tail)
  e.recorrencia = None
  e.data = head.split("*'''")[1]
  agenda.append(e)


regulares = []
def parse_evento_regular(line, recorrencia):
  global regulares
  head, tail = line.strip().split(":'''")

  e = Evento()
  e.nome = replace_links(tail)
  e.recorrencia = recorrencia
  e.data = head.split("*'''")[1]
  regulares.append(e)


comment = False
def parse_Eventos_Regulares():
  comment = False
  r = requests.get(f"{URL_EVENTOS_REGULARES}?action=raw")
  for line in r.text.split('\n'):
    line = line.strip()
    print(f"LINE: '{line}'")
    if comment:
      if line.endswith("-->"):
        comment = False
        print("comment = False")
      else:
        # TODO: salvar conteudo dos comentarios aqui
        print("OUTRO")
        continue

    if line.startswith("<!--"):
      comment = True
      print("comment = True")
      # Existe a possibilidade de ser um comentário de uma única linha.
      # Portanto precisamos checar novamente:
      if line.endswith("-->"):
        comment = False
        print("<...> comment = False")

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
        parse_evento_regular(line, recorrencia)
      except:
        print(f"Falha ao tentar parsear linha da página 'Eventos Regulares':\n===\n{line}\n===")


def parse_Proximos_Eventos():
  r = requests.get(f"{URL_PROXIMOS_EVENTOS}?action=raw")
  for line in r.text.split('\n'):
    if line.startswith("*'''"):
      try:
        parse_evento(line)
      except:
        print(f"Falha ao tentar parsear linha da página 'Próximos Eventos':\n===\n{line}\n===")


if len(sys.argv) != 2:
  print(f"Usage:    {sys.argv[0]} TOKEN")
  sys.exit(-1)

token = sys.argv[1]
bot = telegram.Bot(token)
updater = Updater(token)
dispatcher = updater.dispatcher
parse_Proximos_Eventos()
parse_Eventos_Regulares()

BOT_CMDS = dict()
def bot_command(func):
  """Register a function as a Telegram Bot command."""
  name = func.__name__.split("cmd_")[1]
  print(f"Registering /{name} command.")

  @functools.wraps(func)
  def func_wrapper(*args, **kwargs):
    print(f"/{name}... ", end="")
    ret_val = func(*args, **kwargs)
    print("DONE")
    return ret_val

  if name not in BOT_CMDS:
    dispatcher.add_handler(CommandHandler(name, func_wrapper))

  BOT_CMDS[name] = func.__doc__
  return func_wrapper


@bot_command
def cmd_help(bot, update):
  """Exibe os comandos disponíveis."""
  cmd_docs = "\n".join([f"  <b>/{name}</b> - {doc}" for name, doc in BOT_CMDS.items()])
  update.message.reply_text(f"Comandos disponíveis:\n{cmd_docs}", parse_mode="HTML")


@bot_command
def cmd_agenda(bot, update):
  """Lista as próximas atividades agendas no Garoa Hacker Clube."""
  eventos_proximos = "\n".join([f"  - {evento}" for evento in agenda])
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=f"Próximos eventos:\n{eventos_proximos}\n")


@bot_command
def cmd_regulares(bot, update):
  """Lista as atividades que acontecem recorrentemente no Garoa."""
  print(regulares)
  eventos_regulares = "\n".join([f"  - {evento}" for evento in regulares])
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=f"Eventos regulares:\n{eventos_regulares}\n")

print(regulares)

print(agenda)

# Start the bot
updater.start_polling()
updater.idle()
