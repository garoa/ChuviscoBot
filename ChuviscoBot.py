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
    com_link = f"{a}<a href='https://garoa.net.br/wiki/{pagename}'>{title}</a>{c}"
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


agenda = []
def parse_evento(line):
  global agenda
  head, tail = line.strip().split("''':")

  e = Evento()
  e.nome = replace_links(tail)
  e.recorrencia = None
  e.data = head.split("*'''")[1]
  agenda.append(e)


def parse_Proximos_Eventos():
  r = requests.get("https://garoa.net.br/wiki/Pr%C3%B3ximos_Eventos?action=raw")
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
def cmd_eventos(bot, update):
	"""Lista as atividades da agenda do Garoa Hacker Clube."""
	lista_de_eventos = "\n".join([f"  - {evento}" for evento in agenda])
	print(lista_de_eventos)
	bot.send_message(chat_id=update.message.chat_id,
	                 parse_mode="HTML",
	                 text=f"Esta é a lista completa dos eventos futuros:\n{lista_de_eventos}")


# Start the bot
updater.start_polling()
updater.idle()
