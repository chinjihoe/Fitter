import sqlite3
import flet as ft
import homepage
from database import DB_Error, DB_Fitter 

class LoginPage:
    def __init__(self, page: ft.Page, db:DB_Fitter):
        self.page = page
        self.db = db

    def show(self):
        if self.db.isConnected() is False:
            if self.db.connect() is False:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Database connection error (ERR: {self.db.error})"), bgcolor=ft.colors.ORANGE)
                self.page.snack_bar.open = True
                self.page.update()

        def reconnect(e):
            self.db.disconnect()
            self.db = None
            self.db = DB_Fitter()
            self.db.connect()
            if self.db.error == DB_Error.OK:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Reconnect success!"), bgcolor=ft.colors.GREEN)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Reconnect failed (ERR: {self.db.error})"), bgcolor=ft.colors.ORANGE)

            self.page.snack_bar.open = True
            self.page.update()

        def button_clicked(e):
            login_username.value = login_username.value.strip()
            if self.db.userlogin(login_username.value, login_password.value) is True:
                homepage.HomePage(self.page, self.db, login_username.value).show()
            else:
                if self.db.error == DB_Error.LOGIN_FAILED:
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Wrong username or password"), bgcolor=ft.colors.ORANGE)
                else:
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Database connection error (ERR: {self.db.error})"), bgcolor=ft.colors.ORANGE)

                self.page.snack_bar.open = True
                self.page.update()
                login_username.focus()

        self.page.clean()
        self.page.appbar = ft.AppBar(
            leading_width=40,
            toolbar_height= 110,
            title=ft.Text("Fitter", size=60),
            center_title=False,
            bgcolor=ft.colors.GREEN,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="Reconnect database", on_click=reconnect
                        ),
                    ]
                ),
            ],
        )

        login_username = ft.TextField(label="user", autofocus=True, on_submit=button_clicked)
        login_password = ft.TextField(label="password", password=True, can_reveal_password=True, on_submit=button_clicked)
        login_button = ft.ElevatedButton(text="Login", on_click=button_clicked)

        login_container = ft.Container(content=ft.Column([
            login_username,
            login_password,
            login_button
        ]), margin=ft.margin.only(top=10))

        self.page.add(ft.SafeArea(login_container, expand=True))