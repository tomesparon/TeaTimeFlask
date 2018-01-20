# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
from crontab import CronTab
import sys
import signal
import json

from flask import Flask, render_template, request, Response, redirect, make_response
from config import Config
from forms import LoginForm

import temperature
from time import time

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def mainpage():
    form = LoginForm()
    if form.validate_on_submit():
        text = form.name.data
        #press button via gpio
        from subprocess import Popen,PIPE,STDOUT
        Popen(["python", "piservo.py"],stdout=PIPE)
        #say message
        try:
            from subprocess import DEVNULL
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')
        text = "Your kettle is On, MR " + text
        p = Popen(['espeak', '-b', '1'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        p.communicate(text)
        return render_template('temperature.html')

    #default
    return render_template('main_template.html',form=form)

## temperature views

@app.route('/temperature')
def hello_world():
    return render_template('temperature.html', data='test')

## called by js highcharts every 8sec
@app.route('/live-data')
def live_data():
    temp = temperature.read_temp()
    # Create a PHP?? array and echo it as JSON
    data = [time() * 1000, temp]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


## alarm view routes start


def lookup_alarms():
    cron = CronTab(user="pi")
    return [str(job) for job in cron if job.is_enabled()]

def lookup_sounds():
    return  [x.split(".")[0] for x in os.listdir('/home/pi/projects/django-rpi/TeaTimeFlask/src/alarm/sounds')]

@app.route("/schedule")
def hello():
    """
    entry point


    :return: returns basic "hello world" string
    """
    sounds = lookup_sounds()
    scheduled = [ x.split() for x in lookup_alarms()]
    data = {"sounds":sounds, "scheduled":scheduled}
    return render_template("scheduler.html", **data)

@app.route("/remove_alarms")
def remove_alarms():
    cron = CronTab(user="pi")
    print "removing"
    for job in cron:
        print job
        cron.remove( job )
    cron.write()
    
    return "<h1>ALarms reset</h1>"

@app.route("/running_alarms")
def running_alarms():
    """
    gets list of running alarms
    :return: returns list of running alarms
    """
    return json.dumps(os.listdir('/home/pi/projects/django-rpi/TeaTimeFlask/src/alarm/alarms'))

@app.route("/set_alarm/<newalarm>")
def set_alarm(newalarm):
    """
    sets and alarm
    :param newalarm: a string representing the alarm to dset
    :return: returns success or failure base on data
    """
    print "got back", newalarm
    days, hours, sound = newalarm.split("-")
    if not days or not hours or not sound:
        return json.dumps("Failure")

    #determine days
    day_string = []
    for x in days:
        if x == "U":
            day_string.append(0)
        elif x == "M":
            day_string.append(1)
        elif x == "T":
            day_string.append(2)
        elif x == "W":
            day_string.append(3)
        elif x == "R":
            day_string.append(4)
        elif x == "F":
            day_string.append(5)
        elif x == "S":
            day_string.append(6)
        else:
            return json.dumps("Failure")

    times = hours.split(":")

    for day in day_string:

        cron = CronTab(user="pi")
        job = cron.new(command='/home/pi/projects/django-rpi/TeaTimeFlask/src/alarm/alarm.py {0}'.format(sound))
        job.dow.on(day)

        #determine hours
        job.hour.on(times[0])
        job.minute.on(times[1])
        #create new cron
        if job.is_valid():
            job.enable()
            cron.write()

    return json.dumps("success")

@app.route("/get_alarms")
def get_alarms():
    return json.dumps(lookup_alarms())

@app.route("/sounds")
def get_sounds():
    return json.dumps(lookup_sounds())

@app.route("/kill/<int:pid>")
def kill(pid):
    try:
        os.kill(pid, signal.SIGHUP)
        return "success"
    except Exception as e:
        return str(e)

## alarm views routes

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
