from flask import Flask
app_finl = Flask(__name__)

@app_finl.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app_finl.run()
