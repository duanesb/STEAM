import flet as ft
from objects import BackElevatedButton,ContentContainer

def Ohm_View(router):

    top_formula = 0
    left_formula = 0

    volts = 0
    resistance = 10
    current = 0

    volt_text = ft.Text(
        "0.1V",size=22,weight="bold",color="white",
        left=520,top=40,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    resistance_text = ft.Text(
        "10Ω",size=22,weight="bold",color="white",
        left=520,top=5,
        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
    )

    def updateVolt(e):
        nonlocal volts
        volts = round(e.control.value,2)
        volt_text.value = f"{volts}V"
        volt_text.update()

    def updateResistance(e):
        nonlocal resistance
        resistance = int(e.control.value)
        resistance_text.value = f"{resistance}Ω"
        resistance_text.update()
    
    def updateCurrent(e):
        nonlocal current
        current = round(e.control.value, 2)
        resistance_text.value = f"{current}mA"
        resistance_text.update()
    
    
    def switch_v(e):
        v_text.content.color = "#ffae17"
        i_text.content.color = "#ab9dd4"
        r_text.content.color = "#ab9dd4"
        volt_slider.visible = False
        resistance_slider.visible = True
        current_slider.visible = True
        current_slider.top = 35
        slider_text.value = ("Resistance: Current:")

        
        router.update()

    def switch_i(e):
        v_text.content.color = "#ab9dd4"
        i_text.content.color = "#ffae17"
        r_text.content.color = "#ab9dd4"
        volt_slider.visible = True
        resistance_slider.visible = True
        current_slider.visible = False
        slider_text.value = ("Resistance: Voltage:")


        router.update()

    def switch_r(e):
        v_text.content.color = "#ab9dd4"
        i_text.content.color = "#ab9dd4"
        r_text.content.color = "#ffae17"
        volt_slider.visible = True
        resistance_slider.visible = False
        current_slider.visible = True
        current_slider.top = 3
        slider_text.value = ("Current: Voltage:")

        
        router.update()

    volt_slider = ft.Container(content=ft.Slider(min=0.1, max=9,width=300, divisions=89, label="{value}V", round=2, active_color="#ab9dd4", on_change=updateVolt),bgcolor="transparent",top=35, left=230)
    resistance_slider = ft.Container(content=ft.Slider(min=10, max=100,width=300, divisions=89, label="{value}Ω", active_color="#ab9dd4", on_change=updateResistance),bgcolor="transparent",top=3, left=230)
    current_slider = ft.Container(content=ft.Slider(min=10, max=900,width=300, divisions=890, label="{value}mA", round=1, active_color="#ab9dd4", on_change=updateCurrent),bgcolor="transparent",top=3, left=230, visible=False)

    slider_text = ft.Text("Resistance: Voltage:",weight="bold",size=22, color="black",width=135,left=100,top=11)

    calculator_button = ft.IconButton(
            icon=ft.Icons.CALCULATE,
            selected=False,
            icon_size=70,
            style=ft.ButtonStyle(color="#ab9dd4"),
        )
    
    v_text = ft.Container(content=ft.Text("V", color="#ab9dd4", size=80, weight="bold"), on_click=switch_v, left=left_formula, top=top_formula)
    i_text = ft.Container(content=ft.Text("I", color="#ffae17", size=80, weight="bold"), left=110+left_formula, on_click=switch_i, top=top_formula)
    r_text = ft.Container(content=ft.Text("R", color="#ab9dd4", size=80, weight="bold"), left=140+left_formula, on_click=switch_r, top=top_formula)

    controls = [
        ft.Text("Ohm's Law", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e"),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=600,height=400,bgcolor="#faffe2", margin=0,padding=0,
                        content=ft.Stack(
                            controls=[
                                v_text,
                                ft.Text("=", color="#ab9dd4", size=80, weight="bold", left=55),
                                i_text,
                                r_text,
                            ],
                        )
                    ),
                    ft.Container(width=600,height=90,bgcolor="#706394",border=ft.border.only(top=ft.BorderSide(5,"black")),
                        content=ft.Stack(
                            controls=[
                                slider_text,
                                resistance_slider,
                                volt_slider,
                                current_slider,
                                volt_text,
                                resistance_text,
                                calculator_button,
                            ]
                        )
                    ),
                ],
                spacing=0
            ),
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content