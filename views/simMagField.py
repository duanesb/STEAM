import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer


def Magnetic_View(router):
    controls = [
        ft.Text("Magnetic Field", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e"),
            content=ft.Column(controls=[
                ft.Container(width=50,height=50,bgcolor="red",rotate=10)
            ])
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content