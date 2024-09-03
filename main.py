from flet import Container, Column, Row, Text, Stack, colors as COLORS
import flet as ft
from modules import MyColors, GlobalMonitor, readFile

def main(page: ft.Page):
    page.title = "Random Task Selector"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = COLORS.BLACK
    page.padding = 12

    readFile()
    
    page.add(
        Row(
            controls=[
                Container( #the working area
                    content=GlobalMonitor(),
                    bgcolor=MyColors.SUPERGREY,
                    expand=True,
                    border_radius=8,
                    padding=12,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
    pass


if __name__ == "__main__":
    ft.app(main)
    pass