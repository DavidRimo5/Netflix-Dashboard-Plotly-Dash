from dash import dcc, html, ctx
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from app import app
df = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'])
df['duration'] = df['duration'].str.replace(r'\D', '')
df["duration"] = pd.to_numeric(df["duration"], errors='coerce')

def linegraph(lineGraph):
    df_line = df[(df['type'] == lineGraph)]
    df_line['type1'] = df_line['type']
    df_line1 = df_line.groupby(['release_year', 'type1'])['type'].count().reset_index()
    return df_line1


mov_line1 = linegraph('Movie')
show_line1 = linegraph('TV Show')


def linegraph2(lineGraph):
    df_line = df[(df['type'] == lineGraph)]
    df_avg = pd.pivot_table(df_line, values='duration', index='release_year', aggfunc='mean')
    return df_avg


mov_line2 = linegraph2('Movie')
show_line2 = linegraph2('TV Show')

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Button(
                'Movie', id='btn_1', n_clicks=0, className="me-1"
            ),
            dbc.Button(
                'Tv Show', id='btn_2', n_clicks=0, className="me-1"
            ),
            dcc.Slider(id='slider_year',
                       included=True,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min=1925,
                       max=2020,
                       step=1,
                       value=2015,
                       marks={str(yr): str(yr) for yr in range(1925, 2020, 10)},
                       className='dcc_compon'),
        ], xs=10, sm=10, md=10, lg=12, xl=12),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='avg_graph', className="growHover", config={
                           'displayModeBar': False
                       }),
        ], xs=10, sm=10, md=10, lg=12, xl=12),
    ])

], className="container-fluid")


@app.callback(
    Output('avg_graph', 'figure'),
    [
        Input('slider_year', 'value'),
        Input('btn_1', 'n_clicks'),
        Input('btn_2', 'n_clicks')
    ]
)
def update_graph(slider_year, button1, button2):
    line_mov = lambda line: (line[(line.release_year >= slider_year)])
    line_mov = line_mov(mov_line1)
    line_mov2 = lambda lines: (lines[lines.index >= slider_year])
    line_mov2 = line_mov2(mov_line2)
    line_show = lambda line: (line[(line.release_year >= slider_year)])
    line_show = line_show(show_line1)
    line_show2 = lambda lines: (lines[lines.index >= slider_year])
    line_show2 = line_show2(show_line2)


    def updateline(line1, line2, typeName):
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=line1['release_year'],
            y=line1['type'],
            mode='markers+lines',
            name=typeName,
            line=dict(shape="spline", smoothing=1.3, width=3, color='green'),
            marker=dict(size=10, symbol='circle', color='white',
                        line=dict(color='orange', width=2)
                        )
        ), secondary_y=False)

        fig.add_trace(go.Scatter(
            x=line2.index,
            y=line2['duration'],
            mode='markers+lines',
            name='Avg Duration',
            line=dict(shape="spline", smoothing=1.3, width=3, color='#FF00FF'),
            marker=dict(size=10, symbol='circle', color='white',
                        line=dict(color='#FF00FF', width=2)
                        )
        ), secondary_y=True)
        fig.update_layout(title_text="Total Number of {} released with Avg Duration".format(typeName),
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)',
                 title={
                    'y': 0.98,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                 titlefont={
                            'color': 'white',
                            'size': 15},
                 hovermode='x',

                 xaxis=dict(title='<b>Card Category</b>',
                            showline=False,
                            showgrid=False,
                            linecolor='white',
                            linewidth=1,


                    ),
                 yaxis=dict(title='<b>Count</b>',
                            color='white',
                            showline=False,
                            showgrid=False,
                            linecolor='white',

                    ),
                legend = {
                    'orientation': 'h',
                    'bgcolor': 'rgba(0,0,0,0)',
                    'x': 0.5,
                    'y': 1.25,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                font = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'white')
        ),
        fig.update_xaxes(title_text="Year", showgrid=False,)
        fig.update_yaxes(
            title_text="Total no of {}".format(typeName) ,
            secondary_y=False)
        fig.update_yaxes(
            title_text="Average Duration",
            secondary_y=True)
        return fig
    movie_line = updateline(line_mov, line_mov2, 'Movie')
    show_line = updateline(line_show, line_show2, 'TV Show')
    def selected_path(button1, button2):
        if 'btn_1' == ctx.triggered_id:
            return movie_line
        if 'btn_2' == ctx.triggered_id:
            return show_line
        else:
            return movie_line
    return selected_path("btn_1", "btn_2")

