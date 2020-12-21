from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['semesters'] = [{'name': '1st'}, {'name': '2nd'}, {'name': '3rd'}, {'name': '4th'}, {'name': '5th'}, {'name': '6th'}, {'name': '7th'}, {'name': '8th'}]
    app.config['branch'] = [{'name': 'CSE'}, {'name': 'IT'}, {'name': 'ECE'}, {'name': 'EEE'}, {'name': 'MAE'}]
    app.config['batches'] = [{'name': '2017-2021'}, {'name': '2018-2022'}, {'name': '2019-2023'}]
    with app.app_context():
        from app import views

    return app