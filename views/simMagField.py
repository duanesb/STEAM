import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer

def Magnetic_View(router):
    # CREATES THE MAGNETIC POINTERS
    pointers=[]
    rows = 8
    columns = 9
    containerWidth = 20
    containerHeight = 5
    magnetWidth = 125
    magnetHeight = 50

    for row in range(rows):
        pointers.append([])
        for column in range(columns):
            x = 40 + 60 * column
            y= 40 + 45 * row
            container = ft.Container(
                width=containerWidth,height=containerHeight,bgcolor="blue",
                left=x,top=y
            )
            pointers[row].append({"container":container,"absX":x+containerWidth/2,"absY":y+containerHeight/2})

    # CREATES THE MAGNET
    def moveContainer(e:ft.DragUpdateEvent):
        magnetContainer.top = max(0, min(magnetContainer.top + e.delta_y,400-magnetHeight))
        magnetContainer.left = max(0, min(magnetContainer.left + e.delta_x,590-magnetWidth))
        magnetContainer.update()
    
    magnetContainer = ft.GestureDetector(
        left=300,
        top=200,
        content=ft.Container(
            width=magnetWidth,
            height=magnetHeight,
            border=ft.border.all(5,"black"),
            content=ft.Row(
                controls=[
                    ft.Container(width=magnetWidth/2 - 5,height=magnetHeight,bgcolor="red"),
                    ft.Container(width=magnetWidth/2 - 5,height=magnetHeight,bgcolor="white")
                ],
                spacing=0
            )
        ),
        drag_interval=10,
        on_pan_update=moveContainer
    )

    controls = [
        ft.Text("Magnetic Field", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=600,height=400,bgcolor="white", margin=0,padding=0,
                        content=ft.Stack(
                            controls=[
                                *[pointers[row][column]["container"] for row in range(rows) for column in range(columns)],
                                magnetContainer
                            ]
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