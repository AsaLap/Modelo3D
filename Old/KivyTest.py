# Sous Windows :
# pip install kivy
# pip install Pillow
# python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew

# coding : utf-8

from kivy.app import App
from kivy.uix.label import Label

class HelloApp(App):
    def build(self):
        return Label(text='Hello World!', font_size='100sp')

HelloApp().run()
