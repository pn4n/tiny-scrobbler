#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
from pylast import last

from gui import run_app
from config import Window

dpg.create_context()
W = Window()

def login():
    global last
    W.set_status('getting token...', 200)
    res = last.request_token()
    W.set_status('authorizing with browser...', res)
    res = last.authorize()
    return

run_app(login)