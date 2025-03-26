import flet as ft
from objects import BackElevatedButton,ContentContainer
import asyncio
import random

def Ohm_View(router):

    top_formula = 0
    left_formula = 200

    volts = 0.1
    resistance = 10
    current = 10

    voltage_text = ft.Text(
        f"{volts}V",size=22,weight="bold",color="white",
        left=475,top=40,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    resistance_text = ft.Text(
        f"{resistance}Ω",size=22,weight="bold",color="white",
        left=475,top=5,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    current_text = ft.Text(
        f"{current}mA",size=22,weight="bold",color="white",
        left=475,top=40,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
        visible=False
    )

    answer_text = ft.Text(
        f"Current: {current}mA",size=30,weight="bold",color="black",
        left=190,top=230,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
    )

    white_background = ft.Container(bgcolor="white", opacity=0.9, width=800, height=800, visible=False, top=0, left=0)

    ohm_info = ft.Container(
        content=ft.Icon(name=ft.Icons.INFO_OUTLINE, tooltip="Ohm’s Law defines the relationship between three fundamental electrical properties: voltage, current, and resistance. Voltage is the potential difference that pushes electric charges through a conductor, driving the flow of current. Current refers to the flow of electric charge, which is measured in amperes (A). Resistance is the property of a material that resists the flow of electric current, measured in ohms (Ω). The law states that the voltage across a conductor is directly proportional to the current passing through it and inversely proportional to its resistance. Understanding this relationship allows us to predict how electrical circuits will behave under different conditions and is fundamental to the design and analysis of electronic systems.", size=30, color="#ffae17"),
        left=565,
        top=5,
    )

    def checkelecctronamount():
        nonlocal current
        if current >= 225:
            electron2.visible = True
        else:
            electron2.visible = False
        
        if current >= 550:
            electron3.visible = True
        else:
            electron3.visible = False
        
        if current >= 775:
            electron4.visible = True
        else:
            electron4.visible = False

        if current >= 900:
            electron5.visible = True
        else:
            electron5.visible = False
    
    resistor_storage = ft.Stack()
    
    def add_resistance():
        nonlocal resistance
        resistor_storage.controls.clear()
        num_circles_needed = int(resistance / 20)

        for _ in range(num_circles_needed):
            new_circle = ft.Container(
                width=10,
                height=10,
                bgcolor=ft.Colors.BLACK,
                border_radius=10,
                top=random.randint(0, 45),
                left=random.randint(0,180),
            )
            resistor_storage.controls.append(new_circle)
        router.update()


    def updateVolt(e):
        nonlocal volts, resistance, current
        volts = round(e.control.value, 1)
        voltage_text.value = f"{volts}V"
        voltage_text.update()
        start_movement(volts)
        if current_slider.visible:
            resistance = round(volts / (current / 1000))

            answer_text.value = f"Resistance: {resistance}Ω"

            if resistance < 10:
                resistance = 10
            elif resistance > 900:
                resistance = 900
                
            resistance_text.value = f"{resistance}Ω"
            resistance_slider.content.value = resistance
            resistance_slider.content.update()
            add_resistance()
        else:
            current = round((volts / resistance) * 1000,1)

            answer_text.value = f"Current: {current}mA"

            if current < 0.1:
                current = 0.1
            elif current > 900:
                current = 900

            current_text.value = f"{current}mA"
            current_slider.content.value = current
            current_slider.content.update()
            checkelecctronamount()

    
    def updateResistance(e):
        nonlocal resistance, volts, current
        resistance = round(e.control.value)
        resistance_text.value = f"{resistance}Ω"
        resistance_text.update()

        add_resistance()

        if current_slider.visible:
            volts = round(resistance * (current / 1000), 1)

            answer_text.value = f"Voltage: {volts}V"

            if volts < 0.1:
                volts = 0.1
            elif volts > 9:
                volts = 9

            voltage_text.value = f"{volts}V"
            volt_slider.content.value = volts
            volt_slider.content.update()
            start_movement(volts)
        else:
            current = round((volts / resistance) * 1000,1)

            answer_text.value = f"Current: {current}mA"

            if current < 0.1:
                current = 0.1
            elif current > 900:
                current = 900

            current_text.value = f"{current}mA"
            current_slider.content.value = current
            current_slider.content.update()
            checkelecctronamount()


    
    def updateCurrent(e):
        nonlocal current, resistance, volts
        current = round(e.control.value, 1)

        current_text.value = f"{current}mA"
        current_text.update()
        checkelecctronamount()

        if current_slider.top == 3:
            resistance = round(volts / (current / 1000))
            
            answer_text.value = f"Resistance: {resistance}Ω"

            if resistance < 10:
                resistance = 10
            elif resistance > 900:
                resistance = 900

            resistance_text.value = f"{resistance}Ω"
            resistance_slider.content.value = resistance
            resistance_slider.content.update()
            add_resistance()
        else:
            volts = round(resistance * (current / 1000), 1)

            answer_text.value = f"Voltage: {volts}V"

            if volts < 0.1:
                volts = 0.1
            elif volts > 9:
                volts = 9

            voltage_text.value = f"{volts}V"
            volt_slider.content.value = volts
            volt_slider.content.update()
            checkelecctronamount()
            start_movement(volts)

    def switch_v(e):
        nonlocal volts
        v_text.content.color = "#ffae17"
        i_text.content.color = r_text.content.color = "#ab9dd4"
        volt_slider.visible = voltage_text.visible = False
        resistance_slider.visible = current_slider.visible = resistance_text.visible = current_text.visible = True
        current_slider.top = 35
        slider_text.value = ("Resistance: Current:")
        current_text.top = 40
        answer_text.value = f"Voltage: {volts}V"
        router.update()

    def switch_i(e):
        nonlocal current
        v_text.content.color = r_text.content.color = "#ab9dd4"
        i_text.content.color = "#ffae17"
        volt_slider.visible = resistance_slider.visible = voltage_text.visible = resistance_text.visible = True
        current_slider.visible = current_text.visible = False
        slider_text.value = ("Resistance: Voltage:")
        answer_text.value = f"Current: {current}mA"
        router.update()

    def switch_r(e):
        nonlocal resistance
        v_text.content.color = i_text.content.color = "#ab9dd4"
        r_text.content.color = "#ffae17"
        volt_slider.visible = current_slider.visible = voltage_text.visible = current_text.visible = True
        resistance_slider.visible = resistance_text.visible = False
        current_slider.top = 3
        slider_text.value = ("Current: Voltage:")
        current_text.top = 5
        answer_text.value = f"Resistance: {resistance}Ω"
        router.update()
    
    def open_calculator(e):
        white_background.visible = True
        router.update()

    volt_slider = ft.Container(content=ft.Slider(min=0.1, max=9,value=0.1 ,width=275, divisions=89, label="{value}V", round=2, active_color="#ab9dd4", on_change=updateVolt),bgcolor="transparent",top=35, left=210)
    resistance_slider = ft.Container(content=ft.Slider(min=10, max=1000, value=10, width=275, divisions=990, label="{value}Ω", round=1, active_color="#ab9dd4", on_change=updateResistance),bgcolor="transparent",top=3, left=210)
    current_slider = ft.Container(content=ft.Slider(min=0.1, max=900.0, value=10,width=275, divisions=8999, label="{value}mA", round=1, active_color="#ab9dd4", on_change=updateCurrent),bgcolor="transparent",top=3, left=210, visible=False)

    slider_text = ft.Text("Resistance: Voltage:",weight="bold",size=22, color="black",width=135,left=85,top=11)

    calculator_button = ft.IconButton(
            icon=ft.Icons.CALCULATE,
            selected=False,
            icon_size=70,
            style=ft.ButtonStyle(color="#ab9dd4"),
            on_click=open_calculator,
        )
    
    v_text = ft.Container(content=ft.Text("V", color="#ab9dd4", size=80, weight="bold"), on_click=switch_v, left=left_formula, top=top_formula)
    i_text = ft.Container(content=ft.Text("I", color="#ffae17", size=80, weight="bold"), left=110+left_formula, on_click=switch_i, top=top_formula)
    r_text = ft.Container(content=ft.Text("R", color="#ab9dd4", size=80, weight="bold"), left=140+left_formula, on_click=switch_r, top=top_formula)

    cable = ft.Container(
        padding=10,
        border=ft.border.all(2, "black"),
        width=400,
        height=200,
        bgcolor=None,
        top=160,
        left=100,
    )

    electron_path = [(290, 150), (490, 150), (490, 350), (90, 350), (90, 150)]

    electron = ft.Container(
        width=20,
        height=20,
        bgcolor=ft.Colors.BLUE,
        border_radius=10,
        top=electron_path[0][1],
        left=290,
        animate_position=500
    )

    electron2 = ft.Container(
        width=20,
        height=20,
        bgcolor=ft.Colors.BLUE,
        border_radius=10,
        top=electron_path[0][1],
        left=290,
        animate_position=500,
        visible=False
    )

    electron3 = ft.Container(
        width=20,
        height=20,
        bgcolor=ft.Colors.BLUE,
        border_radius=10,
        top=electron_path[0][1],
        left=290,
        animate_position=500,
        visible=False
    )

    electron4 = ft.Container(
        width=20,
        height=20,
        bgcolor=ft.Colors.BLUE,
        border_radius=10,
        top=electron_path[0][1],
        left=290,
        animate_position=500,
        visible=False
    )

    electron5 = ft.Container(
        width=20,
        height=20,
        bgcolor=ft.Colors.BLUE,
        border_radius=10,
        top=electron_path[0][1],
        left=290,
        animate_position=500,
        visible=False
    )

    battery = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("-", color="white", size=40),
                width=100,
                height=65,
                bgcolor="#706394",
                alignment=ft.alignment.top_left,
            ),
            ft.Container(
                content=ft.Text("+", color="white", size=40),
                width=100,
                height=65,
                bgcolor="#706394",
                alignment=ft.alignment.top_right
            )
        ], top=128, left=200, spacing=0
    )

    resistor = ft.Container(
        content=resistor_storage,
        top=325, 
        left=200, 
        width=200,
        height=65,
        bgcolor="transparent",
        border=ft.border.all(3,"#201b2e"),
        border_radius=10,
    )

    current_task = None

    async def move_electron(speed):
        electrons = [electron, electron2, electron3, electron4, electron5]
        positions = [electron_path[0]] * len(electrons)
        while True:
            for pos in electron_path:
                positions.insert(0, pos)
                positions.pop()
                for i, e in enumerate(electrons):
                    e.left, e.top = positions[i]
                    e.animate_position = int(2000 / (speed / 0.9))
                router.update()
                await asyncio.sleep(2 / (speed / 0.9))


    def start_movement(speed):
        nonlocal current_task
        if current_task:
            current_task.cancel()
        current_task = router.run_task(move_electron, speed)

    start_movement(volts)

    controls = [
        ft.Text("Ohm's Law", size=55, weight="bold"),
        ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    width=600, height=500, bgcolor="white", border=ft.border.all(5, "#201b2e"),
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                width=600, height=400, bgcolor="#faffe2", margin=0, padding=0,
                                                content=ft.Stack(
                                                    controls=[
                                                        v_text,
                                                        ft.Text("=", color="#ab9dd4", size=80, weight="bold", left=55+left_formula),
                                                        i_text,
                                                        r_text,
                                                        cable,
                                                        resistor,
                                                        electron,
                                                        electron2,
                                                        electron3,
                                                        electron4,
                                                        electron5,
                                                        battery,
                                                        answer_text,
                                                    ]
                                                )
                                            ),
                                            ft.Container(
                                                width=600, height=90, bgcolor="#706394",
                                                border=ft.border.only(top=ft.BorderSide(5, "black")),
                                                content=ft.Stack(
                                                    controls=[
                                                        slider_text,
                                                        resistance_slider,
                                                        volt_slider,
                                                        current_slider,
                                                        voltage_text,
                                                        resistance_text,
                                                        current_text,
                                                        # calculator_button,
                                                    ]
                                                )
                                            ),
                                        ],
                                        spacing=0
                                    ),
                                )
                            ]
                        )
                    ),
                    white_background,
                    ohm_info,

                ]
            )
        ),
        BackElevatedButton("Back", lambda e: router.go('/intro'))
    ]

    content = ContentContainer(controls)
    return content