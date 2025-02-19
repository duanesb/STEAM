import flet as ft
from views.hub import Router
from objects import hover_sound, click_sound

#import pygame

def main(page: ft.Page):
    router = Router(page, ft)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = 'Physics Simulators'
    page.window.width = 800
    page.window.height = 800
    page.bgcolor = '#c3bad9'
    page.scroll = True
    page.window.resizable = False
    page.on_route_change = router.route_change
    router.page = page
    page.add(
        click_sound, 
        hover_sound,
        router.body,
    )
    router.page = page
    page.go('/intro')

ft.app(target=main, assets_dir="assets")