import flet as ft
from database import DB_Error, DB_Fitter
import loginpage, homepage

class App:
    def set_database(self, db):
        self.db = db
    def main(self, page: ft.Page):
        # page.window_width = 1080/2
        # page.window_height = 2340/2
        page.title="Fitter"

        self.page = page
        # self.db = database.DB_Fitter()
        self.loginpage = loginpage.LoginPage(page, self.db)
        self.loginpage.show()

db_fitter = DB_Fitter()
app = App()
app.set_database(db_fitter)
ft.app(app.main)

# db = Database()
# db.show()