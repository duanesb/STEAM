import flet as ft
from objects import SimulatorButton

def Intro_View(router):
    content = ft.Container(
        content= ft.Column(
            controls=[
                ft.Text("Simulators", size=55, weight="bold"),
                ft.Row(
                    controls=[
                        SimulatorButton("Ohm's Law","Ohm-intro.png",lambda e:router.go('/ohm')),
                        SimulatorButton("Magnetic Field","Magnetic-intro.png",lambda e:router.go('/magnetic')),
                        SimulatorButton("Capacitance","Capacitance-intro.png",lambda e:router.go('/capacitance')),
                        SimulatorButton("Resistance","Resistance-intro.png",lambda e:router.go('/resistance'))
                    ],
                    width=700,
                    wrap=True,
                    spacing=30,
                    run_spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=30,
            alignment= ft.MainAxisAlignment.START,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
        width=800,
        height=800,
        padding=ft.padding.only(top=20)
    )
    return content
