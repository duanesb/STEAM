import flet as ft

import sys
import os

def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.join(sys._MEIPASS, "assets")
    else: base_path = ""
    
    return os.path.join(base_path, filename)

click_sound = ft.Audio(get_asset_path("press.WAV"))
hover_sound = ft.Audio(get_asset_path("hover.wav"))

def onHoverSimButton(e):
    if e.data == "true":
        e.control.bgcolor = "#a99fc2"
        hover_sound.play() 
    else: 
        e.control.bgcolor = "#c3bad9"
    e.control.update()

def clickfix(e):
    e.control.bgcolor = "#c3bad9"
    e.control.update()

class SimulatorButton(ft.Container):
    def __init__(self,text,image,function):
        super().__init__()
        self.content= ft.Column(
            controls=[
                ft.Text(text,size=30,weight="bold"),
                ft.Image(image,width=200)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.width=280
        self.border = ft.border.all(5,"#b4abc9")
        self.on_click = lambda e: (function(e), clickfix(e),click_sound.play())
        self.on_hover= onHoverSimButton
        self.padding=ft.padding.only(5,5,5,0)

class BackElevatedButton(ft.ElevatedButton):
    def __init__(self,text,function):
        super().__init__()
        self.height=60
        self.width=175
        self.text=text
        self.color="white"
        self.style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=25,weight="bold"),
            bgcolor="#443b5c",
            shape=ft.RoundedRectangleBorder(radius=5),
            side=ft.BorderSide(width=5,color="#201b2e")
        )
        self.on_click=function

class ContentContainer(ft.Container):
    def __init__(self,content):
        super().__init__()
        self.content=ft.Column(
            controls=content,
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.width=800
        self.height=750
        self.padding=ft.padding.only(top=20)
    
class ContainerDivider(ft.Container):
    def __init__(self,left,top):
        super().__init__()
        self.width=3
        self.height=70
        self.bgcolor="black"
        self.border_radius=ft.border_radius.all(10)
        self.left=left
        self.top=top

class ContainerText(ft.Text):
    def __init__(self,text,size,left,top):
        super().__init__(text)
        self.weight="bold"
        self.size=size
        self.color="black"
        self.left=left
        self.top=top

class ContainerReading(ft.Container):
    def __init__(self,width,left,top,default=None,textField:bool=False,function=None):
        super().__init__()
        if textField:
            self.content = ft.TextField(
                value="N/A",suffix_text="cm ",
                border=ft.InputBorder.NONE,
                content_padding=ft.padding.only(top=-20),
                text_size=14, cursor_color="black",cursor_height=12,
                on_submit=function, disabled=True
            )
            self.bgcolor = "#d6ccdb"
        else:
            self.content = ft.Text(default if default is not None else "N/A", selectable=True)
            self.bgcolor="white"
        self.width=width
        self.height=20
        self.border=ft.BorderSide(3,"grey")
        self.left=left
        self.top=top
    
    def set(self,change):
        self.content.value = change
        self.content.update()
    
    def getVal(self):
        return float(self.content.value)
    
    def enable(self):
        self.content.disabled = False
        self.content.update()
        