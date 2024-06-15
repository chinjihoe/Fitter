import flet as ft
from database import DB_Error, DB_Fitter
import loginpage, homepage
import logging

class App:
    def main(self, page: ft.Page):
        # page.window_width = 1080/2
        # page.window_height = 2340/2
        page.title="Fitter"

        self.page = page
        # self.db = database.DB_Fitter()
        login = loginpage.LoginPage(page)
        home = homepage.HomePage(page)

        login.setHomePage(home)
        home.setLoginPage(login)

        login.show()

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
app = App()
ft.app(app.main)

# db = Database()
# db.show()