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
import sys
from agenda import Agenda
from bot_setup import (bot_setup,
                       bot_run,
                       bot_command,
                       BOT_CMDS)

if len(sys.argv) != 2:
  print(f"Usage:    {sys.argv[0]} TOKEN")
  print("          TOKEN: Valor de token gerado pelo BotFather após o registro de um novo bot.")
  sys.exit(-1)
else:
  token = sys.argv[1]
  bot_setup(token)
  agenda = Agenda()

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

@bot_command
def cmd_agenda(bot, update):
  """Lista a agenda completa."""
  eventos_proximos = "\n".join([f"  - {evento}" for evento in agenda.proximos])
  eventos_regulares = "\n".join([f"  - {evento}" for evento in agenda.regulares])
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=(f"Próximos eventos:\n{eventos_proximos}\n\n"
                         f"Eventos regulares:\n{eventos_regulares}\n"))


bot_run()
