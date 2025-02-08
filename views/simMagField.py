import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer

def Magnetic_View(router):
    pointers=[]
    rows = 8
    columns = 9
    containerWidth = 20
    containerHeight = 5

    for row in range(rows):
        pointers.append([])
        for column in range(columns):
            x = 40 + 60 * column
            y= 40 + 45 * row
            container = ft.Container(width=containerWidth,height=containerHeight,bgcolor="blue",
                            left = x,
                            top = y
            )

            pointers[row].append({"container":container,"absX":x+containerWidth/2,"absY":y+containerHeight/2})

    controls = [
        ft.Text("Magnetic Field", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=600,height=400,bgcolor="white", margin=0,padding=0,
                        content=ft.Stack(
                            controls=[pointers[row][column]["container"] for row in range(rows) for column in range(columns)]
                        )),
                    ft.Container(width=600,height=90,bgcolor="#7a7094",border=ft.border.only(top=ft.BorderSide(5,"#201b2e"))),
                ],
                spacing=0
            )
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content