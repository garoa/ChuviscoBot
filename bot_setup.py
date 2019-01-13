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
import functools
import sys

import logging
import telegram
from telegram.ext import (CommandHandler,
                          Updater,
                          JobQueue)

dispatcher = None
updater = None
job_queue = None
def bot_setup(token):
  global dispatcher, updater, job_queue
  print("bot_setup")
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  token = sys.argv[1]
  bot = telegram.Bot(token)
  job_queue = JobQueue(bot)
  updater = Updater(token)
  dispatcher = updater.dispatcher


def bot_run():
  job_queue.start()
  updater.start_polling()
  updater.idle()

def bot_task_daily(func):
  from datetime import datetime
  job_queue.run_once(func, when=datetime.now()) #FIXME! Daily!
  return func

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
