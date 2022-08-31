import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import dash_bootstrap_components as dbc

from app import app
netflix_df = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles.csv')

def clean_netflix_df(df):
    df["date_added"] = pd.to_datetime(df['date_added'])
    df['month_added'] = df['date_added'].dt.month
    df['month_name_added'] = df['date_added'].dt.month_name()
    df['year_added'] = df['date_added'].dt.year
    netflix_df['count'] = 1
    return df


netflix_df = clean_netflix_df(netflix_df)


def fig_pie_purst():
    fig_purst = px.sunburst(netflix_df[netflix_df['year_added'] >= 2018], path=['year_added', 'month_name_added'],
                            values='count', color_continuous_scale='armyrose')
    fig_purst.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13, color='#8a8d93'),
        hoverlabel=dict(bgcolor="#444", font_size=10,
                        font_family="Lato, sans-serif"),
        margin=dict(t=100, b=0, l=0, r=0)

    )
    fig_purst.update_layout(title_font=dict(size=20, color='red',
                                      family="Lato, sans-serif")
                      )
    return fig_purst


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='purst_fig', figure=fig_pie_purst(), className="growHover")
        ])
    ])
])
