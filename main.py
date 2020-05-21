from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color,Line,Rectangle
from kivy.base import EventLoop
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty

class RadioButton(ToggleButton):
	"""cambiar el comportamiento de un ToggleButton como el de un RadioButton
	ya que permite tener solo un boton de color seleccionado a la vez"""
	def _do_press(self):
		if self.state == 'normal':
			ToggleButtonBehavior._do_press(self)

class CanvasWidget(Widget):

	line_width = 2
	btnErase = ObjectProperty(RadioButton)

	def on_touch_down(self,touch):
		if Widget.on_touch_down(self,touch):
			return
		with self.canvas:
			#ud : User Data
			touch.ud['current_line'] = Line(points=(touch.x,touch.y),width=self.line_width)

	def on_touch_move(self,touch):
		if 'current_line' in touch.ud:
			touch.ud['current_line'].points += (touch.x,touch.y)


	def clear_canvas(self):
		saved = self.children[:] #copiamos un array completo de hijos en saved(en este caso boton)
		self.clear_widgets() #remueve todos los hijos del widget padre
		self.canvas.clear() #limpia el canvas
		
		"""agrega todos los widgets guardados anteriormente
		en este caso el boton 'Clear' al widget Padre"""
		for widget in saved:
			self.add_widget(widget)

	def set_color(self,new_color):
		self.canvas.add(Color(*new_color))

	def set_line_width(self,line_width='Normal'):
		dictionary_width_line = {'Thin':1 , 'Normal':2 , 'Thick':4}
		if line_width in dictionary_width_line:
			self.line_width = dictionary_width_line[line_width]


	def erase_canvas(self):
		if self.btnErase.state == 'down':
			print("down")
		elif self.btnErase.state == 'stop':
			print("stop")
		elif self.btnErase.state == 'normal':
			print("normal")



class PaintApp(App):

	def build(self):
		self.canvas_widget = CanvasWidget()
		self.canvas_widget.set_color(get_color_from_hex('#2980b9')) #inicialmente es azul
		return self.canvas_widget

if __name__ == '__main__':
	from kivy.config import Config
	Config.set('graphics','width','960') #setear ancho
	Config.set('graphics','height','540') #setear alto
	Config.set('graphics','resizable','False') #no es redimensionable
	Config.set('input','mouse','mouse,disable_multitouch') #desactivar multitouch y esos circulos rojos (click derecho)
	from kivy.core.window import Window
	from kivy.utils import get_color_from_hex
	Window.clearcolor = get_color_from_hex('#FFFFFF')
	PaintApp().run()

#activar entorno virtual
#source ~/kivy_venv/bin/activate