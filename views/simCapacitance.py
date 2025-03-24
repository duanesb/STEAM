import flet as ft
import numpy as np
from objects import BackElevatedButton, ContentContainer, ContainerDivider, ContainerText, ContainerReading

def Capacitance_View(router):
    pointers = []
    rows = 8
    columns = 14
    containerWidth = 22
    containerHeight = 5.5
    plateWidth = 120
    plateHeight = 40
    voltage = 0
    plateSeparation = 0.01
    plateArea = 0.01
    epsilon0 = 8.854e-12
    minOpacityValue = 1.5
    maxOpacityValue = 50

    def calculatePhysics(plateLeft, plateTop, pointX, pointY, voltage):
        nonlocal minOpacityValue, maxOpacityValue
        pixelToMeter = 0.00025
        posPlateX = (plateLeft + plateWidth / 2) * pixelToMeter
        posPlateY = (plateTop + plateHeight / 2) * pixelToMeter
        posObsX = pointX * pixelToMeter
        posObsY = pointY * pixelToMeter

        coordsObservation = np.array([posObsX, posObsY])
        coordsPlate = np.array([posPlateX, posPlateY])

        distPointerPlate = coordsPlate - coordsObservation

        radiusPointerPlate = np.linalg.norm(distPointerPlate)

        electricField = voltage / radiusPointerPlate

        electricFieldDirection = np.atan2(distPointerPlate[1], distPointerPlate[0])
        opacityCheck = np.clip(electricField * 1e4, minOpacityValue, maxOpacityValue)
        opacity = 0.1 + 0.9 * ((opacityCheck - minOpacityValue) / (maxOpacityValue - minOpacityValue))

        return {
            "electricField": electricField,
            "electricFieldDirection": electricFieldDirection,
            "opacity": opacity,
            "coordsMeter": {
                "x": -(posPlateX - posObsX),
                "y": posPlateY - posObsY,
                "radius": np.linalg.norm([posPlateX - posObsX, posPlateY - posObsY])
            }
        }

    def calculateCapacitance():
        nonlocal plateSeparation, plateArea, epsilon0
        return (epsilon0 * plateArea) / plateSeparation

    def calculateTopPlateCharge():
        nonlocal voltage
        capacitance = calculateCapacitance()
        return capacitance * voltage

    def calculateStoredEnergy():
        nonlocal voltage
        capacitance = calculateCapacitance()
        return 0.5 * capacitance * (voltage ** 2)

    def updateElectricFieldLines():
        field_lines = []
        
        if voltage != 0 and plateSeparation >= 2.02:
            num_lines = max(3, int(plateContainer.width / 20))
            
            top_plate_bottom = plateContainer.top + plateHeight
            bottom_plate_top = secondPlateContainer.top
            field_height = abs(bottom_plate_top - top_plate_bottom)
            
            arrow_count = max(3, int(field_height / 25))
            arrow_size = 12
            arrow_color = "#ff3333" if voltage > 0 else "#3333ff"
            
            spacing = plateContainer.width / (num_lines - 1) if num_lines > 1 else 0
            
            for i in range(num_lines):
                x_pos = plateContainer.left + (i * spacing)
                
                field_line = ft.Container(
                    width=1.5,
                    height=field_height,
                    left=x_pos,
                    top=top_plate_bottom,
                    bgcolor=arrow_color,
                    opacity=0.8,
                    border_radius=ft.border_radius.all(1)
                )
                field_lines.append(field_line)
                
                for j in range(1, arrow_count):
                    arrow_y = top_plate_bottom + j * (field_height/arrow_count)
                    
                    arrow = ft.Container(
                        width=arrow_size,
                        height=arrow_size,
                        left=x_pos - arrow_size/2 + 0.75,
                        top=arrow_y - arrow_size/2,
                        content=ft.Icon(
                            name=ft.icons.ARROW_DROP_DOWN if voltage > 0 else ft.icons.ARROW_DROP_UP,
                            color=arrow_color,
                            size=arrow_size,
                            opacity=0.9
                        )
                    )
                    field_lines.append(arrow)
        
        return field_lines

    def updateReadings():
        nonlocal voltage
        capacitance = calculateCapacitance()
        topPlateCharge = calculateTopPlateCharge()
        storedEnergy = calculateStoredEnergy()
        
        readingCapacitance.set(f"{capacitance:.2e}F")
        readingTopPlateCharge.set(f"{topPlateCharge:.2e}C")
        readingStoredEnergy.set(f"{storedEnergy:.2e}J")

    def updateVoltage(e):
        nonlocal voltage
        slider_value = int(e.control.value)
        voltage = -1.5 + (slider_value * (3.0 / 20))
        readingVoltage.set(f"{voltage:.2f}V")
        updateReadings()
        updateMainStack()

    def updatePlateSeparation(e):
        nonlocal plateSeparation
        plateSeparation = float(e.control.value)
        readingPlateSeparation.set(f"{plateSeparation:.2f}mm")
        centerY = 200
        plateContainer.top = centerY - (plateSeparation * 20) / 2
        secondPlateContainer.top = centerY + (plateSeparation * 20) / 2
        plateContainer.update()
        secondPlateContainer.update()
        updateReadings()
        updateMainStack()

    def updatePlateArea(e):
        nonlocal plateArea
        plateArea = float(e.control.value)
        readingPlateArea.set(f"{plateArea:.2f}mm²")
        initialArea = 100
        scalingFactor = np.sqrt(plateArea / initialArea)
        newWidth = max(60, min(300, plateWidth * scalingFactor))
        plateContainer.width = newWidth
        secondPlateContainer.width = newWidth
        plateContainer.left = 300 - newWidth / 2
        secondPlateContainer.left = 300 - newWidth / 2
        plateContainer.update()
        secondPlateContainer.update()
        updateReadings()
        updateMainStack()

    def updateMainStack():
        main_stack.controls = [
            *[pointers[row][column]["container"] for row in range(rows) for column in range(columns)],
            plateContainer,
            secondPlateContainer,
            *updateElectricFieldLines(),
            anchorSim
        ]
        main_stack.update()

    plateContainer = ft.Container(
        width=plateWidth,
        height=plateHeight,
        left=300 - plateWidth / 2,
        top=260 - plateHeight / 2 - (plateSeparation * 100 * 20) / 2,
        border=ft.border.all(5, "black"),
        bgcolor="grey"
    )

    secondPlateContainer = ft.Container(
        width=plateWidth,
        height=plateHeight,
        left=300 - plateWidth / 2,
        top=200 - plateHeight / 2 + (plateSeparation * 100 * 20) / 2,
        border=ft.border.all(5, "black"),
        bgcolor="grey"
    )

    # Create pointers
    for row in range(rows):
        pointers.append([])
        for column in range(columns):
            x = 40 + 38 * column
            y = 40 + 45 * row
            container = ft.Container(
                width=containerWidth, height=containerHeight,
                bgcolor="white", left=x, top=y
            )
            pointers[row].append({"container": container, "absX": x + containerWidth / 2, "absY": y + containerHeight / 2})
            changes = calculatePhysics(plateContainer.left, plateContainer.top, pointers[row][column]["absX"], pointers[row][column]["absY"], voltage)
            pointers[row][column]["container"].bgcolor = f"white,{changes['opacity']}"
            pointers[row][column]["container"].rotate = ft.transform.Rotate(changes["electricFieldDirection"] + np.pi)

    anchorContainer = ft.Container(
        width=25, height=25, bgcolor="#f5e267",
        border_radius=ft.border_radius.all(30),
        border=ft.border.all(3, "#fce865"),
    )
    anchorSim = ft.GestureDetector(
        visible=False,
        left=10, top=10,
        content=anchorContainer,
        drag_interval=10,
    )

    # Main stack
    main_stack = ft.Stack(
        controls=[
            *[pointers[row][column]["container"] for row in range(rows) for column in range(columns)],
            plateContainer,
            secondPlateContainer,
            *updateElectricFieldLines(),
            anchorSim
        ]
    )

    # Reading containers
    readingVoltage = ContainerReading(60, 90, 20, "0.00V")
    readingPlateSeparation = ContainerReading(60, 90, 55, "1.00mm")
    readingPlateArea = ContainerReading(60, 230, 20, "100.00mm²")
    readingCapacitance = ContainerReading(60, 470, 10)
    readingTopPlateCharge = ContainerReading(60, 470, 33)
    readingStoredEnergy = ContainerReading(60, 470, 56)

    controls = [
        ft.Text("Capacitance Simulator", size=55, weight="bold"),
        ft.Container(
            width=600, height=500, bgcolor="white", border=ft.border.all(5, "#201b2e"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=600, height=400, bgcolor="black", margin=0, padding=0,
                        content=main_stack
                    ),
                    ft.Container(width=600, height=90, bgcolor="#706394", border=ft.border.only(top=ft.BorderSide(5, "black")),
                        content=ft.Stack(
                            controls=[
                                ContainerText("Voltage", 9, 8, 10),
                                ft.Slider(
                                    min=0, 
                                    max=20,
                                    value=10,
                                    width=100,
                                    left=-7, 
                                    top=11,
                                    active_color="#ab9dd4", 
                                    on_change=updateVoltage
                                ),
                                readingVoltage,

                                ContainerText("Plate Separation", 9, 8, 45),
                                ft.Slider(
                                    min=1, max=20,
                                    width=100,
                                    left=-7, top=48,
                                    active_color="#ab9dd4", on_change=updatePlateSeparation
                                ),
                                readingPlateSeparation,
                                ContainerText("Plate Area", 9, 160, 10),
                                ft.Slider(
                                    min=100, max=1000,
                                    width=100,
                                    left=145, top=11,
                                    active_color="#ab9dd4", on_change=updatePlateArea
                                ),
                                readingPlateArea,
                                ContainerDivider(300, 10),
                                ContainerText("Capacitance:", 16, 310, 10), readingCapacitance,
                                ContainerText("Top Plate Charge:", 16, 310, 33), readingTopPlateCharge,
                                ContainerText("Stored Energy:", 16, 310, 56), readingStoredEnergy,
                            ]
                        )
                    )
                ],
                spacing=0
            )
        ),
        ft.Row(
            controls=[
                ft.Container(width=200),
                BackElevatedButton("Back", lambda e: router.go('/intro')),
                ft.Text("Move the sliders to see what happens.", width=200, size=11)
            ],
            width=600,
            alignment=ft.MainAxisAlignment.CENTER
        )
    ]
    content = ContentContainer(controls)
    return content