import dearpygui.dearpygui as dpg
from window import W
import os

appimage_base_path = os.environ.get("APPDIR", os.getcwd())
app_path = lambda x: os.path.join(appimage_base_path, x)

logo_scaled_w, logo_scaled_h = 0, 0
btn_w = 200
indent = 20

def run_app(callback):

	logo_width, logo_height, _, data = dpg.load_image(app_path("src/last.png"))

	global logo_scaled_h, logo_scaled_w
	logo_scaled_w = W.logo_scale * logo_width 
	logo_scaled_h = W.logo_scale * logo_height

	with dpg.texture_registry(show=False):
		dpg.add_static_texture(width=logo_width, 
							   height=logo_height,
							   default_value=data, 
							   tag="texture_tag")

	#font
	with dpg.font_registry():
		default_font = dpg.add_font(app_path("src/HelveticaNeueCyr-Light.ttf"), 18)

	dpg.bind_font(default_font)

	with dpg.window(tag="primary window"):
		dpg.add_image('texture_tag',
					  width=logo_scaled_w, 
					  height=logo_scaled_h,
					  pos=[(W.width - logo_scaled_w) / 2, 
					  	   (W.height - logo_scaled_h) / 2 - 35],)
		dpg.add_button(label="Log in", width = btn_w, 
					   callback=callback,
					   tag='main btn',
					   pos=[(W.width - btn_w) / 2, 
					   		(W.height - logo_scaled_h) / 2 + logo_scaled_h])

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
						width=W.width, height=W.height)
	# dpg.show_style_editor()
	dpg.setup_dearpygui()
	dpg.show_viewport()
	dpg.set_primary_window("primary window", True)
	dpg.start_dearpygui()
	dpg.destroy_context()

def add_check_auth_btn(callback):
	dpg.configure_item('main btn',
					pos=[(W.width - indent) / 2 - btn_w, 
						 (W.height - logo_scaled_h) / 2 + logo_scaled_h])
	
	dpg.add_button(label="Check auth", 
				parent="primary window",
				width=btn_w, 
				callback=callback,
				tag='check btn',
				pos=[(W.width + indent) / 2, 
					 (W.height - logo_scaled_h) / 2 + logo_scaled_h])

