from flask import Flask

app = Flask(__name__)

@app.route('/')
def getInit():  
  return 'Estoy vivo'


@app.route('/ping')
def getPing():  
  return 'pong'

if __name__ == '__main__':
  app.run(debug=False, port=4000)