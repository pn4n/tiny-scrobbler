import dearpygui.dearpygui as dpg
from window import W
import os

appimage_base_path = os.environ.get("APPDIR", os.getcwd())
app_path = lambda x: os.path.join(appimage_base_path, x)

logo_scaled_w, logo_scaled_h = 0, 0
btn_w = 200
indent = 20

def basic_setup():
	#font
	with dpg.font_registry():
		default_font = dpg.add_font(app_path("src/HelveticaNeueCyr-Light.ttf"), 18)

	dpg.bind_font(default_font)

	#theme
	with dpg.theme() as global_theme:
		with dpg.theme_component(dpg.mvAll):
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (135,15,15,255), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (200,0,0,153), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (236,29,29,103), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			
			dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			
			dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			
			dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_TabActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_TabUnfocusedActive, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_DockingPreview, (200,0,0,153), category=dpg.mvThemeCat_Core)

			dpg.add_theme_color(dpg.mvThemeCol_PlotLines, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_PlotLinesHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (200,0,0,153), category=dpg.mvThemeCat_Core)  
			dpg.add_theme_color(dpg.mvThemeCol_PlotHistogramHovered, (236,29,29,103), category=dpg.mvThemeCat_Core) 
			
			dpg.add_theme_color(dpg.mvThemeCol_TextSelectedBg, (200,0,0,153), category=dpg.mvThemeCat_Core)  

	dpg.bind_theme(global_theme)

	dpg.create_viewport(title='Tiny Scrobbler', 
						small_icon=app_path('src/icon_small.png'),
						large_icon=app_path('src/icon_big.png'),
						width=W.width, height=W.height,)
						# resizable=False)

def login_window(login_func, is_valid_app):
	with dpg.group(parent='primary window', show=False) as stage:
		logo_width, logo_height, _, data = dpg.load_image(app_path("src/last.png"))

		global logo_scaled_h, logo_scaled_w
		logo_scaled_w = W.logo_scale * logo_width 
		logo_scaled_h = W.logo_scale * logo_height

		with dpg.texture_registry(show=False):
			dpg.add_static_texture(width=logo_width, 
								height=logo_height,
								default_value=data, 
								tag="texture_tag")

		dpg.add_image('texture_tag',
						width=logo_scaled_w, 
						height=logo_scaled_h,
						pos=[(W.width - logo_scaled_w) / 2, 
							(W.height - logo_scaled_h) / 2 - 35],)
		dpg.add_button(label="Log in", width = btn_w, 
						callback=login_func,
						enabled=is_valid_app,
						tag='main btn',
						pos=[(W.width - btn_w) / 2, 
							(W.height - logo_scaled_h) / 2 + logo_scaled_h])
	return stage



	# dpg.show_style_editor()
	# dpg.setup_dearpygui()
	# dpg.show_viewport()
	# dpg.set_primary_window("primary window", True)

	# if not is_valid_app:
	# 	W.set_status(text="Invalid API keys in config.py or config.json", error=True)
	# else:
	# 	# try to login if keys in config.json are valid
	# 	try: 
	# 		login_func()
	# 	except:
	# 		pass






	# raise Exception("Invalid API keys [config.py]")

# def add_check_auth_btn(login_func):
# 	dpg.configure_item('main btn',
# 					pos=[(W.width - indent) / 2 - btn_w, 
# 						 (W.height - logo_scaled_h) / 2 + logo_scaled_h])
	
# 	dpg.add_button(label="Check auth", 
# 				parent="primary window",
# 				width=btn_w, 
# 				login_func=login_func,
# 				tag='check btn',
# 				pos=[(W.width + indent) / 2, 
# 					 (W.height - logo_scaled_h) / 2 + logo_scaled_h])

def main_window(logout_func):
	# import dearpygui.demo as demo
	# demo.show_demo()
	dpg.draw_rectangle( parent='primary window',
						show=False,
						tag='header',
						pmin=[-5, -5],
						pmax=[W.width, 30],
						color=(0,0,0, 55),
						fill=(0,0,0, 55))
	with dpg.group(parent='primary window', show=False) as stage:

		with dpg.group(horizontal=True):

			with dpg.tab_bar():							
				with dpg.tab(label="Scrobbling"):
					dpg.add_text("This is the avocado tab!")
					dpg.add_button(label="Scrobble", width=W.width)
				
				with dpg.tab(label="Settings"):
					dpg.add_text("This is the broccoli tab!")

				with dpg.tab(label="Cucumber"):
					dpg.add_text("This is the cucumber tab!")
			dpg.add_text('User: ')
			dpg.add_text('username', tag="username")
			dpg.add_button(label='logout', callback=logout_func)

		return stage
	
def load_main_window(data):
	print(data)
	dpg.set_value('username', data['name'])
	dpg.configure_item('header', show=True)

	# dpg.set_primary_window("primary window", True)
	# dpg.add_group(parent='primary window', tag='header',
	# 		      horizontal=True, )
	# 		    #   pos=[10, 10])
	# dpg.add_text(parent='header', str='User: ' + data['name'])
	# dpg.add_button(parent='header', label='logout', callback=logout_func)

	# dpg.add_tab_bar(parent='primary window', tag='tab bar')
	# dpg.add_tab(parent='tab bar', label='Scrobbling')
	# dpg.add_tab(parent='tab bar', label='Settings')


	# with dpg.window(label="primary window"):


	# 	with dpg.menu_bar():
	# 		with dpg.menu(label="Themes"):
	# 			dpg.add_menu_item(label="Dark")
	# 			dpg.add_menu_item(label="Light")
	# 			dpg.add_menu_item(label="Classic")

	# 			with dpg.menu(label="Other Themes"):
	# 				dpg.add_menu_item(label="Purple")
	# 				dpg.add_menu_item(label="Gold")
	# 				dpg.add_menu_item(label="Red")

	# 		with dpg.menu(label="Tools"):
	# 			dpg.add_menu_item(label="Show Logger")
	# 			dpg.add_menu_item(label="Show About")

	# 		with dpg.menu(label="Oddities"):
	# 			dpg.add_button(label="A Button")
	# 			dpg.add_simple_plot(label="Menu plot", default_value=(0.3, 0.9, 2.5, 8.9), height=80)

	# # create header
	# dpg.draw_rectangle( parent='primary window',
	# 					pmin=[-10, 0],
	# 					pmax=[W.width, 30],
	# 					color=(0,0,0, 55),
	# 					fill=(0,0,0, 55))
	



	# 	with dpg.group(horizontal=True, pos=[10, 10]):
	# 		dpg.add_text('User: ' + data['name'], tag="header")
	# 		dpg.add_button(label='logout', callback=logout_func)

	# 	print(data)
	# 	with dpg.tab_bar():							
	# 		with dpg.tab(label="Scrobbling"):
	# 			dpg.add_text("This is the avocado tab!")
			
	# 		with dpg.tab(label="Settings"):
	# 			dpg.add_text("This is the broccoli tab!")

	# 		with dpg.tab(label="Cucumber"):
	# 			dpg.add_text("This is the cucumber tab!")
	
	
