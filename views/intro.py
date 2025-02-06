import flet as ft

def Intro_View(router):
    content = ft.Container(
        content=ft.Column(spacing=25,controls=[
            ft.Row(controls=[ft.Text("Simulators", size=35, weight="bold")],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/ohm'), content=ft.Column(controls=[
                        ft.Text("Ohm's Law", size=30, weight="bold"),
                ],alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(on_click=lambda _: router.go('/capacitance'), content=ft.Column(controls=[
                        ft.Text("Capacitance", size=30, weight="bold"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ]),

                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/electric'), content=ft.Column(controls=[
                        ft.Text("Electric Field", size=30, weight="bold"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                    ft.Container(on_click=lambda _: router.go('/resistance'), content=ft.Column(controls=[
                        ft.Text("Resistance", size=30, weight="bold"),
                    ], alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                ])
            ])
        ])
    )
    return content
