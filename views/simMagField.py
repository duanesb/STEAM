import flet as ft

def Magnetic_View(router):
    content = ft.Container(
        content=ft.Column(spacing=25,controls=[
            ft.Row(controls=[ft.Text("Magnetic Field", size=35, weight="bold")],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/intro'), content=ft.Column(controls=[
                        ft.Text("Back", size=30, weight="bold"),
                    ]))
                ])
            ])
        ])
    )
    return content