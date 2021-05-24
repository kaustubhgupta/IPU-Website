from dash.dependencies import Input, Output
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import requests
import json
import os
# from dotenv import load_dotenv
# load_dotenv()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


url = "https://ipubackendapi.herokuapp.com/fetchStats"

headers = {'Authorization': 'Bearer {}'.format(os.environ['API_KEY'])}
received = requests.request("GET", url, headers=headers)
data = received.json()['result']

def create_dashboard(server):

    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=external_stylesheets
    )

    dash_app.layout = html.Div(children=[

        html.Center(children=[
            html.H1(children='Analytics Dashboard')]),
            html.Div(children=[
                html.Center(children=[
                    html.H3(children='College Statistics(Average Score)')]),
                    dcc.Dropdown(
                        id='batch-dropdown',
                        options=[
                            {'label': '2017-2021', 'value': '17'},
                            {'label': '2018-2022', 'value': '18'},
                            {'label': '2019-2023', 'value': '19'}
                        ],
                        value='17',
                        placeholder="Select Batch",
                        style={'width': "45%",
                            'display': 'inline-block',
                            'verticalAlign': "middle",
                            },
                        searchable=False,
                        multi=False
                    ),
                    dcc.Dropdown(
                        id='semester-dropdown',
                        options=[
                            {'label': '1st', 'value': '1'},
                            {'label': '2nd', 'value': '2'},
                            {'label': '3rd', 'value': '3'},
                            {'label': '4th', 'value': '4'},
                            {'label': '5th', 'value': '5'},
                            {'label': '6th', 'value': '6'},
                            {'label': '7th', 'value': '7'},
                            {'label': '8th', 'value': '8'},
                        ],
                        value='1',
                        placeholder="Select Semester",
                        style={'width': "45%",
                            'display': 'inline-block',
                            'verticalAlign': "middle"},
                        searchable=False
                    )]),

            html.Div(children=[
                dcc.Dropdown(id='branch-select',
                            placeholder="Select Branch",
                            options=[
                                {'label': 'CSE', 'value': 'CSE'},
                                {'label': 'IT', 'value': 'IT'},
                                {'label': 'MAE', 'value': 'MAE'},       
                                {'label': 'EEE', 'value': 'EEE'},
                                {'label': 'ECE', 'value': 'ECE'}
                            ],
                            value='CSE',
                            style={'width': "45%",
                                    'display': 'inline-block',
                                    'verticalAlign': "middle"},
                            searchable=False
                            ),

                dcc.Dropdown(id='column-select',
                            value='Percentage',
                            style={'width': "45%",
                                    'display': 'inline-block',
                                    'verticalAlign': "middle",
                                    'optionHeight': 120},
                            searchable=False,
                            optionHeight=70,
                            ),

                dcc.Graph(id='final-graph',
                            style={
                            "margin-right": "auto",
                            "margin-left": "auto"
                        }
            )
        ])
    ], 
    
    style={
        'textAlign': 'center',
        })

    init_callbacks(dash_app)
    return dash_app.server

def init_callbacks(dash_app):


    @dash_app.callback(Output(component_id='final-graph', component_property='figure'),
                       [Input(component_id='batch-dropdown', component_property='value'),
                        Input(component_id='semester-dropdown', component_property='value'),
                        Input(component_id='branch-select', component_property='value'),
                        Input(component_id='column-select', component_property='value')
                        ]
                       )
    def update_graph(batch, semester, branch, subject):
        
        searchKey = semester + batch + branch
        try:
            displaySubjectColumns = data[searchKey]['subjects']

            if subject not in displaySubjectColumns:
                subject = 'Percentage'

            marksData = json.loads(data[searchKey]['averageMarks'])
            dataset = pd.DataFrame.from_dict(marksData, orient='index')
            values = dataset[subject].apply(lambda x: round(x, 0))

            graph = px.bar(
                x=dataset.index,
                y=values,
                color=dataset[subject],
                text=values,
                color_continuous_scale='Bluered',
                labels={'color': ''}
            )
            graph.update_layout(
                    xaxis_title='Colleges',
                    yaxis_title=subject,
                    xaxis_tickangle=-40,
                    yaxis={'visible': False, 'showticklabels': False},
                    font=dict(size=15),
                )

            return graph

        except:

            graph = ''
            return graph


    @dash_app.callback([Output(component_id='branch-select', component_property='disabled'),
                        Output(component_id='branch-select', component_property='value')],
                       [Input(component_id='semester-dropdown', component_property='value')])
    def update_branch(semester):

        if semester in ['1', '2']:
            return True, 'All'
        else:
            return False, 'CSE'


    @dash_app.callback(Output(component_id='column-select', component_property='options'),
                       [Input(component_id='semester-dropdown', component_property='value'),
                        Input(component_id='branch-select', component_property='value'),
                        Input(component_id='batch-dropdown', component_property='value')])
    def update_options(semester, branch, batch):

        if semester in ['1', '2']:
            branch = 'All'

        searchKey = semester + batch + branch
        try:
            displaySubjectColumns = data[searchKey]['subjects']
            sentColumns = [{'label': i, 'value': i} for i in displaySubjectColumns]
            sentColumns.append({'label': 'Percentage', 'value': 'Percentage'})

            return sentColumns

        except:

            return {'label': 'Percentage', 'value': 'Percentage'}