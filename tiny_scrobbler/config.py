import dearpygui.dearpygui as dpg

#common winodw properties that used across the app
class Window():
    width = 500
    height = 250
    logo_scale = 0.7

    __instance__ = None

    def __new__(cls):
        if cls.__instance__ is None:
            cls.__instance__ = super(Window, cls).__new__(cls)
            cls.__instance__.init_window()
        return cls.__instance__

    def init_window(self):
        with dpg.handler_registry():
            dpg.window(label="primary window")


    def __init__(self): self.status_bar = False

    def get_status(self): return self.status_bar

    def set_status(self, text, previous_res=200, loading=True):
        if previous_res != 200:
            try: #assuming spinner and bar exist
                dpg.configure_item('spinner', show=False)
                dpg.set_value('status bar', f"Error: {previous_res}")
            except:
                if not self.status_bar:
                    self.__create_status__(f"Error: {previous_res}", loading=False)
        else:
            try:
                dpg.set_value("status bar", text)
                dpg.configure_item('spinner', show=loading)
            except:
                if not self.status_bar:
                    self.__create_status__(text, loading=True)

    def __create_status__(self, text, loading=False):
        dpg.draw_rectangle(parent='primary window',
                           pmin=[-20, self.height - 50],
                           pmax=[self.width, self.height],
                           color=(0,0,0, 55),
                           fill=(0,0,0, 55))
        with dpg.group(horizontal=True, parent='primary window', pos=[10, self.height - 35]):
            dpg.add_loading_indicator(tag='spinner',
                                      show=loading,
                                      color=(255,255,255,255),
                                      secondary_color=(255,255,255,103),
                                      radius=1.2,
                                      thickness=0.2)
            dpg.add_text("getting token...", tag="status bar")
        self.status_bar = True

# W = Window()