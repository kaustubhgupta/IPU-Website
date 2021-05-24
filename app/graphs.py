import plotly
import plotly.graph_objs as go
import json


def sgpa_Graph(sgpas):
    fig_batch = {
        'data': [
            go.Scatter(
                x=tuple(sgpas.keys()),
                y=tuple(sgpas.values()),
                mode='lines+markers',
                marker_line_width=2,
                marker_size=10,
                hovertemplate = "SGPA: %{y}<br>Semester: %{x}<extra></extra>"
            )],

        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': 'SGPAs'},
            title='CGPA over semesters',
            yaxis_range=[1, 11],
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            hovermode='closest',
            xaxis_tickangle=-28,
            font=dict(size=15)

        )}
    graphJSON = json.dumps(fig_batch, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def percentage_Graph(percentages):
    fig_batch = {
        'data': [
            go.Scatter(
                x=tuple(percentages.keys()),
                y=tuple(percentages.values()),
                mode='lines+markers',
                marker_line_width=2,
                marker_size=10,
                hovertemplate = "Percentage: %{y}<br>Semester: %{x}<extra></extra>"
            )],

        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': 'Percents'},
            title='Percentage over semesters',
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            hovermode='closest',
            xaxis_tickangle=-28,
            font=dict(size=15)

        )}
    graphJSON = json.dumps(fig_batch, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON