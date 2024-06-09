import flet as ft
import database
import loginpage, homepage, settingspage

class App:
    def main(self, page: ft.Page):
        # page.window_width = 1080/2
        # page.window_height = 2340/2
        page.title="Fitter"

        self.page = page
        self.db = database.DB_Fitter()

        if self.db.connect() is False:
            self.page.clean()
            self.page.add(ft.SafeArea(ft.Text("Database connection error."), expand=True))
        else:
            self.loginpage = loginpage.LoginPage(page, self.db)

            # self.homepage.show()
            self.loginpage.show()
        page.update()


app = App()
ft.app(app.main)

# db = Database()
# db.show()