import flet as ft
import datetime
import pandas
from operator import itemgetter

class HomePage:
    def __init__(self, page):
        # page.client_storage.clear()
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
            print(f"{exercise}: {value}\n")

    # Exercise dropdown menu
    def exerciseSelect(self):
        def dropdown_changed(e):
            self.page.remove(self.chart)
            self.progressChart()
            self.page.add(self.chart)
            print(f"Show {self.exerciseSelection.value}")

        self.exerciseSelection = ft.Dropdown(
            on_change=dropdown_changed,
        )
        for ex in self.exercises:
            self.exerciseSelection.options.append(ft.dropdown.Option(ex))
        self.exerciseSelection.value = self.exerciseSelection.options[0].key

    # Date picker overlay menu
    def datePicker(self):
        def change_date(e):
            self.selectedDate = self.date_picker.value.strftime("%d %B %Y")
            date_text.value = self.selectedDate
            self.page.update()

        self.date_picker = ft.DatePicker(
            on_change=change_date,
            first_date=datetime.datetime(2024, 1, 1),
        )
        self.date_picker.value = datetime.datetime.now()
        self.page.overlay.append(self.date_picker)

        date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
        )
        date_text = ft.Text(value=self.selectedDate)
        self.dateRow = ft.Row(controls=[
            date_button,
            date_text
        ])

    # Adds entry in selected exercise with picked date
    def entryAdd(self):
        _Numberfilter = ft.InputFilter('^[0-9]*')
        reps = ft.TextField(label="Reps", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        sets = ft.TextField(label="Sets", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        weight = ft.TextField(label="Weight", width=100, multiline=False, autofocus=False, input_filter=_Numberfilter)
        
        def add_clicked(e):
            # print(dd.value, reps.value, sets.value, weight.value, date_picker.value.strftime("%d %m %Y"))
            self.exerciseData[self.exerciseSelection.value].append({
                "reps": reps.value,
                "sets": sets.value,
                "weight": weight.value,
                "date": self.date_picker.value.strftime("%d %m %Y"),
            })
            self.page.client_storage.set(self.exerciseSelection.value, self.exerciseData[self.exerciseSelection.value])
            # print(self.page.client_storage.get(dd.value))
            self.page.update()

        self.entryRow = ft.Row(controls=[
            reps,
            sets,
            weight,
            ft.ElevatedButton(text="Add", on_click=add_clicked)
        ])

    def progressChart(self):
        entries = []
        firstDate = None
        lastDate = None
        for entry in self.exerciseData[self.exerciseSelection.value]:
            date = entry['date'].split(' ')
            entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            if firstDate is None: firstDate = datetime.date(int(date[2]),int(date[1]),int(date[0]))
            elif datetime.date(int(date[2]),int(date[1]),int(date[0])) < firstDate: firstDate = datetime.date(int(date[2]),int(date[1]),int(date[0]))
            if lastDate is None: lastDate = datetime.date(int(date[2]),int(date[1]),int(date[0]))
            elif datetime.date(int(date[2]),int(date[1]),int(date[0])) > lastDate: lastDate = datetime.date(int(date[2]),int(date[1]),int(date[0]))

        if len(entries) > 0: 
            allDates = pandas.date_range(firstDate,lastDate,freq='d').strftime("%d %m %Y").tolist()
            allDates = [[i, int(f"{date.split(' ')[2]}{date.split(' ')[1]}{date.split(' ')[0]}")] for i, date in enumerate(allDates)]
            label_index = [[label[1] for label in allDates].index(entry[0]) for entry in entries]
            entries = [entry + [label_index[i]] for i, entry in enumerate(entries)]
            entries = sorted(entries, key=itemgetter(4)) # entries = [[date, Y-value, X-value], ...]
            print(entries)

            min_x = min([entry[4] for entry in entries])
            max_x = max([entry[4] for entry in entries]) + 1
            min_y=0
            max_y = max([max([entry[1] for entry in entries]), max([entry[2] for entry in entries]), max([entry[3] for entry in entries])]) + 1
        else:
            min_x = 0
            max_x = 3
            min_y = 0
            max_y = 3

        data_1 = [
            ft.LineChartData( # reps
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[1], tooltip=None, show_tooltip=False) for entry in entries
                ],
                stroke_width=5,
                color=ft.colors.CYAN,
                curved=False,
                stroke_cap_round=True,
            ),
            ft.LineChartData( # sets
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[2], tooltip=None, show_tooltip=False) for entry in entries
                ],
                stroke_width=5,
                color=ft.colors.GREEN,
                curved=False,
                stroke_cap_round=True,
            ),
            ft.LineChartData( # weight
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[3], tooltip=f"Reps: {entry[1]}\nSets: {entry[2]}\nWeight: {entry[3]} \n {datetime.date(int(str(entry[0])[:4]), int(str(entry[0])[4:6]), int(str(entry[0])[6:8])).strftime("%d %b %Y")}") for entry in entries
                ],
                stroke_width=5,
                color=ft.colors.RED,
                curved=False,
                stroke_cap_round=True,
            )
        ]

        self.chart = ft.LineChart(
            data_series=data_1,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            # vertical_grid_lines=ft.ChartGridLines(
            #     interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            # ),
            left_axis=ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(i, size=14, weight=ft.FontWeight.BOLD)) for i in range(min_y,max_y)],
                labels_size=20,
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=axis_label[4],
                        label=
                            ft.Text(
                                f"{str(axis_label[0])[6:]}\n{str(axis_label[0])[4:6]}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                    ) for axis_label in entries],
                labels_size=50,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=min_y,
            max_y=max_y,
            min_x=min_x,
            max_x=max_x,
            # animate=5000,
            expand=True,
        )
    
    def pageHome(self):
        self.page.clean()
        self.exerciseSelect()
        self.datePicker()
        self.entryAdd()
        self.progressChart()
        
        self.page.add(self.exerciseSelection, self.dateRow, self.entryRow, self.chart)