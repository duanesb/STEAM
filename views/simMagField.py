import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer,ContainerDivider,ContainerText

def Magnetic_View(router):
    # CREATES THE MAGNETIC POINTERS
    pointers=[]
    rows = 8
    columns = 14
    containerWidth = 22
    containerHeight = 5.5
    magnetWidth = 40
    magnetHeight = 100
    magStrength = 10

    opaLowBound = 4.75e-5
    opaUppBound = 3e-4

    # PHYSICS FORMULA (DISTANCE FROM MAGNET TO POINTER, MAGNET STRENGTH, STRENGTH DIRECTION)
    def calculatePhysics(magnetLeft,magnetTop,pointX,pointY,rawMagStrength):
        nonlocal opaLowBound,opaUppBound
        magnetX, magnetY = magnetLeft+magnetWidth/2, magnetTop+magnetHeight/2
        northX, northY = magnetX, magnetY-magnetHeight/2
        southX, southY = magnetX, magnetY+magnetHeight/2
        magnitude = (float(rawMagStrength))/(1400-9)*50

        # NORTH POLE CALCULATIONS
        deltaPxNx = pointX - northX
        deltaPyNy = pointY - northY
        radiusNorth = np.hypot(deltaPxNx,deltaPyNy)
        normNx, normNy = deltaPxNx/radiusNorth, deltaPyNy/radiusNorth
        northX = magnitude/(radiusNorth**2) * normNx
        northY = magnitude/(radiusNorth**2) * normNy

        # SOUTH POLE CALCULATIONS
        deltaPxSx = pointX - southX
        deltaPySy = pointY - southY
        radiusSouth = np.hypot(deltaPxSx,deltaPySy)
        normSx, normSy = deltaPxSx/radiusSouth, deltaPySy/radiusSouth
        southX = -magnitude/(radiusSouth**2) * normSx
        southY = -magnitude/(radiusSouth**2) * normSy

        # NET
        netX = northX + southX
        netY = northY + southY
        angle = np.atan2(netY,netX)
        strength = np.hypot(netX,netY)

        # VISUAL
        opaCheck = np.clip(strength,opaLowBound,opaUppBound)
        opaScalar = 0.2 + 0.8*(opaCheck-opaLowBound)/(opaUppBound-opaLowBound)

        # print(f"{pointers[3][3]["absX"]}, {pointers[3][3]["absY"]}")
        # pointers[3][3]["container"].update()
        # if(pointers[row][column]["absX"] == 165 and pointers[row][column]["absY"] == 177.75):
            # print("{:.2e}".format(strength))
        
        return {"opacity":opaScalar,"angle":angle,"strength":strength}

    # CREATES POINTERS
    for row in range(rows):
        pointers.append([])
        for column in range(columns):
            x = 40 + 38 * column
            y= 40 + 45 * row
            container = ft.Container(
                width=containerWidth, height=containerHeight,
                bgcolor="white", left=x,top=y
            )
            pointers[row].append({"container":container,"absX":x+containerWidth/2,"absY":y+containerHeight/2})

    # CREATES THE MAGNET
    def moveContainer(e:ft.DragUpdateEvent):
        nonlocal magStrength

        # GET SCALAR MAGNITUDE
        magnitude = magStrength

        magnetContainer.top = max(0, min(magnetContainer.top + e.delta_y,400-magnetHeight))
        magnetContainer.left = max(0, min(magnetContainer.left + e.delta_x,590-magnetWidth))
        magnetContainer.update()
        for row in range(len(pointers)):
            for column in range(len(pointers[row])):
                changes = calculatePhysics(magnetContainer.left,magnetContainer.top,pointers[row][column]["absX"],pointers[row][column]["absY"],magnitude)
                
                # VISUAL CHANGES
                pointers[row][column]["container"].bgcolor = f"white,{changes["opacity"]}"
                pointers[row][column]["container"].rotate = ft.transform.Rotate(changes["angle"]+np.pi)
                pointers[row][column]["container"].update()

                # TEST
                # print(f"{pointers[3][3]["absX"]}, {pointers[3][3]["absY"]}")
                # pointers[3][3]["container"].update()
                # if(pointers[row][column]["absX"] == 165 and pointers[row][column]["absY"] == 177.75):
                    # print("{:.2e}".format(changes["strength"]))

    def updateMagStrength(e):
        nonlocal magStrength
        magStrength = int(e.control.value)
        magStrengthText.value = f"{magStrength} mT"
        magStrengthText.update()

        for row in range(len(pointers)):
            for column in range(len(pointers[row])):
                changes = calculatePhysics(magnetContainer.left,magnetContainer.top,pointers[row][column]["absX"],pointers[row][column]["absY"],magStrength)
                pointers[row][column]["container"].bgcolor = f"white,{changes["opacity"]}"
                pointers[row][column]["container"].update()
    
    def hideAnchorMenu(e):
        magnetStrengthContainerText.value = "0 mT"
        anchorMenu.visible = False
        anchorSim.visible = True
        anchorMenu.update()
        anchorSim.update()
        magnetStrengthContainerText.update()
    
    def hideAnchorSim(e):
        magnetStrengthContainerText.value = "N/A"
        anchorMenu.visible = True
        anchorSim.visible = False
        anchorMenu.update()
        anchorSim.update()
        magnetStrengthContainerText.update()
    
    def moveAnchor(e:ft.DragUpdateEvent):
        anchorSim.top = max(0, min(anchorSim.top + e.delta_y,400-25))
        anchorSim.left = max(0, min(anchorSim.left + e.delta_x,590-25))
        anchorSim.update()
    
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
                            ft.Container(width=magnetWidth - 10,height=magnetHeight/2-5,bgcolor="red"),
                            ft.Container(width=magnetWidth - 10,height=magnetHeight/2-5,bgcolor="blue")
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

    magStrengthText = ft.Text(
        "10mT",size=22,weight="bold",color="white",
        left=470,top=15,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    anchorContainer = ft.Container(
        width=25,height=25,bgcolor="red",
        border_radius=ft.border_radius.all(30),
        border=ft.border.all(2,"#ab4341"),
    )

    anchorMenu = ft.Container(
        content=anchorContainer,
        left=135, top=50,
        on_click= hideAnchorMenu
    )

    anchorSim = ft.GestureDetector(
        visible=False,
        left=10,top=10,
        content= anchorContainer,
        drag_interval=10,
        on_pan_update= moveAnchor,
        on_double_tap=hideAnchorSim
    )

    magnetStrengthContainerText = ft.Text("N/A")
    magnetStrengthContainer = ft.Container(
        width=120,
        height=20,
        bgcolor="white",border=ft.BorderSide(3,"grey"),
        left=225,top=45,
        content=magnetStrengthContainerText
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
                                magnetContainer,
                                anchorSim

                            ]
                        )
                    ),
                    ft.Container(width=600,height=90,bgcolor="#706394",border=ft.border.only(top=ft.BorderSide(5,"black")),
                        content=ft.Stack(
                            controls=[
                                ContainerDivider(90,10),
                                ContainerText("Field Meter",18,100,13),
                                ContainerText("Click Then Drag",11,102,33),
                                anchorMenu, # ANCHOR FOR CONTAINER
                                ContainerDivider(211,10),
                                ContainerText("Field Strength",18,221,13),
                                magnetStrengthContainer, # ANCHOR FOR FIELD STRENGTH
                                ContainerDivider(360,10),
                                ContainerText("Magnet\nStrength",18,374,16),
                                ft.Slider(
                                    min=10,max=1400,divisions=100,
                                    width=140,
                                    left=447,top=40,
                                    active_color="#ab9dd4", on_change=updateMagStrength
                                ),
                                magStrengthText # MAGNET STRENGTH TEXT
                            ]
                        )
                    )
                ],
                spacing=0
            )
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content