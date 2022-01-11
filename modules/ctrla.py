from calendar import month_name, day_abbr, Calendar
from datetime import date

from sqlalchemy import text

from modules import db
from modules.models import Entry


class Database:
    def __init__(self):
        pass

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def get(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def search(type_, order_by: str = "", filter_: str = ""):
        return db.session.query(type_).filter(text(filter_)).order_by(text(order_by))

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.execute(stmt)
        db.session.commit()


class HabitCalendar(Calendar):
    """
    This calendar returns complete HTML pages.
    """

    # CSS classes for the day <td>s
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

    # CSS classes for the day <th>s
    cssclasses_weekday_head = cssclasses

    # CSS class for the days before and after current month
    cssclass_noday = "noday"

    # CSS class for the month's head
    cssclass_month_head = "month"

    # CSS class for the month
    cssclass_month = "month"

    # CSS class for the year's table head
    cssclass_year_head = "year"

    # CSS class for the whole year table
    cssclass_year = "year"

    def formatday(self, day, weekday):
        """
        Return a day as a table cell.
        """

        if day == 0:
            # day outside month
            return '<div class="card-body %s" style="height:100px;width:100px">&nbsp;</div>' % self.cssclass_noday
        else:
            _ = db.session.query(Entry).filter(Entry.datestamp == date(date.today().year, date.today().month, day)).all()
            if _:
                x = ""
                for i in _:
                    x += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="%s" class="bi bi-circle-fill mr-1" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8"/></svg>' % i.habits.color
                return '<div class="card-body border text-truncate %s" style="height:100px;width:100px">%d<br>%s</div>' % (
                    self.cssclasses[weekday], day, x)
            else:
                return '<div class="card-body border %s" style="height:100px;width:100px">%d</div>' % (
                    self.cssclasses[weekday], day)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<div class="row">%s</div>' % s

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return '<p class="text-center card-body font-italic font-weight-bold %s" style="width:100px; height:10px">%s</p>' % (
            self.cssclasses_weekday_head[day], day_abbr[day])

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<div class="row">%s</div>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<p class="text-center %s font-italic" style="font-size:2em">%s</p>' % (
            self.cssclass_month_head, s)

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<div border="0" cellpadding="0" cellspacing="0" class="my-5 w-100 %s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</div>')
        a('\n')
        return ''.join(v)
