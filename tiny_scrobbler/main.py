#!/usr/bin/env python3
import dearpygui.dearpygui as dpg
from pylast import last

import gui
from window import W

dpg.create_context()

def login():

    W.set_status('getting token...')
    last.request_token()
    W.set_status('authorizing with browser...')
    last.authorize()
    if not dpg.does_item_exist('check btn'):
        gui.add_check_auth_btn(last.start_session)
    return

gui.run_app(login)
