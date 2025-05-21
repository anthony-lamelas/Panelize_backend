# Web Server Gateway Interface
# WSGI is a specification that describes how a web server communicates with web applications

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000)