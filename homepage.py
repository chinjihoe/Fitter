import flet as ft
import datetime

def date_range(start, end):
    # this function takes two dates and generates all the dates in the range
    for d in range((end - start).days + 1):
        yield start + datetime.timedelta(days=d)

class HomePage:
    def __init__(self, page):
        self.page = page
        self.exercises = [
            "Bicep curl", 
            "Chest press", 
            "Shoulder press", 
            "Leg press", 
            "Squat", 
            "Lateral pulldown", 
            "Hyperextension", 
            "Hipabduction (inward)", 
            "Hipabduction (outward)", 
            "Abdominal crunch", 
            "Dips",
            "Running", 
            "Cross trainer"
            ]
        self.selectedDate = datetime.datetime.now().strftime('%d %B %Y')
        self.exerciseData = {}
        self.month_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

        self.showRepsGraph = True
        self.showSetsGraph = True
        self.showWeightGraph = True
        self.chartTimeFrameOptions = [
            "Show 30 days",
            "Show 3 months",
            "Show 6 months",
            "Show 1 year",
            "Show from beginning",
        ]
        self.chartTimeframe = self.chartTimeFrameOptions[0]
        self.chartTimeOffset = 0

    def loadData(self):
        for exercise in self.exercises:
            value = self.page.client_storage.get(exercise)
            if value != None:
                self.exerciseData[exercise] = value
            else:
                self.exerciseData[exercise] = []
            print(f"{exercise}: {value}\n")

    # Exercise dropdown menu
    def exerciseSelect(self):
        def dropdown_changed(e):
            self.updateProgressChartData()

        self.exerciseSelection = ft.Dropdown(
            on_change=dropdown_changed,
            height=55
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

        def delete_clicked(e):
            def close_dlg_no(e):
                dlg_modal.open = False
                self.page.update()

            def close_dlg_yes(e):
                for data in self.exerciseData[self.exerciseSelection.value]:
                    if data["date"] == self.date_picker.value.strftime('%d %m %Y'):
                        self.exerciseData[self.exerciseSelection.value].remove(data)
                        self.page.client_storage.set(self.exerciseSelection.value, self.exerciseData[self.exerciseSelection.value])
                        self.updateProgressChartData()
                        break
                dlg_modal.open = False
                self.page.update()

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Delete?"),
                content=ft.Text(f"Delete data from {self.date_picker.value.strftime('%d %b %Y')}?"),
                actions=[
                    ft.TextButton("Yes", on_click=close_dlg_yes),
                    ft.TextButton("No", on_click=close_dlg_no),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()
        
        self.dateRow = ft.Row(controls=[
            date_button,
            date_text,
            ft.ElevatedButton(text="Delete", on_click=delete_clicked),
        ])

    # Adds entry in selected exercise with picked date
    def entryAdd(self):
        _Numberfilter = ft.InputFilter('^[0-9]*')
        reps = ft.TextField(label="Reps", width=80, height=40, multiline=False, autofocus=False, input_filter=_Numberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        sets = ft.TextField(label="Sets", width=80, height=40, multiline=False, autofocus=False, input_filter=_Numberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        weight = ft.TextField(label="Weight", width=80, height=40, multiline=False, autofocus=False, input_filter=_Numberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        
        def add_clicked(e):
            date_already_exists = False
            for data in self.exerciseData[self.exerciseSelection.value]:
                if data["date"] == self.date_picker.value.strftime('%d %m %Y'):
                    data["reps"] = reps.value
                    data["sets"] = sets.value
                    data["weight"] = weight.value
                    date_already_exists = True
                    break

            if date_already_exists == False:
                self.exerciseData[self.exerciseSelection.value].append({
                    "reps": reps.value,
                    "sets": sets.value,
                    "weight": weight.value,
                    "date": self.date_picker.value.strftime('%d %m %Y'),
                })
            self.page.client_storage.set(self.exerciseSelection.value, self.exerciseData[self.exerciseSelection.value])
            self.updateProgressChartData()

        self.entryRow = ft.Row(controls=[
            reps,
            sets,
            weight,
            ft.ElevatedButton(text="Add", on_click=add_clicked),
        ])

    # Redraw the progress chart with new data points
    def updateProgressChartData(self):
        entries = []
        allDates = []
        cur_date = datetime.date.today()
        for entry in self.exerciseData[self.exerciseSelection.value]:
            date = entry['date'].split(' ')
            entry_date = datetime.date(int(date[2]),int(date[1]),int(date[0]))
            if self.chartTimeframe == self.chartTimeFrameOptions[0]:
                days_amount = (cur_date-entry_date).days
                if days_amount >= 0+(self.chartTimeOffset*30) and days_amount <= 30+(self.chartTimeOffset*30):
                    print(cur_date,entry_date,days_amount)
                    entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            elif self.chartTimeframe == self.chartTimeFrameOptions[1]:
                months_amount = cur_date.month - entry_date.month + 1
                print(cur_date.month, entry_date.month, months_amount)
                if months_amount >= 1+(self.chartTimeOffset) and months_amount <= 3+(self.chartTimeOffset):
                    entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            elif self.chartTimeframe == self.chartTimeFrameOptions[2]:
                months_amount = cur_date.month - entry_date.month + 1
                print(cur_date.month, entry_date.month, months_amount)
                if months_amount >= 1+(self.chartTimeOffset*3) and months_amount <= 6+(self.chartTimeOffset*3):
                    entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            elif self.chartTimeframe == self.chartTimeFrameOptions[3]:
                years_amount = abs(cur_date.year - entry_date.year)
                if years_amount == self.chartTimeOffset:
                    entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            elif self.chartTimeframe == self.chartTimeFrameOptions[4]:
                entries.append([int(f"{date[2]}{date[1]}{date[0]}"), int(entry['reps']), int(entry['sets']), int(entry['weight'])]) # [Date, reps, sets, weight]
            else:
                print("Unknown Timeframe", self.chartTimeframe)

        
        if len(entries) > 0: 
            firstDate = min([entry[0] for entry in entries])
            lastDate = max([entry[0] for entry in entries])
            firstDate = datetime.date(int(str(firstDate)[:4]),int(str(firstDate)[4:6]),int(str(firstDate)[6:8]))
            lastDate = datetime.date(int(str(lastDate)[:4]),int(str(lastDate)[4:6]),int(str(lastDate)[6:8]))

            # Create list of all dates between first and last date and add index to each date
            allDates = [date.strftime('%d %m %Y') for date in list(date_range(firstDate, lastDate))]
            allDates = [[i, int(f"{date.split(' ')[2]}{date.split(' ')[1]}{date.split(' ')[0]}")] for i, date in enumerate(allDates)]
            # Find the index in allDates using the dates from entries
            label_index = [[label[1] for label in allDates].index(entry[0]) for entry in entries]
            # Add the date index to the corresponding entry
            entries = [entry + [label_index[i]] for i, entry in enumerate(entries)]
            # Sort the entries array using the date index
            def sort_index(var):
                return var[4]
            entries = sorted(entries, key=sort_index) # entries = [[date, reps, sets, weight, X-value], ...]
            
            # the X-axis uses the points from date indexes (first date = index 0)
            min_x = min([entry[4] for entry in entries])
            max_x = max([entry[4] for entry in entries]) + 1
            min_y=0
            max_y = max([max([entry[1] for entry in entries]), max([entry[2] for entry in entries]), max([entry[3] for entry in entries])]) + 1

            # print(entries)
            print(firstDate,lastDate,max_x)
        else:
            min_x = 0
            max_x = 1
            min_y = 0
            max_y = 1

        data_1 = [
            ft.LineChartData( # reps
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[1], tooltip=None, show_tooltip=False) for entry in entries
                ] if self.showRepsGraph else [],
                stroke_width=4,
                color=ft.colors.BLUE_500,
                curved=False,
                stroke_cap_round=True,
            ),
            ft.LineChartData( # sets
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[2], tooltip=None, show_tooltip=False) for entry in entries
                ] if self.showSetsGraph else [],
                stroke_width=4,
                color=ft.colors.GREEN,
                curved=False,
                stroke_cap_round=True,
            ),
            ft.LineChartData( # weight
                data_points=[
                    ft.LineChartDataPoint(entry[4], entry[3],tooltip=f"Reps: {entry[1]}\nSets: {entry[2]}\nWeight: {entry[3]} \n {datetime.date(int(str(entry[0])[:4]), int(str(entry[0])[4:6]), int(str(entry[0])[6:8])).strftime('%d %b %Y')}") for entry in entries
                ] if self.showWeightGraph else [],
                stroke_width=4,
                color=ft.colors.PINK,
                curved=False,
                stroke_cap_round=True,
                below_line_bgcolor=ft.colors.with_opacity(0.2, ft.colors.PINK),
            )
        ]

        self.chart.data_series = data_1
        self.chart.left_axis = ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(i, size=14, weight=ft.FontWeight.BOLD)) for i in range(min_y,max_y)],
                labels_size=20,
            )
        
        bottom_labels = []
        cur_month = 0 # 1-12
        for i, entry in enumerate(entries):
            if i == 0:
                cur_month = int(str(entry[0])[4:6])
                bottom_label = f"{int(str(entry[0])[6:])}\n{self.month_abbr[cur_month - 1]}"
            else:
                next_month = int(str(entry[0])[4:6])
                if next_month > cur_month:
                    cur_month = next_month
                    bottom_label = f"{int(str(entry[0])[6:])}\n{self.month_abbr[cur_month - 1]}"
                else:
                    bottom_label = f"{int(str(entry[0])[6:])}"
            bottom_labels.append([entry[4], bottom_label]) #index, label

        # indexes_with_labels = [x[0] for x in bottom_labels]
        # last_index = max(indexes_with_labels)
        # for i in range(0, last_index):
        #     if i not in indexes_with_labels:
        #         bottom_labels.append([i, '|']) #index, label

        # print(bottom_labels)

        self.chart.bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=bottom_label[0], # X-axis index
                    label=
                        ft.Text(
                            bottom_label[1], # bottom axis labels: day number + month name
                            size=9,
                            weight=ft.FontWeight.BOLD,
                            no_wrap = True
                        ),
                ) for bottom_label in bottom_labels],
            labels_size=25,
            labels_interval = 1,
            show_labels = True
        )
        self.chart.min_x = min_x
        self.chart.max_x = max_x
        self.chart.min_y = min_y
        self.chart.max_y = max_y
        self.page.update()

    # Create progress chart object
    def progressChart(self):
        self.chart = ft.LineChart(
            data_series=None,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.7, ft.colors.BLACK),
            min_y=0,
            max_y=1,
            min_x=0,
            max_x=1,
            animate=ft.Animation(1000, ft.AnimationCurve.EASE),
            expand=True,
            height=400
        )

    # checkboxes to show or hide graph
    # dropdown: show 30 days, show 3 months, show 6 months, show 1 year, show since beginning
    # buttons back/forward: go back or forward with amount selected in dropdown
    def chartSettings(self):
        def checkbox_changed(e):
            self.showRepsGraph = repsCbox.value
            self.showSetsGraph = setsCbox.value
            self.showWeightGraph = weightCbox.value
            self.updateProgressChartData()

        repsCbox = ft.Checkbox(label="Reps", value=True, on_change=checkbox_changed, active_color=ft.colors.BLUE_500)
        setsCbox = ft.Checkbox(label="Sets", value=True, on_change=checkbox_changed, active_color=ft.colors.GREEN)
        weightCbox = ft.Checkbox(label="Weight", value=True, on_change=checkbox_changed, active_color=ft.colors.PINK)

        def dropdown_changed(e):
            self.chartTimeOffset = 0
            self.chartTimeframe = self.timeframeSelection.value
            print(self.chartTimeframe)
            self.updateProgressChartData()

        self.timeframeSelection = ft.Dropdown(
            width=200,
            on_change=dropdown_changed,
            options=[ft.dropdown.Option(option) for option in self.chartTimeFrameOptions],
            height=55
        )
        self.timeframeSelection.value = self.timeframeSelection.options[0].key
    
        def backwards_clicked(e):
            self.chartTimeOffset = self.chartTimeOffset + 1
            self.updateProgressChartData()

        def forwards_clicked(e):
            self.chartTimeOffset = self.chartTimeOffset - 1
            self.updateProgressChartData()

        timeframeRow = ft.Row(controls=[
            self.timeframeSelection,
            ft.ElevatedButton(text="<", on_click=backwards_clicked),
            ft.ElevatedButton(text=">", on_click=forwards_clicked),
        ])

        checkboxRow = ft.Row(controls=[
            repsCbox,
            setsCbox,
            weightCbox,
        ])

        self.chartSettingsCol = ft.Column([
            checkboxRow,
            timeframeRow
        ])
    
    def pageHome(self):
        self.page.clean()
        self.exerciseSelect()
        self.datePicker()
        self.entryAdd()
        self.progressChart()
        self.chartSettings()
        
        self.loadData()
        self.updateProgressChartData()

        self.page.add(ft.SafeArea(ft.Column([
                self.exerciseSelection, 
                self.dateRow, 
                self.entryRow, 
                self.chart, 
                self.chartSettingsCol
            ], 
            # auto_scroll=True,
            # scroll=ft.ScrollMode.AUTO,
            tight=True,
            # expand=True
            alignment=ft.MainAxisAlignment.START
            ), 
            expand=True,
        ))