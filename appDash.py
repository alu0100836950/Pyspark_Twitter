import base64
import datetime
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd

import plotly.figure_factory as ff
import plotly.graph_objs as go



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = []

app.layout = html.Div(children = [
    html.H1(
        children = 'Número de tweets por paises sobre el coronavirus', 
        style={
            'textAlign': 'center'
        }
    ), 
    dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            },
            
            multiple=True
        ),
    #Table
    html.Div(id='output-data-upload',
            style={
                'textAlign': 'center'
    }),
    
    #Graph
    html.Div(id='histogram_graph'),
           
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            
        ),
        dcc.Graph(
            id='histogram_graph',
            figure={
                'data': [
                    
                    {'x': df['Codigo_Pais'], 'y': df['Num_Tweets'], 'type': 'bar', 'name': 'Tweet/Pais'},
                ],
                'layout': go.Layout(
                
                    xaxis=dict(
                        title='Pais'
                    ),
                    yaxis=dict(
                        title='Numero de Tweets'
                    ),

                )
            }
        )

    ])

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children





if __name__ == '__main__':
    app.run_server(debug=True)
