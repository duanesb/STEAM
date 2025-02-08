import flet as ft

def onHoverSimButton(e):
    e.control.bgcolor = "#a99fc2" if e.data == "true" else "#c3bad9"
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
        self.on_click=function
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
        self.height=800
        self.padding=ft.padding.only(top=20)
    
