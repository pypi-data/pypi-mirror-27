# BOTLIB Framework to program bots
#
# botlib/dcc.py
#
# Copyright 2017,2018 B.H.J Thate
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice don't have to be included.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.
#
# Bart Thate
# Heerhugowaard
# The Netherlands

from botlib.bot import Bot

import logging
import sys

def init(*args, **kwargs):
    bot = DCC(sys.stdin)
    bot.start()
    bot.ready()
    return bot

class DCC(Bot):

    """ do communication over a file descriptor. """

    def __init__(self, *args, **kwargs):
        if len(args) >= 2:
            self._origin = args[1] 
            super().__init__(*args[2:], **kwargs)
        elif len(args) > 1:
            super().__init__(*args[1:], **kwargs)
        else:
            super().__init__()
        self._target = args[0]
        
    def say(self, channel, txt, type):
        if self._origin and self._origin != channel:
            return
        try:
            self._target.write(txt)
            self._target.write("\n")
            self._target.flush()
        except:
            pass

