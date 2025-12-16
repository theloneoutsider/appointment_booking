from flask_login import login_required, current_user
import jdatetime, datetime, pytz
from model import Ticket

@login_required
def create_time_table():
    today = jdatetime.date.today()
    week_days = [today + jdatetime.timedelta(days=i) for i in range(7)]
    persian_week_days = [ "شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    persian_days = [persian_week_days[day.weekday()] for day in week_days]
    times = []
    for hour in range(7, 20):
        for minute in (0, 30):
            times.append(jdatetime.time(hour, minute))
    
    the_time_table = []
    for t in times:
        the_time_table.append([])
        for day in week_days:     
            tehran = pytz.timezone("Asia/Tehran")
            now = datetime.datetime.now(tehran)
            date = day.togregorian()
            dt_naive = datetime.datetime.combine(date, t)
            dt_aware = tehran.localize(dt_naive)

            if ( now > dt_aware ):
                the_time_table[-1].append("past-time")
            else:
                ticket = Ticket.query.filter_by(date=jdatetime.date(day.year, day.month, day.day).togregorian(), time=t).first()
                if ticket:
                    if ticket.user.id == current_user.id:
                        the_time_table[-1].append("self-reserved")
                    else:
                        the_time_table[-1].append("reserved")
                else:
                    the_time_table[-1].append("not-reserved")

    return the_time_table, week_days, times, today, persian_days


def jdate_from_string(s: str) -> jdatetime.date:
    y, m, d = map(int, s.split('-'))
    return jdatetime.date(y, m, d)

def jtime_from_string(s: str) -> jdatetime.time:
    parts = list(map(int, s.split(':')))
    while len(parts) < 3:
        parts.append(0)   # fill missing seconds or microseconds

    return jdatetime.time(*parts[:3])