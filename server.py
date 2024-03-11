from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data=["","","","",""]
        data[0] = request.form['ssid'] + "\n"
        data[1] = request.form['username'] +"\n"
        data[2] = request.form['password'] + "\n"
        data[3] = request.form['domain'] + "\n"
        data[4] = request.form['port'] + "\n"

        with open("wifi_client.dat",mode="w") as f:
            f.writelines(data)

        return "OK"
    return render_template('form.html')

app.run(host="0.0.0.0",port=5000,debug=False)
