import datetime

from modules import db
from modules.model import Day


class Calendar:
    def __init__(self):
        pass

    @staticmethod
    def get_last_week():
        today = datetime.date.today()
        return [today - datetime.timedelta(days=i) for i in range(0, 7)]

    @staticmethod
    def get_last_month():
        today = datetime.date.today()
        return [today - datetime.timedelta(days=i) for i in range(0, 30)]

    @staticmethod
    def format_day(day: datetime.date):
        x = ''
        for i in db.session.query(Day).filter(Day.date == day):
            x += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="%s" class="bi bi-circle-fill mr-1" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8"/></svg>' % i.habits.color

        return '<div class="card day border-0"><div class="card-body m-2 bg-light rounded shadow-sm"><a href="/day?day_date=%s" class="link">%s\n%s</a></div></div>' % (
            day, day.strftime("%-m/%-d"), x)

    def format_week(self):
        week = ''.join([self.format_day(i) for i in self.get_last_week()])
        return '<div>%s</div>' % week

    def format_month(self):
        month = ''.join([self.format_day(i) for i in self.get_last_month()])
        return '<div class="row">\n%s</div>' % month
