import flet as ft
from views.simOhm import Ohm_View
from views.intro import Intro_View

class Router:
    def __init__(self, page, ft):
        self.page = page
        self.ft = ft
        self.routes = {
            "/ohm" : Ohm_View(page),
            "/intro" : Intro_View(page),
        }
        self.body = ft.Container(content=self.routes['/intro'])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()

    def update(self): 
        self.page.update()