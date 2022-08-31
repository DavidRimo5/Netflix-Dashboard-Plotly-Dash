import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from app import app

df_c = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_C.csv')
df_g = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_G.csv')

def pieGraph(pieType):
    df_cast1 = df_c[df_c['type'] == pieType]
    df_cast = df_cast1['cast']
    df_genre = df_g[df_g['type'] == pieType]
    df_genre = df_genre['listed_in']
    df_new = pd.concat([df_cast, df_genre], axis=1)
    df_new = df_new.dropna()
    df_new1 = df_new.groupby(['listed_in', 'cast']).size().reset_index(name='count')
    df_pie = df_new1.sort_values('count', ascending=False)
    return df_pie


pie_mov = pieGraph('Movie')
pie_show =pieGraph('TV Show')


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Cast's performed Movie Genre", style={'textAlign': 'center', 'color': 'red', 'fontWeight': 'bold'}),
            html.P("Cast Names:", style={'color': 'white'}),
            dcc.Dropdown(id='cast_mov_names',
                         options=[{'label': i, 'value': i}
                                  for i in pie_mov['cast'].unique()],
                         value=' Rajesh Kava', clearable=True,
                         style={'color': 'green', 'width': "70%"}),
            dcc.Graph(id="pie_graph_mov", className="growHover", config={
                           'displayModeBar': False}),
        ], style={"background-color": 'rgba(0,0,0,0)'}, width=6),
        dbc.Col([
            html.H4("Cast's performed TV Show Genre", style={'textAlign': 'center', 'color': 'red', 'fontWeight': 'bold'}),
            html.P("Cast Names:", style={'color': 'white'}),
            dcc.Dropdown(id='cast_show_names',
                         options=[{'label': i, 'value': i}
                                  for i in pie_show['cast'].unique()],
                         value=' Koji Yusa', clearable=True,
                         style={'color': 'green', 'width': "70%"}),
            dcc.Graph(id="pie_graph_show", className="growHover", config={
                           'displayModeBar': False}),
        ], style={"background-color": 'rgba(0,0,0,0)'}, width=6)
    ], justify='around')
], className="container-fluid")


@app.callback(
    [
        Output("pie_graph_mov", "figure"),
        Output("pie_graph_show", "figure"),
    ],
    [
        Input("cast_mov_names", "value"),
        Input("cast_show_names", "value")
    ])
def generate_chart(mov_name, show_name):
    cast1 = lambda cast: cast[cast['cast'] == mov_name]
    cast_mov = cast1(pie_mov)
    cast2 = lambda cast: cast[cast['cast'] == show_name]
    cast_show = cast2(pie_show)


    def pieChart(self, typeName):
        fig_pie = px.pie(self, values='count',
                         hover_data=['listed_in'],
                         labels={'count': 'No of {}'.format(typeName),
                                 'listed_in': 'Genre'}, hole=.7)
        fig_pie.update_layout(
                              showlegend=True,
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              font=dict(size=17, color='#8a8d93'),
                              hoverlabel=dict(bgcolor="#444", font_size=13,
                                              font_family="Lato, sans-serif"))
        return fig_pie

    movie_pie_fig = pieChart(cast_mov, 'Movie')
    show_pie_fig = pieChart(cast_show, 'TV Show')

    return movie_pie_fig, show_pie_fig
