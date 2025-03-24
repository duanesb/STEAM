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
        voltage = int(e.control.value)
        readingVoltage.set(f"{voltage}V")
        updateReadings()

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

    def updatePlateArea(e):
        nonlocal plateArea
        plateArea = float(e.control.value)
        readingPlateArea.set(f"{plateArea:.2f}mm²")
        initialArea = 100
        scalingFactor = np.sqrt(plateArea / initialArea)
        newWidth = plateWidth * scalingFactor
        newHeight = plateHeight * scalingFactor
        plateContainer.width = newWidth
        plateContainer.height = newHeight
        secondPlateContainer.width = newWidth
        secondPlateContainer.height = newHeight
        plateContainer.left = 300 - newWidth / 2
        secondPlateContainer.left = 300 - newWidth / 2
        plateContainer.update()
        secondPlateContainer.update()
        updateReadings()

    def textFieldChange(e, left=None, top=None):
        pass

    plateContainer = ft.Container(
        width=plateWidth,
        height=plateHeight,
        left=300 - plateWidth / 2,
        top=260 - plateHeight / 2 - (plateSeparation * 100 * 20) / 2,  # Initial position
        border=ft.border.all(5, "black"),
        bgcolor="grey"
    )

    secondPlateContainer = ft.Container(
        width=plateWidth,
        height=plateHeight,
        left=300 - plateWidth / 2,
        top=200 - plateHeight / 2 + (plateSeparation * 100 * 20) / 2,  # Initial position
        border=ft.border.all(5, "black"),
        bgcolor="grey"
    )

    # CREATES POINTERS
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

    # ANCHOR ELEMENTS
    anchorContainer = ft.Container(
        width=25, height=25, bgcolor="#f5e267",
        border_radius=ft.border_radius.all(30),
        border=ft.border.all(3, "#fce865"),
    )
    anchorMenu = ft.Container(
        content=anchorContainer,
        left=45, top=50,
    )
    anchorSim = ft.GestureDetector(
        visible=False,
        left=10, top=10,
        content=anchorContainer,
        drag_interval=10,
    )

    # READING CONTAINERS
    readingVoltage = ContainerReading(60, 90, 20, "0V")
    readingPlateSeparation = ContainerReading(60, 90, 55, "1.00mm")
    readingPlateArea = ContainerReading(60, 230, 20, "100.00mm²")
    readingCapacitance = ContainerReading(60, 470, 10)
    readingTopPlateCharge = ContainerReading(60, 470, 33)
    readingStoredEnergy = ContainerReading(60, 470, 56)
    readingElectricField = ContainerReading(87, 495, 10)

    controls = [
        ft.Text("Capacitance Simulator", size=55, weight="bold"),
        ft.Container(
            width=600, height=500, bgcolor="white", border=ft.border.all(5, "#201b2e"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=600, height=400, bgcolor="black", margin=0, padding=0,
                        content=ft.Stack(
                            controls=[
                                *[pointers[row][column]["container"] for row in range(rows) for column in range(columns)],
                                plateContainer,
                                secondPlateContainer,
                                anchorSim
                            ]
                        )
                    ),
                    ft.Container(width=600, height=90, bgcolor="#706394", border=ft.border.only(top=ft.BorderSide(5, "black")),
                        content=ft.Stack(
                            controls=[

                                ContainerText("Voltage", 9, 8, 10),
                                ft.Slider(
                                    min=1, max=20,
                                    width=100,
                                    left=-7, top=11,
                                    active_color="#ab9dd4", on_change=updateVoltage
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