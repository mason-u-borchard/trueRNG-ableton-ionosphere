# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:12:11 2023

@author: danic
"""

import rtmidi
from rtmidi.midiconstants import (CONTROL_CHANGE)

midiout = rtmidi.MidiOut()
midiout.open_port(1)

#ctrl+M in ableton and select your parameter, then set to unused midi channel and any CC_num here, then run this script, then ctrl+M again

CHANNEL = 3
CC_NUM = 76

modCC = ([CONTROL_CHANGE | CHANNEL, CC_NUM, 127])
midiout.send_message(modCC)