import sys
from dash import dcc, html, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app

sys.path.insert(0, r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\Dashboard 2\callbacks')
from callbacks import functions as fn
from callbacks import TotalCount
from callbacks import LineGraph
from callbacks import Chrorpleth as ch
from callbacks import  PieChart as pie
from callbacks import country_wise as cs
from callbacks import sunbrust


app.layout = dbc.Container([
    html.H1("NETFLIX", className='title'),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            TotalCount.layout
        ], className="totalcount", width=4,),
        dbc.Col([
            dbc.Card([
                dbc.Col([html.H6("Total Movie"),fn.total_mov], className="total mt-3"),
                dbc.Col([html.H6("Total TV Show"), fn.total_show], className="total"),
                dbc.Col([html.H6("Total Director"), fn.total_dir], className="total"),
                dbc.Col([html.H6("Total Cast"), fn.total_cast], className="total"),
            ], className="bg-transparent align-content-center"),
        ]),
        dbc.Col([
            cs.layout
        ]),
    ], justify='around', align="center"),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            LineGraph.layout
        ], width=8),
        dbc.Col([
            dcc.Graph(figure=fn.fig_donut, className="donut growHover")
        ], xs=10, sm=10, md=10, lg=4, xl=4)
    ], align="center"),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fn.mov_rating_fig, className="growHover")
        ], xs=10, sm=10, md=10, lg=4, xl=4),
        dbc.Col([
            dcc.Graph(figure=fn.show_rating_fig, className="growHover")
        ], xs=10, sm=10, md=10, lg=4, xl=4),
        dbc.Col([
            dcc.Graph(figure=fn.fig_country, className="growHover")
        ], xs=10, sm=10, md=10, lg=4, xl=4)
    ], justify="center", align="center"),
    html.Br(),
    html.Br(),
    dbc.Button(
            'Movie', id='btn1', n_clicks=0, className="btn"
        ),
    dbc.Button(
            'Tv Show', id='btn2', n_clicks=0, className="btn"
        ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id = "2ndGraph", className="growHover")
                ])
            ], style={"background-color": 'rgba(0,0,0,0)'})
        ], xs=10, sm=10, md=10, lg=6, xl=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id = "3rdGraph", className="growHover"),
                ])
            ], style={"background-color": 'rgba(0,0,0,0)'})
        ], xs=10, sm=10, md=10, lg=6, xl=6)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            ch.layout
        ])
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    pie.layout
                ])
            ], style={"background-color": 'rgba(0,0,0,0)'})
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Movies and Shows added in last 5 year",
                            style={'textAlign': 'center', 'color': 'red', 'fontWeight': 'bold'}),
                    sunbrust.layout
                ])
            ], style={"background-color": 'rgba(0,0,0,0)'},)
        ], width=4)
    ], justify='around'),

],style={ "background-image": 'url("/assets/bg.jpg")'}, fluid=True)
# style={'background-color': '#313236'}
@app.callback(
    Output('2ndGraph', 'figure'),
    Output('3rdGraph', 'figure'),
    [
        Input('btn1', 'n_clicks'),
        Input('btn2', 'n_clicks')
    ]
)
def selected_path(button1, button2):
    if 'btn1' == ctx.triggered_id:
        return fn.mov_dir_fig, fn.mov_cast_fig,
    if 'btn2' == ctx.triggered_id:
        return fn.show_dir_fig, fn.show_cast_fig,
    else:
        return fn.mov_dir_fig, fn.mov_cast_fig,


if __name__ == '__main__':
    app.run_server(debug=True)