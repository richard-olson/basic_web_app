from basic_web_app import app

wsgi = app

if __name__ == "__main__":
    wsgi.run(host="0.0.0.0", port=5000)