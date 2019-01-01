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


def help_(bot, update):
	print("help")
	"""Display all avaiable commands when /help is issued."""
	message = '/eventos - Lista as atividades da agenda do Garoa Hacker Clube.'
	update.message.reply_text(message)

def eventos(bot, update):
	"""Lista eventos mediante comando /eventos"""
	print ("eventos")
	lista_de_eventos = "\n".join([f"  - {evento}" for evento in agenda])
	print(lista_de_eventos)
	bot.send_message(chat_id=update.message.chat_id,
	                 parse_mode="HTML",
	                 text=f"Esta é a lista completa dos eventos futuros:\n{lista_de_eventos}")
    

bot = telegram.Bot(token)
updater = Updater(token)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('help', help_))
dispatcher.add_handler(CommandHandler('eventos', eventos))

# Start the bot
updater.start_polling()

updater.idle()
