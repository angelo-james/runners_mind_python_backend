from app import app

@app.route('/api/users')
def get_all_users():
    return 'Hello World'