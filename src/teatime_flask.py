

from flask import Flask, render_template, request,Response


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        #press button via gpio
        from subprocess import Popen,PIPE,STDOUT
        Popen(["python", "piservo.py"],stdout=PIPE)
        #say message
        try:
            from subprocess import DEVNULL
        except ImportError:
            import os
            DEVNULL = open(os.devnull, 'wb')

        text = "Your kettle is on"
        p = Popen(['espeak', '-b', '1'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        p.communicate(text)

        return render_template('boiling.html')
        
    else:
        return render_template('main_template.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
