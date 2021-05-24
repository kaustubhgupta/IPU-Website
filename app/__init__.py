from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['semesters'] = [{'name': '1st'}, {'name': '2nd'}, {'name': '3rd'}, {
        'name': '4th'}, {'name': '5th'}, {'name': '6th'}, {'name': '7th'}, {'name': '8th'}]
    app.config['branch'] = [{'name': 'CSE'}, {'name': 'IT'}, {
        'name': 'ECE'}, {'name': 'EEE'}, {'name': 'MAE'}]
    app.config['batches'] = [{'name': '2017-2021'},
                             {'name': '2018-2022'}, {'name': '2019-2023'}]
    app.config['colleges'] = [
        {'name': 'Whole University'},
        {'name': 'AIACTR'},
        {'name': 'AMITY'},
        {'name': 'BMCEM'},
        {'name': 'BPIT'},
        {'name': 'BVCOE'},
        {'name': 'BMIET'},
        {'name': 'CBPGEC'},
        {'name': 'DITE'},
        {'name': 'DTC'},
        {'name': 'GBPGEC'},
        {'name': 'GTBIT'},
        {'name': 'HMR'},
        {'name': 'JIMS'},
        {'name': 'MAIT'},
        {'name': 'MSIT'},
        {'name': 'MSWAMI'},
        {'name': 'NPTI'},
        {'name': 'NIEC'},
        {'name': 'GNNT'},
        {'name': 'DITM'}, ]

    app.config['branches'] = [{'name': 'All Branch'}, {'name': 'CSE'}, {
        'name': 'IT'}, {'name': 'ECE'}, {'name': 'EEE'}, {'name': 'MAE'}]
    app.config['tops'] = [{'name': 'Top 10'}, {
        'name': 'Top 50'}, {'name': 'Top 100'}]

    with app.app_context():

        from app import views
        from .dashboard.dashboard import create_dashboard
        app = create_dashboard(app)

    return app
