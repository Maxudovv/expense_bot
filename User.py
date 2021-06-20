import schedule
import datetime as dt

class User:
    def __init__(self, reg_time=dt.datetime.now()):
        schedule.every().day.do(self.new_day)
        schedule.every().week.do(self.new_week)
        self.register_time = reg_time
        self.month_salary = 0
        self.month_spending = 0
        self.day_salary = 0
        self.day_spending = 0
        self.logs = {} # За месяц
        self.day_logs = {}
        self.weeks = 0

    def new_week(self):
        self.weeks += 1
        if self.weeks % 4 == 0:
            self.new_month()

    def new_day(self):
        self.day_salary = 0
        self.day_spending = 0
        self.day_logs = {}

    def new_month(self):
        self.month_salary = 0
        self.month_spending = 0
        self.logs = {}

    def add_money(self, value: int):
        self.day_salary += value
        self.month_salary += value

    def spend_money(self, value: int, for_what: str):
        for_what = for_what.title()
        self.day_salary -= value
        self.month_salary -= value
        self.day_spending += value
        self.month_spending += value
        res = self.logs.setdefault(for_what, 0)
        self.logs.update({for_what: res + value})
        self.day_logs.update({for_what: res + value})