import dearpygui.dearpygui as dpg
from window import W
import webbrowser
import os

appimage_base_path = os.environ.get("APPDIR", os.getcwd())
app_path = lambda x: os.path.join(appimage_base_path, x)

logo_scaled_w, logo_scaled_h = 0, 0
btn_w = 200
indent = 20

def basic_setup():
	# font
	with dpg.font_registry():
		with dpg.font(app_path("src/HelveticaNeueCyr-Light.ttf"), 18) as helvetica:
			dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
			dpg.bind_font(helvetica)

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
	with dpg.theme(tag="hyperlinkTheme"):
		with dpg.theme_component(dpg.mvButton):
			dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 0, 0, 0])
			dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [0, 0, 0, 0])
			dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [200,0,0,63])
			dpg.add_theme_color(dpg.mvThemeCol_Text, [236,29,29,200])
			
	dpg.create_viewport(title='Tiny Scrobbler', 
						small_icon=app_path('src/icon_small.png'),
						large_icon=app_path('src/icon_big.png'),
						width=W.width, height=W.height,
						resizable=False)

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



def main_window(logout_func):
	_, _, _, data1 = dpg.load_image(app_path("src/play.png"))
	_, _, _, data2 = dpg.load_image(app_path("src/pause.png"))
	with dpg.texture_registry():
		texture_id_1 = dpg.add_static_texture(24, 24, data1)
		texture_id_2 = dpg.add_static_texture(24, 24, data2)


	dpg.draw_rectangle( parent='primary window',
						show=False,
						tag='header',
						pmin=[-5, -5],
						pmax=[W.width, 30],
						color=(0,0,0, 55),
						fill=(0,0,0, 35))
	
	dpg.draw_line((-5, 28), (W.width, 28), color=(236,29,29,103), thickness=2)
	# dpg.draw_rectangle( parent='primary window',
	# 					show=False,
	# 					tag='scrobble string',
	# 					pmin=[0, W.height - 45],
	# 					pmax=[W.width, W.height],
	# 					color=(0,0,0, 55),
	# 					fill=(255, 255, 255, 55))
	with dpg.group(parent='primary window', show=False) as stage:

		with dpg.group(horizontal=True):
			dpg.add_image(texture_id_1, tag='play_icon', show=True)
			dpg.add_image(texture_id_2, tag='pause_icon', show=False)

			dpg.add_button(label='Unknown track', tag='current_track_name')
			dpg.bind_item_theme('current_track_name', "hyperlinkTheme")
			dpg.add_text(' : ')
			dpg.add_button(label='Unknown artist', tag='current_track_artist')
			dpg.bind_item_theme('current_track_artist', "hyperlinkTheme")

		with dpg.group(horizontal=True):
			dpg.add_button(label='username', tag='username')
			dpg.bind_item_theme('username', "hyperlinkTheme")

			dpg.add_button(label='logout', callback=logout_func)
			

		return stage
	
def load_main_window(username):
	dpg.configure_item('username', label=username)
	dpg.set_item_callback('username', lambda:webbrowser.open('https://www.last.fm/user/' + username))
	dpg.configure_item('header', show=True)
	# dpg.configure_item('scrobble string', show=True)

def update_track(track):
	dpg.configure_item('current_track_name', label=track['title'])
	dpg.set_item_callback('current_track_name', lambda:webbrowser.open('https://www.last.fm/user/' + track['title']))

	dpg.configure_item('current_track_artist', label=track['artist'])
	dpg.set_item_callback('current_track_artist', lambda:webbrowser.open('https://www.last.fm/user/' + track['title']))

def switch_play_icon(is_playing):
	if is_playing:
		dpg.configure_item('play_icon', show=True)
		dpg.configure_item('pause_icon', show=False)
	else:
		dpg.configure_item('play_icon', show=False)
		dpg.configure_item('pause_icon', show=True)