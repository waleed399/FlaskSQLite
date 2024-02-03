
from database import app
from views.routes import setup_routes


if __name__ == '__main__':

    setup_routes()
    app.run(debug=True)


