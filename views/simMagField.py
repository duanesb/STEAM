import flet as ft
import numpy as np
from objects import BackElevatedButton,ContentContainer,ContainerDivider,ContainerText,ContainerReading

def Magnetic_View(router):
    pointers=[]
    rows = 8
    columns = 14
    containerWidth = 22
    containerHeight = 5.5
    magnetWidth = 40
    magnetHeight = 120
    magStrength = 300

    opaLowBound = 2.65e-08
    opaUppBound = 2.51e-07

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

        pfs = 1.25663706e-06
        # DOUBLE MONOPOLE
        pointXY = np.array([pointX,pointY])
        northXY = np.array([magnetX,magnetY-magnetHeight/2])
        southXY = np.array([magnetX,magnetY+magnetHeight/2])
        magCharge = ((rawMagStrength/1000)/pfs)*0.0001

        radiusNorth = pointXY - northXY
        normRadiusNorth = np.linalg.norm(radiusNorth)
        fieldStrengthNorth = (pfs/(4 * np.pi))*(magCharge*radiusNorth/normRadiusNorth**3)

        radiusSouth = pointXY - southXY
        normRadiusSouth = np.linalg.norm(radiusSouth)
        fieldStrengthSouth = -(pfs/(4*np.pi))*(magCharge*radiusSouth/normRadiusSouth**3)

        netFieldStrength = np.linalg.norm(fieldStrengthNorth - fieldStrengthSouth)
        pullForce = ((netFieldStrength**2)*0.0001)/(2*pfs)


        # NET
        netX = northX + southX
        netY = northY + southY
        angle = np.atan2(netY,netX)
        strength = np.hypot(netX,netY)/4000

        # VISUAL
        opaCheck = np.clip(strength,opaLowBound,opaUppBound)
        opaScalar = 0.2 + 0.8*(opaCheck-opaLowBound)/(opaUppBound-opaLowBound)        
        return {"opacity":opaScalar,"angle":angle,"strength":{"br":netFieldStrength,"pf":pullForce},"distance":{"x":distX,"y":distY,"radius":distRadius}}

    def updateReadings():
        nonlocal magStrength
        information = calculatePhysics(magnetContainer.left,magnetContainer.top,anchorSim.left+12.5,anchorSim.top+12.5,magStrength)
        readingXDist.set(f"{information["distance"]["x"]:.1f}cm")
        readingYDist.set(f"{information["distance"]["y"]:.1f}cm")
        readingRadius.set(f"{information["distance"]["radius"]:.1f}cm")
        readingBr.set(f"{information["strength"]["br"]:.2f}G")
        readingPullForce.set(f"{information["strength"]["pf"]:.2f}N")


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
        readingMagStrength.set(f"{magStrength}mT")
        if magStrength <= 500:
            readingMSComp.value = "Comparison: Ceramic"
        elif magStrength > 500 and magStrength < 900:
            readingMSComp.value = "Comparison: N/A"
        elif magStrength >= 900 and magStrength < 1100:
            readingMSComp.value = "Comparison: SmCo"
        elif magStrength >= 1100 and magStrength < 1170:
            readingMSComp.value = "Comparison: Alnico"
        else:
            readingMSComp.value = "Comparison: Neodymium"
        
        readingMSComp.update()

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
        anchorMenu.visible = True
        anchorSim.visible = False
        anchorMenu.update()
        anchorSim.update()
        readingXDist.set("N/A")
        readingYDist.set("N/A")
        readingRadius.set("N/A")
        readingBr.set("N/A")
        readingPullForce.set("N/A")
    
    def moveAnchor(e:ft.DragUpdateEvent):
        anchorSim.top = max(0, min(anchorSim.top + e.delta_y,400-25))
        anchorSim.left = max(0, min(anchorSim.left + e.delta_x,590-25))
        anchorSim.update()
        updateReadings()
    
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
            changes = calculatePhysics(magnetContainer.left,magnetContainer.top,pointers[row][column]["absX"],pointers[row][column]["absY"],magStrength)
            pointers[row][column]["container"].bgcolor = f"white,{changes["opacity"]}"
            pointers[row][column]["container"].rotate = ft.transform.Rotate(changes["angle"]+np.pi)

    # ANCHOR ELEMENTS
    anchorContainer = ft.Container(
        width=25,height=25,bgcolor="#f5e267",
        border_radius=ft.border_radius.all(30),
        border=ft.border.all(3,"#fce865"),
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

    # READING CONTAINERS
    readingMagStrength = ContainerReading(60,230,37,"300mT")
    readingMSComp = ContainerText("Comparison: Ceramic",12,132,60)
    readingXDist = ContainerReading(60,375,10)
    readingYDist = ContainerReading(60,375,33)
    readingRadius = ContainerReading(60,375,56)
    readingBr = ContainerReading(87,495,10)
    readingPullForce = ContainerReading(87,495,43)
    
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
                                ContainerText("Field Meter",18,10,10),
                                ContainerText("Click Then Drag",11,12,30),
                                anchorMenu, # ANCHOR FOR CONTAINER
                                ContainerDivider(121,10),
                                ContainerText("Magnet Strength",18,132,10),
                                ft.Slider( # MAGNET STRENGTH SLIDER
                                    min=300,max=1400,divisions=50,
                                    width=125,
                                    left=112,top=25,
                                    active_color="#ab9dd4", on_change=updateMagStrength
                                ),
                                readingMagStrength, # MAGNET STRENGTH READING
                                readingMSComp,
                                ContainerDivider(300,10),
                                ContainerText("X-Dist:",16,310,10), readingXDist,
                                ContainerText("Y-Dist:",16,310,33), readingYDist,
                                ContainerText("Radius:",16,310,56), readingRadius,
                                ContainerText("B(r):",16,450,10), readingBr,
                                ContainerText("Pull:",16,450,43), readingPullForce
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