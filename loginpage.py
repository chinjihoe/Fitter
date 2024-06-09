import sqlite3
import flet as ft
import database, homepage

class LoginPage:
    def __init__(self, page: ft.Page, db:database.DB_Fitter):
        self.page = page
        self.db = db

    def show(self):
        def button_clicked(e):
            if self.db.userlogin(login_username.value, login_password.value) is True:
                homepage.HomePage(self.page, self.db, login_username.value).show()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Login failed"), bgcolor=ft.colors.ORANGE)
                self.page.snack_bar.open = True
                self.page.update()
                login_username.focus()

        self.page.clean()
        login_username = ft.TextField(label="user", autofocus=True, on_submit=button_clicked)
        login_password = ft.TextField(label="password", password=True, can_reveal_password=True, on_submit=button_clicked)
        login_button = ft.ElevatedButton(text="Login", on_click=button_clicked)

        login_container = ft.Container(content=ft.Column([
            ft.Text("Fitter", size=70),
            login_username,
            login_password,
            login_button
        ]), margin=ft.margin.only(top=10))

        self.page.add(ft.SafeArea(login_container, expand=True))