import flet as ft
import homepage, settingspage

class App:
    def pageExersices(self):
        self.page.clean()
        self.page.add(ft.SafeArea(ft.Text(value="ex", color="black"), expand=True))

    def main(self, page: ft.Page):
        # page.window_width = 1080/2
        # page.window_height = 2340/2
        self.page = page
        self.homePage = homepage.HomePage(page)
        self.settingsPage = settingspage.SettingsPage(page)

        page.title="Fitter"

        # def navbar_clicked(e):
        #     navIndex = page.navigation_bar.selected_index
        #     if navIndex == 0:
        #         self.homePage.pageHome()
        #     elif navIndex == 1:
        #         self.pageExersices()
        #     elif navIndex == 2:
        #         self.settingsPage.pageSettings()
        #     page.update()

        # page.navigation_bar = ft.NavigationBar(
        #     destinations=[
        #         ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
        #         ft.NavigationDestination(icon=ft.icons.PHOTO, label="Exercises"),
        #         ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings"),
        #     ],
        #     on_change=navbar_clicked
        # )

        self.homePage.pageHome()


app = App()
ft.app(app.main)
