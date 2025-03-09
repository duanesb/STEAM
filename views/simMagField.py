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

    # RANGE FOR OPACITY
    minOpacityValue = 1.5
    maxOpacityValue = 50

    # PHYSICS FORMULA (DISTANCE FROM MAGNET TO POINTER, MAGNET STRENGTH, DIRECTION)
    def calculatePhysics(magnetLeft,magnetTop,pointX,pointY,rawMagStrength):
        nonlocal minOpacityValue,maxOpacityValue
        # UNITS
        pfs = 1.25663706e-06
        area = 0.0001
        magCharge = ((rawMagStrength/1000)/pfs)*area

        # CONVERSIONS (40px = 1cm, 1cm = 0.01m, 40px = 0.00025m)
        pixelToMeter = 0.00025
        posMagnetX = (magnetLeft + magnetWidth/2)*pixelToMeter
        posMagnetY = (magnetTop + magnetHeight/2)*pixelToMeter
        posObsX = pointX*pixelToMeter
        posObsY = pointY*pixelToMeter

        # COORDINATES
        coordsObservation = np.array([posObsX,posObsY])
        coordsMagnet = np.array([posMagnetX,posMagnetY])
        coordsNorthPole = np.array([posMagnetX,posMagnetY-(magnetHeight/2)*pixelToMeter])
        coordsSouthPole = np.array([posMagnetX,posMagnetY+(magnetHeight/2)*pixelToMeter])

        # DISTANCE
        distPointerNorth = coordsNorthPole-coordsObservation
        distPointerSouth = coordsSouthPole-coordsObservation

        # RADIUS
        radiusPointerNorth = np.linalg.norm(distPointerNorth)
        radiusPointerSouth = np.linalg.norm(distPointerSouth)

        # MAGNETIC FLUX DENSITY (B)
        bNorth = (pfs/(4*np.pi)) * (magCharge*distPointerNorth/(radiusPointerNorth**3))
        bSouth = -(pfs/(4*np.pi)) * (magCharge*distPointerSouth/(radiusPointerSouth**3))
        bNetCoords = bNorth + bSouth
        bNetRadius = np.linalg.norm(bNetCoords)

        # PULL FORCE
        pullForce = ((bNetRadius**2)*area)/(2*pfs)

        # VISUAL CHANGES
        bNetDirection = np.atan2(bNetCoords[1],bNetCoords[0])
        opacityCheck = np.clip(bNetRadius*1e4,minOpacityValue,maxOpacityValue)
        opacity = 0.1 + 0.9 * ((opacityCheck-minOpacityValue)/(maxOpacityValue-minOpacityValue))

        return {
            "bNetTesla":bNetRadius,
            "pullForceNewton":pullForce,
            "bNetDirection":bNetDirection,
            "opacity":opacity,
            "coordsMeter":{
                "x":posMagnetX-posObsX,
                "y":posMagnetY-posObsY,
                "radius":np.linalg.norm([posMagnetX-posObsX,posMagnetY-posObsY])
            }
        }

    def updateReadings():
        nonlocal magStrength
        information = calculatePhysics(magnetContainer.left,magnetContainer.top,anchorSim.left+12.5,anchorSim.top+12.5,magStrength)
        bNet = information["bNetTesla"]*1e4
        bNet = f"{bNet:.2e}G" if abs(bNet) >= 10000 else f"{bNet:.2f}G"

        pullForce = information["pullForceNewton"]

        if (abs(pullForce) >= 1000 or (abs(pullForce) > 0 and abs(pullForce) < 0.01)):
            pullForce = f"{pullForce:.2e}N"
        else:
            pullForce = f"{pullForce:.2f}N"


        readingXDist.set(f"{abs(information["coordsMeter"]["x"])*100:.1f}cm")
        readingYDist.set(f"{abs(information["coordsMeter"]["y"])*100:.1f}cm")
        readingRadius.set(f"{information["coordsMeter"]["radius"]*100:.1f}cm")
        readingBNet.set(bNet)
        readingPullForce.set(pullForce)


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
                pointers[row][column]["container"].rotate = ft.transform.Rotate(changes["bNetDirection"]+np.pi)
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
        readingBNet.set("N/A")
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
            pointers[row][column]["container"].rotate = ft.transform.Rotate(changes["bNetDirection"]+np.pi)

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
    readingBNet = ContainerReading(87,495,10)
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
                                ContainerText("B(r):",16,450,10), readingBNet,
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