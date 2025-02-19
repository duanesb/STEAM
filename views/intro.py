import flet as ft
from objects import SimulatorButton,ContentContainer, get_asset_path

def Intro_View(router):
    controls = [
        ft.Text("Simulators", size=55, weight="bold"),
        ft.Row(
            controls=[
                SimulatorButton("Ohm's Law", get_asset_path("Ohm-intro.png"), lambda e: router.go('/ohm')),
                SimulatorButton("Magnetic Field", get_asset_path("Magnetic-intro.png"), lambda e: router.go('/magnetic')),
                SimulatorButton("Capacitance", get_asset_path("Capacitance-intro.png"), lambda e: router.go('/capacitance')),
                SimulatorButton("Resistance", get_asset_path("Resistance-intro.png"), lambda e: router.go('/resistance')),
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
