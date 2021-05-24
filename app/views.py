import pandas as pd
import requests
import os
import json
from app.graphs import *
from flask import current_app as app
from flask import render_template, request, redirect, abort
# from dotenv import load_dotenv
# load_dotenv()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/creator')
def contact():
    return render_template('creator.html')


@app.route('/')
def home():
    return render_template('index.html', batches=app.config['batches'], semesters=app.config['semesters'])


@app.route('/profile')
def profile():
    return render_template('profile.html', batches=app.config['batches'], semesters=app.config['semesters'])


@app.route('/portal', methods=['GET', 'POST'])
def portal():
    rollNo = 0
    batch = '2018-2022'
    semester = '1st'
    if request.method == 'POST':
        rollNo = request.form.get('rollNo')
        batch = request.form.get('batch-select')
        semester = request.form.get('semester-select')
        url = "https://ipubackendapi.herokuapp.com/score?eNumber={}&semester={}&batch={}".format(
            rollNo, semester[0], batch[2:4])
        headers = {'Authorization': 'Bearer {}'.format(os.environ['API_KEY'])}
        received = requests.request("GET", url, headers=headers)
        data = received.json()
        if data['result'] is not None:
            marks = [(i, j, k, z, t) for i, j, k, z, t in zip(data['result']['subjects'], data['result']['int_marks'],
                                                              data['result']['ext_marks'], data['result']['total_marks'], data['result']['grade_points'])]
            df = pd.DataFrame(
                marks, columns=['Subjects', 'Internals', 'Externals', 'Total', 'Grade Points'])
            return render_template('marksheet.html', marksTable=df.to_html(index=False), name=data['result']['name'],
                                   semester=semester, college=data['result'][
                                       'college_name'], branch=data['result']['branch_name'],
                                   percentage=data['result']['percentage'], sgpa=data['result']['sgpa'],
                                   college_overall_rank=(
                                       data['result']['ranks']['college_rank'], data['result']['ranks']['college_total']),
                                   college_branch_rank=(
                                       data['result']['ranks']['college_branch_rank'], data['result']['ranks']['college_branch_total']),
                                   university_overall_rank=(
                                       data['result']['ranks']['uni_rank'], data['result']['ranks']['uni_total']),
                                   university_branch_rank=(
                                       data['result']['ranks']['uni_branch_rank'], data['result']['ranks']['uni_branch_total']),
                                   total_marks=(df['Total'].sum(), len(df['Subjects'])*100))
        else:
            abort(404)

    else:
        abort(404)


@app.route('/profile-gen', methods=['GET', 'POST'])
def profile_render():
    rollNo = 0
    batch = '2018-2022'
    semester = '1st'
    if request.method == 'POST':
        rollNo = request.form.get('rollNo')
        batch = request.form.get('batch-select')
        semester = request.form.get('semester-select')
        if semester[0] != '1':
            result_semester = str(int(semester[0])-1)
        else:
            result_semester = '1'
        url = "https://ipubackendapi.herokuapp.com/profile?eNumber={}&last_result_semester={}&batch={}".format(
            rollNo, result_semester, batch[2:4])
        headers = {'Authorization': 'Bearer {}'.format(os.environ['API_KEY'])}
        received = requests.request("GET", url, headers=headers)
        data = received.json()
        curr_sem = int(result_semester)
        parsed_data = []
        cgpa = 0
        count = 0
        percentage_ = 0
        sgpas = {}
        percentages = {}
        while(curr_sem != 0):
            for key, value in data['result'].items():
                searchKey = 'semester_{}'.format(curr_sem)
                if searchKey == key:
                    if value is not None:
                        marks = [(i, j, k, z, t) for i, j, k, z, t in zip(
                            value['subjects'], value['int_marks'], value['ext_marks'], value['total_marks'], value['grade_points'])]
                        df = pd.DataFrame(
                            marks, columns=['Subjects', 'Internals', 'Externals', 'Total', 'Grade Points'])
                        parsed_data.append((curr_sem, df.to_html(
                            index=False), value['sgpa'], value['percentage']))
                        cgpa += value['sgpa']
                        sgpas['Semester ' + str(curr_sem)] = value['sgpa']
                        percentages['Semester ' +
                                    str(curr_sem)] = value['percentage']
                        percentage_ += value['percentage']
                        count += 1
                    else:
                        continue

            curr_sem -= 1
        cgpa_final = round((cgpa/count), 2)
        percentage_final = round((percentage_/count), 2)
        sgpas = dict(reversed(list(sgpas.items())))
        sgpa_plot = sgpa_Graph(sgpas)
        percentages = dict(reversed(list(percentages.items())))
        percentage_plot = percentage_Graph(percentages)
        return render_template('profile_render.html', name=data['result']['name'], sgpa_plot=sgpa_plot, percentage_plot=percentage_plot,
                               college=data['result']['college_name'], branch=data['result']['branch_name'], parsed_data=parsed_data, cgpa=cgpa_final, percentage_final=percentage_final)

    else:
        abort(404)


@app.route("/Ranks", methods=['GET', 'POST'])
def ranks():
    batch = '2018-2022'
    semester = '1st'
    branch = 'All Branch'
    college_uni = 'Whole University'
    top = 10
    if request.method == 'POST':
        batch = request.form.get('batch-select')
        semester = request.form.get('semester-select')
        top = request.form.get('top-select')
        college_uni = request.form.get('college-uni-select')
        branch = request.form.get('branch-select')
        url = "https://ipubackendapi.herokuapp.com/fetchRanks?semester={}&batch={}&top={}&college_uni={}&branch={}".format(
            semester[0], batch[2:4], int(top[4:]), college_uni, branch)
        headers = {'Authorization': 'Bearer {}'.format(os.environ['API_KEY'])}
        received = requests.request("GET", url, headers=headers)
        data = received.json()['result']

        if data != None:
            data = json.loads(data)
            data = pd.DataFrame.from_dict(data, orient='index')
            data.reset_index(inplace=True)
            data.rename(columns={'index': 'Rank',
                                 'Percentage': '%'}, inplace=True)
            data['Rank'] = data['Rank'].astype(int)
            data['Rank'] = data['Rank'].apply(lambda x: x+1)
            data.set_index('Rank')

            if data.shape[0] != 0:

                return render_template('ranks.html', tops=app.config['tops'], branches=app.config['branches'], batches=app.config['batches'], semesters=app.config['semesters'], colleges=app.config['colleges'], data=data.to_html(index=False), message=f'{top} students in batch {batch}, <br>for {semester} semester, <br>in {college_uni}, <br>& from {branch} are:')

            else:
                return render_template('ranks.html', tops=app.config['tops'], branches=app.config['branches'], batches=app.config['batches'], semesters=app.config['semesters'], message='No data found!', colleges=app.config['colleges'], )

        else:
            return render_template('ranks.html', tops=app.config['tops'], branches=app.config['branches'], batches=app.config['batches'], semesters=app.config['semesters'], message='No data found!', colleges=app.config['colleges'], )

    return render_template('ranks.html', tops=app.config['tops'], branches=app.config['branches'], batches=app.config['batches'], semesters=app.config['semesters'], colleges=app.config['colleges'], )
