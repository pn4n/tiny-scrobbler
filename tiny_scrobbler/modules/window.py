import dearpygui.dearpygui as dpg	

#common winodw properties that used across the app
class Window():
	width = 500
	height = 250
	logo_scale = 0.7
	
	def __init__(self): self.status_bar = None
	
	def __create_status_bar__(self):
		self.status_rect = dpg.draw_rectangle ( parent='primary window',
												show=False,
												pmin=[-20, self.height - 50],
												pmax=[self.width, self.height],
												color=(0,0,0, 55),
												fill=(0,0,0, 55) )
		
		with dpg.group( parent='primary window', show=False,
				  		horizontal=True, pos=[10, self.height - 35]
					  ) as status_bar:
				dpg.add_loading_indicator( tag='spinner',
											show=False,
											color=(255,255,255,255),
											secondary_color=(255,255,255,103),
											radius=1.2,
											thickness=0.2)
				dpg.add_text('status text', tag='status text')
		self.status_bar = status_bar

	'''
	Set the status of the application.
	Parameters:
		text (str): The text to be displayed in the status bar if previous_res=200.
		previous_res (int, optional): The previous response code, displayed in status bar if it's not equal 200.
		loading (bool, optional): Whether to show a loading spinner. Defaults to True.
	'''
	def set_status(self, text, error=False, loading=True):

		if not self.status_bar:
			self.__create_status_bar__()

		if error:
			dpg.configure_item('spinner', show=False)
			dpg.set_value('status text', f'Error: {text}')

		else:
			dpg.set_value('status text', text)
			dpg.configure_item('spinner', show=loading)

		dpg.configure_item(self.status_bar, show=True)
		dpg.configure_item(self.status_rect, show=True)
		
	
	def hide_status(self):
		dpg.configure_item(self.status_bar, show=False)
		dpg.configure_item(self.status_rect, show=False)


W = Window()
