

def get_database():
    from flask import current_app
    return current_app.config['DATABASE']

def is_testing():
    from flask import current_app
    return current_app.config['TESTING']