from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        #press button via gpio
        from subprocess import call
        call(["python", "piservo.py"])
        return '<h1> The kettle is now on!</h1>'
        
    else:
        return render_template('main_template.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
