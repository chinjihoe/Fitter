import flet as ft
import datetime

class HomePage:
    def __init__(self, page):
        self.page = page
        self.exercises = ["Bicep curl", "Chest press", "Shoulder press", "Leg press", "Squat", "Running", "Cross trainer"]
        self.selectedDate = datetime.datetime.now().strftime("%d %B %Y")

        self.exerciseData = {}
        for exercise in self.exercises:
            value = page.client_storage.get(exercise)
            if value != None:
                self.exerciseData[exercise] = value
            else:
                self.exerciseData[exercise] = []

        print(self.exerciseData)

    def pageHome(self):
        self.page.clean()

        # Exercise select
        def dropdown_changed(e):
            self.page.update()

        dd = ft.Dropdown(
            on_change=dropdown_changed,
        )
        for ex in self.exercises:
            dd.options.append(ft.dropdown.Option(ex))
        dd.value = dd.options[0].key

        # Date picker
        def change_date(e):
            self.selectedDate = date_picker.value.strftime("%d %B %Y")
            date_text.value = self.selectedDate
            self.page.update()

        date_picker = ft.DatePicker(
            on_change=change_date,
            first_date=datetime.datetime(2024, 1, 1),
        )
        date_picker.value = datetime.datetime.now()
        self.page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: date_picker.pick_date(),
        )
        date_text = ft.Text(value=self.selectedDate)
        dateRow = ft.Row(controls=[
            date_button,
            date_text
        ])

        # Entry add
        _Numberfilter = ft.InputFilter('^[0-9]*')
        reps = ft.TextField(label="Reps", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        sets = ft.TextField(label="Sets", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        weight = ft.TextField(label="Weight", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        
        def add_clicked(e):
            print(dd.value, reps.value, sets.value, weight.value, date_picker.value.strftime("%d %m %Y"))
            self.exerciseData[dd.value].append({
                "reps": reps.value,
                "sets": sets.value,
                "weight": weight.value,
                "date": date_picker.value.strftime("%d %m %Y"),
            })

            # self.page.client_storage.set(dd.value, reps.value, sets.value, weight.value, date_picker.value.strftime("%d %m %Y"))
            self.page.update()
        btnRow = ft.Row(controls=[
            reps,
            sets,
            weight,
            ft.ElevatedButton(text="Add", on_click=add_clicked)
        ])
        


        # Chart
        data_1 = [
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 3),
                    ft.LineChartDataPoint(2.6, 2),
                    ft.LineChartDataPoint(4.9, 5),
                    ft.LineChartDataPoint(6.8, 3.1),
                    ft.LineChartDataPoint(8, 4),
                    ft.LineChartDataPoint(9.5, 3),
                    ft.LineChartDataPoint(11, 4),
                ],
                stroke_width=5,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ]

        chart = ft.LineChart(
            data_series=data_1,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=3,
                        label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                    ft.ChartAxisLabel(
                        value=5,
                        label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD),
                    ),
                ],
                labels_size=40,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Container(
                            ft.Text(
                                "MAR",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=5,
                        label=ft.Container(
                            ft.Text(
                                "JUN",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                    ft.ChartAxisLabel(
                        value=8,
                        label=ft.Container(
                            ft.Text(
                                "SEP",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                            ),
                            margin=ft.margin.only(top=10),
                        ),
                    ),
                ],
                labels_size=32,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=0,
            max_y=6,
            min_x=0,
            max_x=11,
            # animate=5000,
            expand=True,
        )
        
        self.page.add(dd, dateRow, btnRow, chart)