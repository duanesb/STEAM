import flet as ft
from objects import SimulatorButton,ContentContainer


def Intro_View(router):
    controls = [
        ft.Text("Simulators", size=55, weight="bold"),
        ft.Row(
            controls=[
                SimulatorButton("Ohm's Law","ohmsLaw.png",lambda e:router.go('/ohm')),
                SimulatorButton("Magnetic Field","magneticField.png",lambda e:router.go('/magnetic')),
                SimulatorButton("Capacitance","capacitance.png",lambda e:router.go('/capacitance')),
                SimulatorButton("Resistance","resistors.png",lambda e:router.go('/resistance'))
            ],
            width=700,
            wrap=True,
            spacing=30,
            run_spacing=30,
            alignment=ft.MainAxisAlignment.CENTER
        )
    ]

    content = ContentContainer(controls)
    return content
