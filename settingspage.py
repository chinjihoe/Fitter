import flet as ft

class SettingsPage:
    def __init__(self, page):
        self.page = page

    def deleteData(self):
        def deletedata_clicked(e):
            def close_dlg_no(e):
                dlg_modal.open = False
                self.page.update()

            def close_dlg_yes(e):
                self.page.client_storage.clear()
                dlg_modal.open = False
                self.page.update()

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Are you sure?"),
                content=ft.Text(f"Delete all data"),
                actions=[
                    ft.TextButton("Yes", on_click=close_dlg_yes),
                    ft.TextButton("No", on_click=close_dlg_no),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()

        self.deleteDataCol = ft.Column([
            ft.Text(value="Delete all data, this action is irreversible", color="black"),
            ft.ElevatedButton(text="Delete data", on_click=deletedata_clicked)
        ])

    def pageSettings(self):
        self.page.clean()
        self.deleteData()

        self.page.add(ft.SafeArea(ft.Column([
            self.deleteDataCol
        ]), expand=True))
        