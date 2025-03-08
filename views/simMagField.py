import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer,ContainerDivider,ContainerText

def Magnetic_View(router):
    pointers=[]
    rows = 8
    columns = 14
    containerWidth = 22
    containerHeight = 5.5
    magnetWidth = 40
    magnetHeight = 120
    magStrength = 10

    opaLowBound = 1.2167e-08
    opaUppBound = 1.0485e-07

    # PHYSICS FORMULA (DISTANCE FROM MAGNET TO POINTER, MAGNET STRENGTH, DIRECTION)
    def calculatePhysics(magnetLeft,magnetTop,pointX,pointY,rawMagStrength):
        nonlocal opaLowBound,opaUppBound
        magnetX, magnetY = magnetLeft+magnetWidth/2, magnetTop+magnetHeight/2
        northX, northY = magnetX, magnetY-magnetHeight/2
        southX, southY = magnetX, magnetY+magnetHeight/2
        magnitude = (float(rawMagStrength))/(1400-9)*50
        
        # MID POINT CALCULATIONS
        distX,distY = abs(magnetX-pointX)/40, abs(magnetY-pointY)/40
        distRadius = np.hypot(distX,distY)

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
        netX = (northX + southX)/4000
        netY = (northY + southY)/4000
        angle = np.atan2(netY,netX)
        strength = np.hypot(netX,netY)

        # VISUAL
        opaCheck = np.clip(strength,opaLowBound,opaUppBound)
        opaScalar = 0.2 + 0.8*(opaCheck-opaLowBound)/(opaUppBound-opaLowBound)        
        return {"opacity":opaScalar,"angle":angle,"strength":strength,"distance":{"x":distX,"y":distY,"radius":distRadius}}

    def updateReadings():
        nonlocal magStrength
        information = calculatePhysics(magnetContainer.left,magnetContainer.top,anchorSim.left+12.5,anchorSim.top+12.5,magStrength)
        mcDistxText.value = f"{information["distance"]["x"]:.2f}cm"
        # mcDistxText.value = f"{information["distance"]["x"]:.2f}"
        mcRadiusText.value = f"{information["distance"]["radius"]:.2f}cm"
        mcStrengthText.value = f"{information["strength"]:.4e}"
        mcDistxText.update()
        mcRadiusText.update()
        mcStrengthText.update()

    def moveContainer(e:ft.DragUpdateEvent):
        nonlocal magStrength
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
        
        if(anchorSim.visible == True):
            updateReadings()

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
        
        if(anchorSim.visible == True):
            updateReadings()

    def hideAnchorMenu(e):
        updateReadings()
        anchorMenu.visible = False
        anchorSim.visible = True
        anchorMenu.update()
        anchorSim.update()
    
    def hideAnchorSim(e):
        mcStrengthText.value = "N/A"
        anchorMenu.visible = True
        anchorSim.visible = False
        anchorMenu.update()
        anchorSim.update()
        mcStrengthText.update()
    
    def moveAnchor(e:ft.DragUpdateEvent):
        anchorSim.top = max(0, min(anchorSim.top + e.delta_y,400-25))
        anchorSim.left = max(0, min(anchorSim.left + e.delta_x,590-25))
        anchorSim.update()
        updateReadings()
    
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
    
    # MAGNET FOR SIMULATOR
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
                            ft.Container(width=magnetWidth - 10,height=magnetHeight/1.99-5,bgcolor="red"),
                            ft.Container(width=magnetWidth - 10,height=magnetHeight/1.99-5,bgcolor="blue")
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

    # ANCHOR ELEMENTS
    anchorContainer = ft.Container(
        width=25,height=25,bgcolor="red",
        border_radius=ft.border_radius.all(30),
        border=ft.border.all(4,"#bd2a28"),
    )
    anchorMenu = ft.Container(
        content=anchorContainer,
        left=45, top=50,
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

    # ELEMENTS THAT CHANGE
    magStrengthText = ft.Text(
        "10mT",size=22,weight="bold",color="white",
        left=470,top=15,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )
    
    # FIELD ELEMENTS
    mcDistxText = ft.Text("N/A",selectable=True)
    mcDistx = ft.Container(
        width=60,
        height=20,
        bgcolor="white",border=ft.BorderSide(3,"grey"),
        left=160,top=15,
        content=mcDistxText
    )

    mcRadiusText = ft.Text("N/A",selectable=True)
    mcRadius = ft.Container(
        width=60,
        height=20,
        bgcolor="white",border=ft.BorderSide(3,"grey"),
        left=285,top=15,
        content=mcRadiusText
    )

    mcStrengthText = ft.Text("N/A",selectable=True)
    mcStrength = ft.Container(
        width=100,
        height=20,
        bgcolor="white",border=ft.BorderSide(3,"grey"),
        left=245,top=45,
        content=mcStrengthText
    )

    mcDistyText = ft.Text("N/A",selectable=True)
    mcDisty = ft.Container(
        width=100,
        height=20,
        bgcolor="white",border=ft.BorderSide(3,"grey"),
        left=245,top=85,
        content=mcDistyText
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
                                ContainerText("Field Meter",18,10,13),
                                ContainerText("Click Then Drag",11,12,33),
                                anchorMenu, # ANCHOR FOR CONTAINER
                                ContainerDivider(121,10),
                                ContainerText("X:",14,135,16), # X DISTANCE READING
                                mcDistx,
                                ContainerText("Y:",14,135,56),
                                ContainerText("Radius:",14,225,16), # RADIUS READING CONTAINER
                                mcRadius, 
                                mcStrength, # STRENGTH READING CONTAINER
                                ContainerDivider(360,10),
                                ContainerText("Magnet\nStrength",18,374,18),
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