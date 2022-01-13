from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

@app.route('/')
def getInit():  
  return 'Estoy vivo'


@app.route('/ping')
def getInit():  
  return 'pong'

if __name__ == '__main__':
  app.run(debug=True, port=4000)