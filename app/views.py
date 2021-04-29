import pandas as pd
import requests
import os
from flask import current_app as app
from flask import render_template, request, redirect, abort


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
        if semester[0] !='1':
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
        while(curr_sem!=0):
            for key, value in data['result'].items():
                searchKey = 'semester_{}'.format(curr_sem)
                if searchKey == key:
                    if value is not None:
                        marks = [(i, j, k, z, t) for i, j, k, z, t in zip(value['subjects'], value['int_marks'], value['ext_marks'], value['total_marks'], value['grade_points'])]
                        df = pd.DataFrame(marks, columns=['Subjects', 'Internals', 'Externals', 'Total', 'Grade Points'])
                        parsed_data.append((curr_sem, df.to_html(index=False), value['sgpa'], value['percentage']))
                        cgpa += value['sgpa']
                        percentage_ += value['percentage']
                        count += 1
                    else:
                        continue
                    
            curr_sem -= 1
        cgpa_final = round((cgpa/count), 2)
        percentage_final = round((percentage_/count), 2)
        return render_template('profile_render.html', name=data['result']['name'],
                            college=data['result']['college_name'], branch=data['result']['branch_name'], parsed_data=parsed_data, cgpa=cgpa_final, percentage_final=percentage_final)

    else:   
        abort(404)
