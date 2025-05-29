from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
CORS(app)

@app.route('/test', methods = ['post'])
def test() -> Response:
    context: str = str(request.get_json()['context'])
    amount: int = int(request.get_json()['amount'])
    print(context, amount)
    return jsonify({
        'code': '200',
        'message': '请求成功',
        'data': {},
        'context': f'{context}',
        'amount': f'{amount}',
    })


def main() -> None:
    srv = WSGIServer(('0.0.0.0', 8080), app)
    srv.serve_forever()


if __name__ == '__main__':
    main()