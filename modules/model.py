import sys
from calendar import January, month_name, day_abbr, Calendar
from datetime import date

from sqlalchemy import Column, Text, Date, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from modules import db


class Task(db.Model):
    __tablename__ = "tasks"

    name = Column(Text)
    priority = Column(Integer, default=3)
    note = Column(Text)
    done = Column(Boolean, default=False)
    date_created = Column(DateTime)
    date_due = Column(Date)
    date_done = Column(DateTime)
    reminder = Column(Boolean, default=False)
    folder = Column(Integer, ForeignKey("folders.id"))
    parent_task = Column(Integer, ForeignKey("tasks.id"))
    subtasks = relationship("Task", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_parent_task(self):
        return db.session.query(Task).get(self.parent_task)

    def get_subtasks_count(self):
        return self.subtasks.filter(Task.done == False).count()

    def get_subtasks_progress(self):
        done = self.subtasks.filter(Task.done == True).count()
        total = self.subtasks.count()
        perc = (done / total) * 100
        return perc

    def get_priority(self):
        if self.priority == 3:
            return ["Low", "yellow"]
        elif self.priority == 2:
            return ["Medium", "orange"]
        elif self.priority == 1:
            return ["High", "red"]

    def __str__(self):
        return "%s" % self.name


class Folder(db.Model):
    __tablename__ = "folders"

    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime)
    tasks = relationship("Task", backref="folders", lazy="dynamic")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Folder, self).__init__(**kwargs)

    def get_tasks(self):
        return self.tasks.order_by(Task.done, Task.date_created.desc())

    def get_undone_count(self) -> int:
        return self.tasks.filter(Task.done == False).count()

    def __str__(self):
        return "%s" % self.name


class Habit(db.Model):
    __tablename__ = "habits"

    name = Column(Text)
    start_date = Column(DateTime)
    frequency = Column(Text, default="daily")
    end_date = Column(Date)
    reminder = Column(Boolean, default=False)
    color = Column(Text)
    days = relationship("Day", backref="habits", cascade="all, delete")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Habit, self).__init__(**kwargs)

    def __str__(self):
        return "%s" % self.name


class List(db.Model):
    __tablename__ = "lists"

    name = Column(Text)
    contents = Column(Text)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    color = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(List, self).__init__(**kwargs)

    def get_items(self):
        return self.contents.split("\n")

    def __str__(self):
        return "%s" % self.name


class Day(db.Model):
    __tablename__ = "days"

    habit = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date)
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(Day, self).__init__(**kwargs)

    def __str__(self):
        return "%s,%s" % (self.habit, self.date)


db.create_all()


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
            _ = db.session.query(Day).filter(Day.date == date(date.today().year, date.today().month, day)).all()
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

    def formatyear(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' %
          self.cssclass_year)
        a('\n')
        a('<tr><th colspan="%d" class="%s">%s</th></tr>' % (
            width, self.cssclass_year_head, theyear))
        for i in range(January, January + 12, width):
            # months in this row
            months = range(i, min(i + width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(theyear, m, withyear=False))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)

    def formatyearpage(self, theyear, width=3, css='calendar.css', encoding=None):
        """
        Return a formatted year as a complete HTML page.
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()
        v = []
        a = v.append
        a('<?xml version="1.0" encoding="%s"?>\n' % encoding)
        a('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
        a('<html>\n')
        a('<head>\n')
        a('<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n' % encoding)
        if css is not None:
            a('<link rel="stylesheet" type="text/css" href="%s" />\n' % css)
        a('<title>Calendar for %d</title>\n' % theyear)
        a('</head>\n')
        a('<body>\n')
        a(self.formatyear(theyear, width))
        a('</body>\n')
        a('</html>\n')
        return ''.join(v).encode(encoding, "xmlcharrefreplace")
