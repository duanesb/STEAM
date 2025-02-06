import flet as ft
from views.intro import Intro_View
from views.simOhm import Ohm_View
from views.simCapacitance import Capacitance_View
from views.simMagField import Magnetic_View
from views.simResistance import Resistance_View

class Router:
    def __init__(self, page, ft):
        self.page = page
        self.ft = ft
        self.routes = {
            "/intro" : Intro_View(page),
            "/ohm" : Ohm_View(page),
            "/capacitance" : Capacitance_View(page),
            "/magnetic" : Magnetic_View(page),
            "/resistance" : Resistance_View(page),
            
        }
        self.body = ft.Container(content=self.routes['/intro'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()

    def update(self): 
        self.page.update()