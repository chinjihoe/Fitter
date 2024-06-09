import flet as ft
import datetime
import database
from threading import Timer

def date_range(start, end):
    # this function takes two dates and generates all the dates in the range
    for d in range((end - start).days + 1):
        yield start + datetime.timedelta(days=d)

class HomePage:
    def __init__(self, page: ft.Page, db:database.DB_Fitter, curentUser):
        self.page = page
        self.db = db
        self.curentUser = curentUser
        self.exercises = [
            ("Bicep curl", "bicepcurls"),
            ("Chest press", "chestpress"), 
            ("Shoulder press", "shoulderpress"), 
            ("Leg press", "legpress"), 
            ("Squat", "squat"), 
            ("Lateral pulldown", "lateralpulldown"), 
            ("Hyperextension", "hyperextension"), 
            ("Hipabduction (inward)", "hipabductioninward"), 
            ("Hipabduction (outward)", "hipabductionoutward"), 
            ("Abdominal crunch", "abdominalcrunch"),
            ("Dips", "dips"),
            ("Back kick", "backkick"),
            ("Seated row", "seatedrow"),
            ("Running", "running"), 
            ("Cross trainer", "crosstrainer")
            ]
        self.selectedDate = datetime.datetime.now().strftime('%d %B %Y')
        # self.exerciseData = {}
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
        self.notesTimer = None

    def _getDBTableName(self):
        return self.exercises[[exercise[0] for exercise in self.exercises].index(self.exerciseSelection.value)][1]

    # Exercise dropdown menu
    def exerciseSelect(self):
        def dropdown_changed(e):
            db_tablename = self._getDBTableName()
            if db_tablename == 'running' or db_tablename == 'crosstrainer':
                self.input1.label = 'Mins'
                self.input2.label = 'Km'
                self.input3.label = 'Speed'
                self.chartCBox1.label = 'Mins'
                self.chartCBox2.label = 'Km'
                self.chartCBox3.label = 'Speed'
            else:
                self.input1.label = 'Sets'
                self.input2.label = 'Reps'
                self.input3.label = 'Weight'
                self.chartCBox1.label = 'Sets'
                self.chartCBox2.label = 'Reps'
                self.chartCBox3.label = 'Weight'
            self.updateProgressChartData()

        self.exerciseSelection = ft.Dropdown(
            on_change=dropdown_changed,
        )
        for ex in self.exercises:
            self.exerciseSelection.options.append(ft.dropdown.Option(ex[0]))
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
                db_tablename = self._getDBTableName()
                self.db.DeleteEntry(db_tablename, self.curentUser, self.date_picker.value.strftime('%Y-%m-%d'))
                self.updateProgressChartData()
                dlg_modal.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Entry deleted"), bgcolor=ft.colors.BLUE)
                self.page.snack_bar.open = True
                self.page.update()
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
        # positiveNumberfilter = ft.InputFilter('^[0-9]*') # only positive numbers allowed
        decimalNumberfilter = ft.InputFilter('-?\d+\.?\d*') # all decimal numbers allowed
        self.input1 = ft.TextField(label="Sets", width=80, height=40, multiline=False, autofocus=False, input_filter=decimalNumberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        self.input2 = ft.TextField(label="Reps", width=80, height=40, multiline=False, autofocus=False, input_filter=decimalNumberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        self.input3 = ft.TextField(label="Weight", width=80, height=40, multiline=False, autofocus=False, input_filter=decimalNumberfilter, keyboard_type=ft.KeyboardType.NUMBER)
        
        def add_clicked(e):
            db_tablename = self._getDBTableName()
            if db_tablename == 'running' or db_tablename == 'crosstrainer':
                self.db.AddDistanceEntry(db_tablename, self.curentUser, self.input1.value, self.input2.value, self.input3.value, self.date_picker.value.strftime('%Y-%m-%d'))
            else:
                self.db.AddWeightEntry(db_tablename, self.curentUser, self.input1.value, self.input2.value, self.input3.value, self.date_picker.value.strftime('%Y-%m-%d'))
            self.updateProgressChartData()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Entry added"), bgcolor=ft.colors.BLUE)
            self.page.snack_bar.open = True
            self.page.update()

        self.entryRow = ft.Row(controls=[
            self.input1,
            self.input2,
            self.input3,
            ft.ElevatedButton(text="Add", on_click=add_clicked),
        ])

    # Redraw the progress chart with new data points
    def updateProgressChartData(self):
        entries = []
        allDates = []

        db_tablename = self._getDBTableName()
        if self.chartTimeframe == self.chartTimeFrameOptions[0]: # 30 days
            data = self.db.loadExerciseData(db_tablename, self.curentUser, offset_days = self.chartTimeOffset*30, offset_days_range = 30)
        elif self.chartTimeframe == self.chartTimeFrameOptions[1]: # 3 months
            data = self.db.loadExerciseData(db_tablename, self.curentUser, offset_months = self.chartTimeOffset*3, offset_months_range = 3)
        elif self.chartTimeframe == self.chartTimeFrameOptions[2]: # 6 months
            data = self.db.loadExerciseData(db_tablename, self.curentUser, offset_months = self.chartTimeOffset*6, offset_months_range = 6)
        elif self.chartTimeframe == self.chartTimeFrameOptions[3]: # 1 year
            data = self.db.loadExerciseData(db_tablename, self.curentUser, offset_years = self.chartTimeOffset, offset_years_range = 1)
        elif self.chartTimeframe == self.chartTimeFrameOptions[4]: # since beginning
            data = self.db.loadExerciseData(db_tablename, self.curentUser, get_all=True)
        else:
            data = []

        for entry in data:
            date = entry[4].split('-')
            entries.append([int(f"{date[0]}{date[1]}{date[2]}"), int(entry[2]), int(entry[1]), float(entry[3])]) # [Date, reps, sets, weight]
        
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
            min_y = min([min([entry[1] for entry in entries]), min([entry[2] for entry in entries]), min([entry[3] for entry in entries])])
            max_y = max([max([entry[1] for entry in entries]), max([entry[2] for entry in entries]), max([entry[3] for entry in entries])]) + 1

            # print(entries)
            # print(firstDate,lastDate,max_x)
        else:
            min_x = 0
            max_x = 1
            min_y = 0
            max_y = 1

        db_tablename = self._getDBTableName()
        if db_tablename == 'running' or db_tablename == 'crosstrainer':
            tooltipName1 = "Mins"
            tooltipName2 = "Km"
            tooltipName3 = "Speed"
        else:
            tooltipName1 = "Sets"
            tooltipName2 = "Reps"
            tooltipName3 = "Weight"

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
                    ft.LineChartDataPoint(entry[4], entry[3],tooltip=f"{tooltipName1}: {entry[2]}\n{tooltipName2}: {entry[1]}\n{tooltipName3}: {entry[3]} \n {datetime.date(int(str(entry[0])[:4]), int(str(entry[0])[4:6]), int(str(entry[0])[6:8])).strftime('%d %b %Y')}") for entry in entries
                ] if self.showWeightGraph else [],
                stroke_width=4,
                color=ft.colors.PINK,
                curved=False,
                stroke_cap_round=True,
                below_line_bgcolor=ft.colors.with_opacity(0.2, ft.colors.PINK),
            )
        ]

        self.progresschart.data_series = data_1
        self.progresschart.left_axis = ft.ChartAxis(
                labels=[ft.ChartAxisLabel(value=i, label=ft.Text(i, size=14, weight=ft.FontWeight.BOLD)) for i in range(int(min_y),int(max_y)+1)],
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

        self.progresschart.bottom_axis=ft.ChartAxis(
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
        self.progresschart.min_x = min_x
        self.progresschart.max_x = max_x
        self.progresschart.min_y = min_y
        self.progresschart.max_y = max_y
        self.page.update()

    # Create progress chart object
    def progressChart(self):
        self.progresschart = ft.LineChart(
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
            # expand=True,
            height=300
        )

    # checkboxes to show or hide graph
    # dropdown: show 30 days, show 3 months, show 6 months, show 1 year, show since beginning
    # buttons back/forward: go back or forward with amount selected in dropdown
    def chartSettings(self):
        def checkbox_changed(e):
            self.showSetsGraph = self.chartCBox1.value
            self.showRepsGraph = self.chartCBox2.value
            self.showWeightGraph = self.chartCBox3.value
            self.updateProgressChartData()

        self.chartCBox1 = ft.Checkbox(label="Sets", value=True, on_change=checkbox_changed, active_color=ft.colors.GREEN)
        self.chartCBox2 = ft.Checkbox(label="Reps", value=True, on_change=checkbox_changed, active_color=ft.colors.BLUE_500)
        self.chartCBox3 = ft.Checkbox(label="Weight", value=True, on_change=checkbox_changed, active_color=ft.colors.PINK)

        def dropdown_changed(e):
            self.chartTimeOffset = 0
            self.chartTimeframe = self.timeframeSelection.value
            # print(self.chartTimeframe)
            self.updateProgressChartData()

        self.timeframeSelection = ft.Dropdown(
            width=200,
            on_change=dropdown_changed,
            options=[ft.dropdown.Option(option) for option in self.chartTimeFrameOptions],
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
            self.chartCBox1,
            self.chartCBox2,
            self.chartCBox3,
        ])

        self.chartSettingsCol = ft.Column([
            checkboxRow,
            timeframeRow
        ])

    def exerciseNotes(self):
        def writeNotes(e):
            if self.db.writeNotes(self.curentUser, self.notesTextField.value) is True:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Notes saved"), bgcolor=ft.colors.BLUE)
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error saving notes"), bgcolor=ft.colors.ORANGE)

            self.page.snack_bar.open = True
            self.page.update()

        # def notes_onchange(e):
        #     if self.notesTimer is not None:
        #         self.notesTimer.cancel()
        #         self.notesTimer = Timer(1, writeNotes)
        #         self.notesTimer.start()
        #     else:
        #         self.notesTimer = Timer(1, writeNotes)
        #         self.notesTimer.start()
        
        noteText = self.db.loadNotes(self.curentUser)
        if len(noteText) == 0:
            noteText = ""
        else:
            noteText = noteText[0][0]

        self.notesTextField = ft.TextField(
            label="Notes",
            multiline=True,
            min_lines=5,
            value=noteText,
            # on_change=notes_onchange
        )
        self.notesContainer = ft.Container(
            content= ft.Column([
                ft.ElevatedButton("Save notes", on_click=writeNotes),
                self.notesTextField
            ]), 
            margin=ft.margin.only(top=20)
            )
    
    def show(self):
        # self.loadData()

        self.page.clean()
        self.exerciseSelect()
        self.datePicker()
        self.entryAdd()
        self.progressChart()
        self.chartSettings()
        self.exerciseNotes()
       
        self.updateProgressChartData()

        page_col = ft.Column([
                self.exerciseSelection, 
                self.dateRow, 
                self.entryRow, 
                self.progresschart, 
                self.chartSettingsCol,
                self.notesContainer
            ], 
            scroll=ft.ScrollMode.HIDDEN,
            height=self.page.height,
            width=self.page.width,
        )

        self.page.add(ft.SafeArea(page_col, expand=True))

        def page_resized(e):
            page_col.height=self.page.height
            page_col.width=self.page.width
            self.page.update()
        self.page.on_resize = page_resized