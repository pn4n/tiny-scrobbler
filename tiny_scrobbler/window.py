import dearpygui.dearpygui as dpg

#common winodw properties that used across the app
class Window():
	width = 500
	height = 250
	logo_scale = 0.7
	
	def __init__(self): self.status_bar = False

	def get_status(self): return self.status_bar

	'''
	Set the status of the application.
	Parameters:
		text (str): The text to be displayed in the status bar if previous_res=200.
		previous_res (int, optional): The previous response code, displayed in status bar if it's not equal 200.
		loading (bool, optional): Whether to show a loading spinner. Defaults to True.
	'''
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
	'''
	Create the status bar.
	Parameters:
		text (str): The text to be displayed in the status bar.
		loading (bool, optional): Whether to show a loading spinner.
	'''
	def __create_status__(self, text, loading):
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
			dpg.add_text(text, tag="status bar")
		self.status_bar = True

W = Window()
