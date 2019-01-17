#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  infogaroa.py
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

from urllib import request
import json

class InfoGaroa:
  def __init__(self, END_POINT = 'http://garoahc.appspot.com/status' ):
    self.f = request.urlopen(END_POINT)
    self.data = json.loads(self.f.readline())
    
  def retorna_tel(self):
    return self.data.get('phone')

  def retorna_twitter(self):
    return str('@') + self.data.get('twitter')
		 
  def retorna_end(self):
    return self.data.get('space')
		
  def status(self):
    return self.data.get('open')
	
