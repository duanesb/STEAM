import flet as ft
from objects import SimulatorButton

def Intro_View(router):
    content2 = ft.Container(
        content= ft.Column(
            controls=[
                ft.Text("Simulators", size=55, weight="bold"),
                ft.Row(
                    controls=[
                        SimulatorButton("Ohm's Law","ohmsLaw.png",lambda e:router.go('/ohm')),
                        SimulatorButton("Magnetic Field","magneticField.png",lambda e:router.go('/magnetic')),
                        SimulatorButton("Capacitance","capacitance.png",lambda e:router.go('/capacitance')),
                        SimulatorButton("Resistance","resistors.png",lambda e:router.go('/resistance'))
                    ],
                    width=600,
                    wrap=True,
                    spacing=100,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=25,
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#d9d9d9",
        width=800,
        height=800,
        padding=0
    )
    content = ft.Container(
        content=ft.Column(spacing=25,controls=[
            ft.Row(controls=[ft.Text("Simulators", size=35, weight="bold")],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/ohm'), content=ft.Column(controls=[
                        ft.Text("Ohm's Law", size=30, weight="bold"),
                        ft.Image(src="Ohm-intro.png", width=200, height=200, fit="contain"),
                ],alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(on_click=lambda _: router.go('/capacitance'), content=ft.Column(controls=[
                        ft.Text("Capacitance", size=30, weight="bold"),
                        ft.Image(src="Capacitance-intro.png", width=200, height=200, fit="contain"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ]),

                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/magnetic'), content=ft.Column(controls=[
                        ft.Text("Magnetic Field", size=30, weight="bold"),
                        ft.Image(src="Magnetic-intro.png", width=200, height=200, fit="contain"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(on_click=lambda _: router.go('/resistance'), content=ft.Column(controls=[
                        ft.Text("Resistance", size=30, weight="bold"),
                        ft.Image(src="Resistance-intro.png", width=200, height=200, fit="contain"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ])
            ])
        ])
    )
    return content2
