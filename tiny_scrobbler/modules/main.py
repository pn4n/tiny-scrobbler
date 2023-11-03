#!/usr/bin/env python3
import dearpygui.dearpygui as dpg

from last import lastfm
from window import W
import gui as gui

dpg.create_context()

def login():
    W.set_status('authorizing with browser...')
    lastfm.authorize()
    lastfm.get_sk()
    print('after sk?') 

gui.run_app(login, lastfm.keys_are_valid)

