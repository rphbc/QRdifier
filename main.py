# coding: utf-8
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()
