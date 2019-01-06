from flask import Flask, render_template, request
from openpyxl import load_workbook

app = Flask(__name__)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with werkzeug server")
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "Shutting server down..."


@app.route('/')
def index():
    read_temps = load_workbook('logged_temps.xlsx', read_only=True)
    sheet = read_temps.active
    avg_24h = sheet['A1'].value
    avg_7d = sheet['A2'].value
    avg_30d = sheet['A3'].value
    return render_template('cold_reading.html', avg_24=avg_24h, avg_7=avg_7d, avg_30=avg_30d)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.157')
