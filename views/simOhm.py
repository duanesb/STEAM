import flet as ft

def Ohm_View(router):
    content = ft.Container(
        content=ft.Column(spacing=25,controls=[
            ft.Row(controls=[ft.Text("Ohm's Law", size=35, weight="bold")],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND,controls=[
                ft.Column(spacing=30,controls=[
                    ft.Container(on_click=lambda _: router.go('/intro'), content=ft.Column(controls=[
                        ft.Text("Back", size=30, weight="bold"),
                    ]))
                ])
            ])
        ])
    )
    content2 = ft.Container(
        content=ft.Column(
            
        )
    )
    return content