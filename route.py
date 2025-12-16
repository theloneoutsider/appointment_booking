from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from utility import create_time_table, jdate_from_string, jtime_from_string
from appointment_booking import  db
from form import RegistrationForm, LoginForm
from model import User, Ticket
import datetime, pytz


blueprint = Blueprint("main", __name__)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("main.index"))
    return render_template("register.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for("main.index")
            return redirect(next)
        flash('Invalid username or password.')
        return redirect(url_for('main.login'))
    return render_template('login.html', form=form)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.login"))


@blueprint.route("/")
@login_required
def index():
    the_time_table, week_days, times, today, persian_days = create_time_table()
    return render_template("index.html", the_time_table=the_time_table, week_days=week_days, times= times, today=today, persian_days=persian_days)


@blueprint.route("/<day>/<time>")
@login_required
def book_appointment(day, time):
    tehran = pytz.timezone("Asia/Tehran")
    now = datetime.datetime.now(tehran)
    date = jdate_from_string(day).togregorian()
    time = jtime_from_string(time)
    dt_naive = datetime.datetime.combine(date, time)
    dt_aware = tehran.localize(dt_naive)

    if ( now > dt_aware ):
        return redirect(url_for("main.index"))
    
    ticket = Ticket.query.filter_by(date=date, time=time).first()
    
    if ticket:
        if ticket.user.id == current_user.id:
            db.session.delete(ticket)
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            return redirect(url_for("main.index"))
    else:
        ticket = Ticket(date=date, time=time, user_id=current_user.id)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("main.index"))