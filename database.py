import sqlite3

class DB_Fitter:
    def __init__(self):
        self.sqliteConnection = None
        self.cursor = None

    def connect(self):
        try:
            self.sqliteConnection = sqlite3.connect('SQLite/db_fitter.db')
            self.cursor = self.sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            return True
        except sqlite3.Error as error:
            self.sqliteConnection = None
            self.cursor = None
            print("Error while connecting to sqlite", error)
            return False

    def disconnect(self):
        try:
            if self.cursor != None:
                self.cursor.close()
            if self.sqliteConnection != None:
                self.sqliteConnection.close()
        except:
            pass

    def userlogin(self, username, password):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"select * from users where username='{username}' and password='{password}';")
                record = self.cursor.fetchall()
                if len(record) == 1:
                    return True
                else:
                    return False
            else:
                return False
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return False
        
    # 30 days
    # 3 months
    # 6 months
    # 1 year
    # since beginning
    def loadExerciseData(self, exercise, user, offset_days=0, offset_months=0, offset_years=0, offset_days_range=0, offset_months_range=0, offset_years_range=0, get_all=False):
        try:
            offset_days_2 = offset_days + offset_days_range
            offset_months_2 = offset_months + offset_months_range
            offset_years_2 = offset_years + offset_years_range
            if self.sqliteConnection != None and self.cursor != None:
                if get_all is True:
                    self.cursor.execute(f"select * from {exercise} where user='{user}' order by date;")
                else:
                    query = f"select * from {exercise} where user='{user}' and date >= DATE('now', '-{offset_days_2} day', '-{offset_months_2} month', '-{offset_years_2} year') and date <= DATE('now', '-{offset_days} day', '-{offset_months} month', '-{offset_years} year') order by date;"
                    # print(query)
                    self.cursor.execute(query)
                record = self.cursor.fetchall()
                return record
            else:
                return None
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return None
        
    # def loadExerciseData(self, exercise, user):
    #     try:
    #         if self.sqliteConnection != None and self.cursor != None:
    #             self.cursor.execute(f"select * from {exercise} where user='{user}' order by date;")
    #             record = self.cursor.fetchall()
    #             return record
    #         else:
    #             return None
    #     except sqlite3.Error as error:
    #         self.disconnect()
    #         self.connect()
    #         return None
    
    def AddWeightEntry(self, exercise, user, sets, reps, weight, date):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"DELETE FROM {exercise} WHERE user='{user}' AND date='{date}';")
                self.cursor.execute(f"insert into {exercise}(user,sets,reps,weight,date) values('{user}', '{sets}', '{reps}', '{weight}', '{date}');")
                self.sqliteConnection.commit()
                return True
            else:
                return False
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return False
        
    def AddDistanceEntry(self, exercise, user, minutes, distance, speed, date):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"DELETE FROM {exercise} WHERE user='{user}' AND date='{date}';")
                self.cursor.execute(f"insert into {exercise}(user,minutes,distance,speed,date) values('{user}', '{minutes}', '{distance}', '{speed}', '{date}');")
                self.sqliteConnection.commit()
                return True
            else:
                return False
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return False
        
    def DeleteEntry(self, exercise, user, date):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"DELETE FROM {exercise} WHERE user='{user}' AND date='{date}';")
                self.sqliteConnection.commit()
                return True
            else:
                return False
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return False

    def loadNotes(self, user):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"select note from notes where user='{user}';")
                record = self.cursor.fetchall()
                return record
            else:
                return None
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return None
    
    def writeNotes(self, user, note):
        try:
            if self.sqliteConnection != None and self.cursor != None:
                self.cursor.execute(f"DELETE FROM notes WHERE user='{user}';")
                self.cursor.execute(f"insert into notes(user,note) values('{user}', '{note}');")
                self.sqliteConnection.commit()
                return True
            else:
                return False
        except sqlite3.Error as error:
            self.disconnect()
            self.connect()
            return False