from flask import Flask, request

app = Flask(__name__)

@app.route('/tg', methods=['GET', 'POST'])
def test():
    print(request)
    return ''


app.run(debug=True)
