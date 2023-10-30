import dearpygui.dearpygui as dpg
from config import Window
import os

# Determine the base path of the AppImage
appimage_base_path = os.environ.get("APPDIR", os.getcwd())

# Build the path to the image relative to the AppImage base path
# image_path = os.path.join(appimage_base_path, "src/last.png")
app_path = lambda x: os.path.join(appimage_base_path, x)

def run_app(login_callback):

	W = Window()
	#logo
	logo_width, logo_height, channels, data = dpg.load_image(app_path("src/last.png"))

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
	    button_w = 200
	    dpg.add_button(label="Log in", width = button_w, 
	                   callback=login_callback,
	                   tag='main btn',
	                   pos=[(W.width - button_w) / 2, 
	                   		(W.height - logo_scaled_h) / 2 + logo_scaled_h])
	                   		# (W.height - logo_scaled_h) / 2 + logo_height - 35])
	    

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
