import flet as ft
from objects import BackElevatedButton,ContentContainer

def Ohm_View(router):
    volt_slider = ft.Container(content=ft.Slider(min=0.1, max=9,width=335, divisions=89, label="{value}V", round=2),bgcolor="transparent",top=12)
    resistance_slider = ft.Container(content=ft.Slider(min=10, max=100,width=335, divisions=89, label="{value}Omega"),bgcolor="transparent",top=22)

    controls = [
        ft.Text("Ohm's Law", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e"),
            content=ft.Stack(
                controls=[
                    volt_slider,
                    resistance_slider,
                ],
            ),
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content