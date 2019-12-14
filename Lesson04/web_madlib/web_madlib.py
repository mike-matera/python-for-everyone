import os 
from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def start_madlib():
    if request.method == 'POST':
        noun = request.form.get('noun', '')
        verb = request.form.get('verb', '')
        adjective = request.form.get('adjective', '')

        # Mad Lib is in the environment variable MADLIB
    
        madlib = "Complete Me!"
        
        return render_template('madlib.html', noun=noun, verb=verb, 
            adjective=adjective, madlib=madlib)

    return render_template('madlib.html')

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8080, debug=True)