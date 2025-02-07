import asyncio
import platform

if platform.system() == "Darwin":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import flet as ft

from views.hub import Router

# import pygame

def main(page: ft.Page):
    router = Router(page, ft)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = 'Physics Simulators'
    page.window.width = 800
    page.window.height = 800
    page.bgcolor = '#632dee'
    page.scroll = True
    page.window.resizable = False
    page.on_route_change = router.route_change
    router.page = page
    page.add(
        router.body,
    )
    router.page = page
    page.go('/intro')

ft.app(target=main, assets_dir="assets")