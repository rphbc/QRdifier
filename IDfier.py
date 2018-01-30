# coding: utf-8
from kivy.app import App

import cv2
import zbar

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from PIL import Image as pilimage
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label

from kivy.uix.camera import Camera


class CameraApp(App):
    qrcodepresent = False

    def build(self):
        self.img1 = Image()   #cria uma imagem onde depois iremos inserir a imagem da camera
        self.label1= Label(text="IDtifier - Cadastro Online")  #label superior
        self.label2= Label(text=" leitura: - ") #label inferior
        layout = BoxLayout(orientation='vertical')  #|aqui criamos um layout  vertical
        layout.add_widget(self.label1)   #inserimos os widgets segundo a ordem que desejamos apresentá-los na tela
        layout.add_widget(self.img1)  
        layout.add_widget(self.label2)
         
        self.capture = cv2.VideoCapture(0)  #criamos um objeto de capture de vídeo. Associamos à primeira camera
        ret, frame = self.capture.read() #criamos um frame com esta imagem
        # criamos um clock para atualizar a imagem a cada 1/320 de segundo
        Clock.schedule_interval(self.atualizaImagem, 1.0 / 30.0) 
        return layout
 
     
 
    def atualizaImagem(self, dt):
        ret, frame = self.capture.read()   #captura uma imagem da camera
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = pilimage.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # Prints data from image.
        decoded = [x.data for x in zbar_image]

        if not decoded:
            self.qrcodepresent = False
        elif not self.qrcodepresent:
            self.label2.text = str(decoded)
            self.qrcodepresent = True

        buf1 = cv2.flip(frame, 0)   #inverte para não ficar de cabeça para baixo
        buf = buf1.tostring() # converte em textura
         
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
         
        self.img1.texture = texture1 # apresenta a imagem

class TestApp(App):
    def build(self):
        return Camera(play=True, resolution=(640,480))

CameraApp().run()
