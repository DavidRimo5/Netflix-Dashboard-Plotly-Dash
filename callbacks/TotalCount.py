from dash import dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date, timedelta

from app import app
df = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles.csv')
df['date_added'] = pd.to_datetime(df['date_added'])


def count(typeName):
    df_type = df[df['type'] == typeName]
    df_type = df_type.groupby(['type', 'date_added']).size().reset_index(name='count')
    return df_type

df_mov = count('Movie')
df_show = count('TV Show')

# className='shadow-lg p-3 mb-5 bg-white rounded, mb-4'
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("Select the start date", style={'color': 'white'}),
            dcc.DatePickerSingle(
                id="my_start_date",
                min_date_allowed=date(2008, 1, 1),
                max_date_allowed=date(2021, 9, 21),
                initial_visible_month=date(2018, 11, 25),
                date=date(2018, 11, 25)
            )
        ],),
        dbc.Col([
            html.H5("Select the end date", style={'color': 'white'}),
            dcc.DatePickerSingle(
                id="my_end_date",
                min_date_allowed=date(2008, 1, 1),
                max_date_allowed=date(2021, 9, 21),
                initial_visible_month=date(2019, 1, 27),
                date=date(2019, 1, 27)
            )
        ], className="date_picker"),
    ], justify='center'),
    html.Br(),
    html.Br(),
    # No of movies and show w.r.t date picker
    dbc.Row([
        dbc.Col([  # No of Movie
            dbc.Card([
                dbc.CardBody([
                    html.H6('No of Movies', style={'textAlign': 'center'}),
                    html.H4(id='total_movies', style={'textAlign': 'center', 'fontWeight': 'bold'}),
                    html.H5(id='total_pct_mov', style={'textAlign': 'center', "color": 'green', "font-family": 'Brush Script MT'})
                ])
            ], className="totalCount")
        ]),
        dbc.Col([  # No of Shows
            dbc.Card([
                dbc.CardBody([
                    html.H6('No of Shows', style={'textAlign': 'center'}),
                    html.H4(id='total_shows', style={'textAlign': 'center', 'fontWeight': 'bold'}),
                    html.H5(id='total_pct_show', style={'textAlign': 'center', "color": 'green', "font-family": 'Brush Script MT'})
                ])
            ], className="totalCount")
        ]),
    ], justify='around'),
])


@app.callback(
    Output('total_movies', 'children'),
    Output('total_shows', 'children'),
    Output('total_pct_mov', 'children'),
    Output('total_pct_show', 'children'),
    [
        Input('my_start_date', 'date'),
        Input('my_end_date', 'date')
    ],
)
def update_count(start_date, end_date):
    df_selected = df_mov[((df_mov.date_added >= start_date) & (df_mov.date_added <= end_date))]
    total_mov_count = df_selected['count'].sum()

    df_selected = df_show[((df_show.date_added >= start_date) & (df_show.date_added <= end_date))]
    total_show_count = df_selected['count'].sum()

    start_date = pd.to_datetime(start_date, format='%Y/%m/%d')
    end_date = pd.to_datetime(end_date, format='%Y/%m/%d')
    total_days = (end_date - start_date).days
    reverse_date = start_date - timedelta(days=total_days)

    selected_rev = df_mov[((df_mov.date_added >= reverse_date) & (df_mov.date_added <= start_date))]
    rev_mov_count = selected_rev['count'].sum()
    selected_rev = df_show[((df_show.date_added >= reverse_date) & (df_show.date_added <= start_date))]
    rev_show_count = selected_rev['count'].sum()

    pct_mov = total_mov_count / rev_mov_count * 100
    formatted_pct_mov = '{0:.2f}'.format(pct_mov)
    pct_show = total_show_count / rev_show_count * 100
    formatted_pct_show = '{0:.2f}'.format(pct_show)
    pct1 = f"{formatted_pct_mov}% Increase"
    pct2 = f"{formatted_pct_show}% Increase"

    return total_mov_count, total_show_count, pct1, pct2
