from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data=[]
        data[0] = request.form['ssid']
        data[1] = request.form['username']
        data[2] = request.form['password']
        data[3] = request.form['domain']
        data[4] = request.form['port']
        with open("wifi_client.dat",mode="w") as f:
            f.writelines(data)
        return True
    return render_template('form.html')

app.run(host="0.0.0.0",port=5000,debug=True)
