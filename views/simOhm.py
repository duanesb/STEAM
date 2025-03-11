import flet as ft
from objects import BackElevatedButton,ContentContainer
import asyncio

def Ohm_View(router):

    top_formula = 0
    left_formula = 200

    volts = 0.1
    resistance = 10
    current = 10

    voltage_text = ft.Text(
        "0.1V",size=22,weight="bold",color="white",
        left=475,top=40,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    resistance_text = ft.Text(
        "10Ω",size=22,weight="bold",color="white",
        left=475,top=5,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    current_text = ft.Text(
        "10.0mA",size=22,weight="bold",color="white",
        left=475,top=40,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
        visible=False
    )

    white_background = ft.Container(bgcolor="white", opacity=0.9, width=800, height=800, visible=False)

    def updateVolt(e):
        nonlocal volts, resistance, current
        volts = round(e.control.value,2)
        voltage_text.value = f"{volts}V"
        voltage_text.update()
        if current_slider.visible == True:
            resistance = volts/current
            resistance_text.value = f"{resistance}Ω"
        else:
            current = (volts/resistance)*1000
            current_text.value = f"{current}mA"

        start_movement(current)

    def updateResistance(e):
        nonlocal resistance, volts, current
        resistance = int(e.control.value)
        resistance_text.value = f"{resistance}Ω"
        resistance_text.update()
        if current_slider.visible == True:
            volts = resistance*current
            voltage_text.value = f"{volts}V"
        else:
            current = (volts/resistance)*1000
            current_text.value = f"{current}mA"
        start_movement(current)
    
    def updateCurrent(e):
        nonlocal current, resistance, volts
        current = round(e.control.value, 2)
        current_text.value = f"{current}mA"
        current_text.update()
        if current_slider.top == 3:
            resistance = volts/current
            resistance_text.value = f"{resistance}Ω"
        else:
            volts = resistance*current
            voltage_text.value = f"{volts}V"
        start_movement(current)
    
    
    def switch_v(e):
        v_text.content.color = "#ffae17"
        i_text.content.color = r_text.content.color = "#ab9dd4"
        volt_slider.visible = voltage_text.visible = False
        resistance_slider.visible = current_slider.visible = resistance_text.visible = current_text.visible = True
        current_slider.top = 35
        slider_text.value = ("Resistance: Current:")
        current_text.top = 40
        router.update()

    def switch_i(e):
        v_text.content.color = r_text.content.color = "#ab9dd4"
        i_text.content.color = "#ffae17"
        volt_slider.visible = resistance_slider.visible = voltage_text.visible = resistance_text.visible = True
        current_slider.visible = current_text.visible = False
        slider_text.value = ("Resistance: Voltage:")
        router.update()

    def switch_r(e):
        v_text.content.color = i_text.content.color = "#ab9dd4"
        r_text.content.color = "#ffae17"
        volt_slider.visible = current_slider.visible = voltage_text.visible = current_text.visible = True
        resistance_slider.visible = resistance_text.visible = False
        current_slider.top = 3
        slider_text.value = ("Current: Voltage:")

        current_text.top = 5
        router.update()
    
    def open_calculator(e):
        white_background.visible = True
        router.update()

    volt_slider = ft.Container(content=ft.Slider(min=0.1, max=9,width=275, divisions=89, label="{value}V", round=2, active_color="#ab9dd4", on_change=updateVolt),bgcolor="transparent",top=35, left=210)
    resistance_slider = ft.Container(content=ft.Slider(min=10, max=100,width=275, divisions=89, label="{value}Ω", active_color="#ab9dd4", on_change=updateResistance),bgcolor="transparent",top=3, left=210)
    current_slider = ft.Container(content=ft.Slider(min=10, max=900,width=275, divisions=890, label="{value}mA", round=1, active_color="#ab9dd4", on_change=updateCurrent),bgcolor="transparent",top=3, left=210, visible=False)

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
        top=180,
        left=100,
    )

    electron_path = [(290, 170), (490, 170), (490, 370), (90, 370), (90, 170)]

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
        left=electron_path[0][0],
        animate_position=500
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
        ], top=148, left=200, spacing=0
    )


    current_task = None

    async def move_electron(speed):
        while True:
            for x, y in electron_path:
                electron.left = x
                electron.top = y
                router.update()
                electron.animate_position = int(2000/(speed/100))
                print(2/(speed/100))
                await asyncio.sleep(2/(speed/100))


    def start_movement(speed):
        nonlocal current_task
        if current_task:
            current_task.cancel()
        current_task = router.run_task(move_electron, speed)

    
    start_movement(current)


    controls = [
        ft.Container(
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Ohm's Law", size=55, weight="bold"),
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
                                                        electron,
                                                        battery
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
                                                        calculator_button,
                                                    ]
                                                )
                                            ),
                                        ],
                                        spacing=0
                                    ),
                                ),
                                BackElevatedButton("Back", lambda e: router.go('/intro'))
                            ]
                        )
                    ),
                    white_background,
                ]
            )
        )
    ]

    content = ContentContainer(controls)
    return content