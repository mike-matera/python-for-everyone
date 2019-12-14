from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    a = 1
    b = 1
    if request.method == 'POST':
        try:
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))
        except:
            return render_template('index.html', error="You gave me a bad number.",
                a=request.form.get('a'), b=request.form.get('b'))

        if b == 0:
            return render_template('index.html', error="I can't divide by zero!",
                        a=request.form.get('a'), b=request.form.get('b'))


    # Put your HTML into the table variable.
    table = '''
    '''
    
    return render_template('index.html', table=table, method=request.method, 
        error=None, a=a, b=b)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    