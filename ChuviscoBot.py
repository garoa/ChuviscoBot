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
import sys

from telegram.ext import CommandHandler, Updater
import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class Evento:
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return f"<strong>{self.nome}:</strong> {self.data} {self.horario} ({self.recorrencia})"

agenda = []
e1 = Evento()
e1.nome = "Monitoramento da Qualidade do Ar"
e1.recorrencia = "semanal"
e1.data = "2a-feira"
e1.horario = "19h30"
agenda.append(e1)

e2 = Evento()
e2.nome = "Interpretadores (com Luciano Ramalho)"
e2.recorrencia = "semanal"
e2.data = "6a-feira"
e2.horario = "19h30"
agenda.append(e2)

if len(sys.argv) != 2:
  print(f"Usage:    {sys.argv[0]} TOKEN")
  sys.exit(-1)

token = sys.argv[1]
bot = telegram.Bot(token)
updater = Updater(token)
dispatcher = updater.dispatcher

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
