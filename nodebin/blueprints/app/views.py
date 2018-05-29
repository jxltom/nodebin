from . import app


@app.route('/')
def index():
    return 'Welcome to Flask!'
