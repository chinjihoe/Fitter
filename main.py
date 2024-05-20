import flet as ft
import datetime
import home

class App:
    def pageExersices(self):
        self.page.clean()
        self.page.add(ft.Text(value="ex", color="black"))

    def pageSettings(self):
        self.page.clean()
        self.page.add(ft.Text(value="sett", color="black"))

    def main(self, page: ft.Page):
        self.page = page
        self.homePage = home.HomePage(page)

        page.title="Fitter"

        def navbar_clicked(e):
            navIndex = page.navigation_bar.selected_index
            if navIndex == 0:
                self.homePage.pageHome()
            elif navIndex == 1:
                self.pageExersices()
            elif navIndex == 2:
                self.pageSettings()
            page.update()

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
                ft.NavigationDestination(icon=ft.icons.PHOTO, label="Exercises"),
                ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ],
            on_change=navbar_clicked
        )

        self.homePage.pageHome()


app = App()
ft.app(app.main)
