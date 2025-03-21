import flet as ft

from objects import BackElevatedButton,ContentContainer

def Capacitance_View(router):
    controls = [
        ft.Text("Capacitance", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white",border=ft.border.all(5,"#201b2e")
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content