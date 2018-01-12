# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, Response, redirect
from config import Config
from forms import LoginForm

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
        return render_template('boiling.html')

    #default
    return render_template('main_template.html',form=form)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)


    # if request.method == 'POST':
    #     #press button via gpio
    #     from subprocess import Popen,PIPE,STDOUT
    #     # Popen(["python", "piservo.py"],stdout=PIPE)
    #     # #say message
    #     # try:
    #     #     from subprocess import DEVNULL
    #     # except ImportError:
    #     #     import os
    #     #     DEVNULL = open(os.devnull, 'wb')

    #     # text = "Your kettle is on"
    #     # p = Popen(['espeak', '-b', '1'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    #     # p.communicate(text)

    #     return render_template('boiling.html')
        
    # else: