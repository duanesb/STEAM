import flet as ft
from objects import BackElevatedButton,ContentContainer

def Ohm_View(router):
    controls = [
        ft.Text("Ohm's Law", size=55, weight="bold"),
        ft.Container(
            width=600,height=500,bgcolor="white"
        ),
        BackElevatedButton("Back",lambda e:router.go('/intro'))
    ]
    content = ContentContainer(controls)
    return content