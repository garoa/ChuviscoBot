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

from agenda import Agenda

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if len(sys.argv) != 2:
  print(f"Usage:    {sys.argv[0]} TOKEN")
  sys.exit(-1)

token = sys.argv[1]
bot = telegram.Bot(token)
updater = Updater(token)
dispatcher = updater.dispatcher
agenda = Agenda()

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

  dispatcher.add_handler(CommandHandler(name, func_wrapper))
  BOT_CMDS[name] = func.__doc__
  return func_wrapper


@bot_command
def cmd_help(bot, update):
  """Exibe os comandos disponíveis."""
  cmd_docs = "\n".join([f"  <b>/{name}</b> - {doc}" for name, doc in BOT_CMDS.items()])
  update.message.reply_text(f"Comandos disponíveis:\n{cmd_docs}", parse_mode="HTML")


@bot_command
def cmd_proximos(bot, update):
  """Lista os próximos eventos na agenda do Garoa."""
  eventos_proximos = "\n".join([f"  - {evento}" for evento in agenda.proximos])
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=f"Próximos eventos:\n{eventos_proximos}\n")


@bot_command
def cmd_regulares(bot, update):
  """Lista as atividades recorrentes."""
  eventos_regulares = "\n".join([f"  - {evento}" for evento in agenda.regulares])
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=f"Eventos regulares:\n{eventos_regulares}\n")


# Start the bot
updater.start_polling()
updater.idle()
