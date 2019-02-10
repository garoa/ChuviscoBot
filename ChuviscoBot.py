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
from infogaroa import InfoGaroa
from agenda import Agenda, MESES
from bot_setup import (bot_setup,
                       bot_run,
                       bot_command,
                       bot_task_daily,
                       BOT_CMDS)
debug_chat_id = 0

if len(sys.argv) not in [2, 3]:
  print("Usage:    {} TOKEN [CHAT_ID]".format(sys.argv[0]))
  print("          TOKEN: Valor de token gerado pelo BotFather após o registro de um novo bot.")
  print("          CHAT_ID: Grupo ou conversa para onde o bot deve mandar mensagens de debugging.")
  sys.exit(-1)
else:
  token = sys.argv[1]
  if len(sys.argv) == 3:
    debug_chat_id = int(sys.argv[2])
  bot_setup(token)
  agenda = Agenda()
  

@bot_command
def cmd_help(bot, update):
  """Exibe os comandos disponíveis."""
  cmd_docs = "\n".join(["  <b>/{}</b> - {}".format(name, doc) for name, doc in BOT_CMDS.items()])
  update.message.reply_text("Comandos disponíveis:\n{}".format(cmd_docs), parse_mode="HTML")


@bot_command
def cmd_proximos(bot, update):
  """Lista os próximos eventos na agenda do Garoa."""
  agenda.load_Proximos_Eventos()
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text="Próximos eventos:\n{}\n".format(agenda.proximos_to_html()))


@bot_command
def cmd_regulares(bot, update):
  """Lista as atividades recorrentes."""
  agenda.load_Eventos_Regulares()
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text="Eventos regulares:\n{}\n".format(agenda.regulares_to_html()))


@bot_command
def cmd_agenda(bot, update):
  """Lista a agenda completa."""
  agenda.load_Proximos_Eventos()
  agenda.load_Eventos_Regulares()
  bot.send_message(chat_id=update.message.chat_id,
                   parse_mode="HTML",
                   text=("Próximos eventos:\n{}\n\n"
                         "Eventos regulares:\n{}\n").format(agenda.proximos_to_html(),
                                                            agenda.regulares_to_html()))


@bot_command
def cmd_cadastro(bot, update):
  """Cadastra um novo evento na wiki"""
  pass

@bot_command
def cmd_status(bot, update):
  """Verifica se o garoa está aberto ou fechado"""
  infogaroa = InfoGaroa()
  if(infogaroa.status() == False):
    sticker_id = 'CAADAQAD8AADBO9jB1DAGOCS82CUAg' # fechado
  else:
    sticker_id = 'CAADAQAD8QADBO9jB8Q5ImC_h8fqAg' # aberto
  bot.send_sticker(chat_id=update.message.chat_id,
                   sticker=sticker_id,
                   disable_notification=True)


def get_chat_id(group_link):
  """ Dado um nome de grupo como "DS_Garoa" extraido
      da URL de convite https://t.me/DS_Garoa
      Retorna o valor numérico do chat_id.

      Enquanto essa função não for implementada corretamente
      iremos retornar o chat_id de um grupo de teste de desenvolvimento
  """
  # FIXME!
  return debug_chat_id


def move_para_eventos_passados(e):
  pass #TODO: Implement-me!


#WIP: @bot_task_daily
def checa_se_vai_rolar_evento(bot, job):
  from telegram import ReplyKeyboardRemove, KeyboardButton
  agenda.load_Proximos_Eventos()
  for e in agenda.proximos:
    e.group_link = "foo" #FIXME: extrair esse link por meio do parser de evento
    e.confirmado = False #FIXME: inicializar isso na classe Evento
    dias = e.dias_para_o_evento()
    if dias < 0:
      move_para_eventos_passados(e)
    elif not e.confirmado and dias >= 1 and dias <= 3:
      chat_id = get_chat_id(e.group_link)
      if chat_id:
        data = "{}/{}/{}".format(e.dia,
                                 MESES[e.mes - 1],
                                 e.ano)
        bot.send_message(chat_id=chat_id,
                         parse_mode="HTML",
                         text=("O evento '{}' está agendado para {}."
                               " Alguém aqui confirma que vai rolar mesmo?").format(e.nome, data),
                         reply_markup=ReplyKeyboardRemove(
                           keyboard=[[KeyboardButton(text="Tá confirmado, vai rolar!"),
                                      KeyboardButton(text="Não... foi cancelado.")]]))
        # TODO: ler a resposta do usuário e fazer alguma coisa.


bot_run()
