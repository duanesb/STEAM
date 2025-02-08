import flet as ft

def onHoverSimButton(e):
    e.control.bgcolor = "#a99fc2" if e.data == "true" else "#c3bad9"
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
        self.on_click = lambda e: (function(e), clickfix(e))
        self.on_hover= onHoverSimButton
        self.padding=ft.padding.only(5,5,5,0)