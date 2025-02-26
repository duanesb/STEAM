import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer

def Magnetic_View(router):
    # CREATES THE MAGNETIC POINTERS
    pointers=[]
    rows = 8
    columns = 14
    containerWidth = 22
    containerHeight = 5.5
    magnetWidth = 40
    magnetHeight = 100

    for row in range(rows):
        pointers.append([])
        for column in range(columns):
            x = 40 + 38 * column
            y= 40 + 45 * row
            container = ft.Image(
                src="pointer.png",
                width=containerWidth, height=containerHeight,
                left=x,top=y
            )
            pointers[row].append({"container":container,"absX":x+containerWidth/2,"absY":y+containerHeight/2})

    # CREATES THE MAGNET
    def moveContainer(e:ft.DragUpdateEvent):
        global magnitude
        magnitude = 10
        magnetContainer.top = max(0, min(magnetContainer.top + e.delta_y,400-magnetHeight))
        magnetContainer.left = max(0, min(magnetContainer.left + e.delta_x,590-magnetWidth))
        magnetContainer.update()
        for row in range(len(pointers)):
            for column in range(len(pointers[row])):
                magnetX, magnetY = magnetContainer.left+magnetWidth/2, magnetContainer.top+magnetHeight/2 # CENTERS
                pointerX, pointerY = pointers[row][column]["absX"], pointers[row][column]["absY"] # CENTERS
                northX, northY = magnetX, magnetY-magnetHeight/2
                southX, southY = magnetX, magnetY+magnetHeight/2

                # NORTH POLE CALCULATIONS
                deltaPxNx = pointerX - northX
                deltaPyNy = pointerY - northY
                radiusNorth = np.hypot(deltaPxNx,deltaPyNy)
                normNx, normNy = deltaPxNx/radiusNorth, deltaPyNy/radiusNorth
                northX = magnitude/(radiusNorth**2) * normNx
                northY = magnitude/(radiusNorth**2) * normNy

                # SOUTH POLE CALCULATIONS
                deltaPxSx = pointerX - southX
                deltaPySy = pointerY - southY
                radiusSouth = np.hypot(deltaPxSx,deltaPySy)
                normSx, normSy = deltaPxSx/radiusSouth, deltaPySy/radiusSouth
                southX = -magnitude/(radiusSouth**2) * normSx
                southY = -magnitude/(radiusSouth**2) * normSy

                # NET
                netX = northX + southX
                netY = northY + southY
                angle = np.atan2(netY,netX)

                pointers[row][column]["container"].rotate = ft.transform.Rotate(angle+np.pi)
                pointers[row][column]["container"].update()

                # distX, distY = pointerX-magnetX, pointerY-magnetY # DISTANCE BETWEEM COORDS
                # radius = np.hypot(distX,distY) # RADIUS

                # normX, normY = distX/radius, distY/radius

                # x = (magnitude/radius**3)*(3*normX**2-1)
                # y = ((3*magnitude)/radius**3)*(normX*normY)

                # angle = np.atan2(y,x)
                # pointers[row][column]["container"].rotate = ft.transform.Rotate(angle+np.pi)
                # pointers[row][column]["container"].update()

    
    magnetContainer = ft.GestureDetector(
        left=300-magnetWidth/2,
        top=200-magnetHeight/2,
        content=ft.Container(
            width=magnetWidth,
            height=magnetHeight,
            border=ft.border.all(5,"black"),
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(width=magnetWidth - 5,height=magnetHeight/2,bgcolor="red"),
                            ft.Container(width=magnetWidth - 5,height=magnetHeight/2,bgcolor="blue")
                        ],
                        spacing=0
                    )
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
                        width=600,height=400,bgcolor="black", margin=0,padding=0,
                        content=ft.Stack(
                            controls=[
                                *[pointers[row][column]["container"] for row in range(rows) for column in range(columns)],
                                magnetContainer
                            ]
                        )
                    ),
                    ft.Container(width=600,height=90,bgcolor="#706394",border=ft.border.only(top=ft.BorderSide(5,"black")))
                ],
                spacing=0
            )
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content