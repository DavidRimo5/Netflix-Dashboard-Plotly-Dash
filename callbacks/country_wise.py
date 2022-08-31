import pandas as pd
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
netflix_df = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles.csv')


def clean_netflix_df(df):
    df['country'] = df['country'].fillna(df['country'].mode()[0])
    df['cast'].replace(np.nan, 'No Data', inplace=True)
    df['director'].replace(np.nan, 'No Data', inplace=True)
    df.dropna(inplace=True)

    df.drop_duplicates(inplace=True)

    df["date_added"] = pd.to_datetime(df['date_added'])
    df['month_added'] = df['date_added'].dt.month
    df['month_name_added'] = df['date_added'].dt.month_name()
    df['year_added'] = df['date_added'].dt.year

    df['first_country'] = df['country'].apply(lambda x: x.split(",")[0])
    df['first_country'].replace('United States', 'United States of America', inplace=True)
    df['first_country'].replace('United Kingdom', 'UK', inplace=True)
    df['first_country'].replace('South Korea', 'S. Korea', inplace=True)

    netflix_df['count'] = 1
    df['genre'] = df['listed_in'].apply(lambda x: x.replace(' ,', ',').replace(', ', ',').split(','))
    return df


netflix_df = clean_netflix_df(netflix_df)

layout = html.Div(children=[
    html.Div(children=[
        html.Label('Movie Statistics Calculator', style={'color': 'white', 'font-size': '2rem'}),
        html.Div([
            dcc.Dropdown(id='dropDown',
                         options=[{'label': x, 'value': x} for x in netflix_df['first_country'].unique()],
                         value='Egypt',
                         clearable=False),
            html.Br(),
            html.Br(),
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Td("No. of Movies till date", className="val"),

                        html.Td([
                            html.Div(
                                id="val1", className="val "

                            )

                        ])
                    ], className="movieCalc"),
                    html.Tr([
                        html.Td("No. of TV Shows till date", className="val"),

                        html.Td([
                            html.Div(
                                id="val2", className="val"

                            )

                        ])
                    ], className="movieCalc"),
                    html.Tr([
                        html.Td("Top Actor", className="val"),

                        html.Td([
                            html.Div(
                                id="val3", className="val"

                            )

                        ])
                    ], className="movieCalc"),
                    html.Tr([
                        html.Td("Top Director", className="val"),

                        html.Td([
                            html.Div(
                                id="val4", className="val"

                            )

                        ])
                    ], className="movieCalc")
            ], className="table table-striped")
        ])
    ], className="col-md-6"),

], className="row"),
], className = "container-fluid", )
@app.callback(
    [Output('val1', 'children'), Output('val2', 'children'), Output('val3', 'children'), Output('val4', 'children')],
    Input('dropDown', 'value')
)
def updateTable(dropDown):
    dfx = netflix_df[['type', 'country']]
    dfMovie = dfx[dfx['type'] == 'Movie']
    dfTV = dfx[dfx['type'] == 'TV Show']
    dfM1 = dfMovie['country'].str.split(',', expand=True).stack()
    dfTV1 = dfTV['country'].str.split(',', expand=True).stack()
    dfM1 = dfM1.to_frame()
    dfTV1 = dfTV1.to_frame()
    dfM1.columns = ['country']
    dfTV1.columns = ['country']
    dfM2 = dfM1.groupby(['country']).size().reset_index(name='counts')
    dfTV2 = dfTV1.groupby(['country']).size().reset_index(name='counts')
    dfM2['country'] = dfM2['country'].str.strip()
    dfTV2['country'] = dfTV2['country'].str.strip()
    val11 = dfM2[dfM2['country'] == dropDown]
    val22 = dfTV2[dfTV2['country'] == dropDown]
    val11 = val11.reset_index()
    val22 = val22.reset_index()
    if val11.empty:
        val1 = 0
    else:
        val1 = val11.loc[0]['counts']

    if val22.empty:
        val2 = 0
    else:
        val2 = val22.loc[0]['counts']

    # Top Actor
    dfA = netflix_df[['cast', 'country']]
    dfA1 = dfA[dfA['country'].str.contains(dropDown, case=False)]
    dfA2 = dfA1['cast'].str.split(',', expand=True).stack()
    dfA2 = dfA2.to_frame()
    dfA2.columns = ['Cast']
    dfA3 = dfA2.groupby(['Cast']).size().reset_index(name='counts')
    dfA3 = dfA3[dfA3['Cast'] != 'No Cast Specified']
    dfA3 = dfA3.sort_values(by='counts', ascending=False)
    if dfA3.empty:
        val3 = "Actor data from this country is not available"
    else:
        val3 = dfA3.iloc[0]['Cast']
    # Top Director
    dfD = netflix_df[['director', 'country']]
    dfD1 = dfD[dfD['country'].str.contains(dropDown, case=False)]
    dfD2 = dfD1['director'].str.split(',', expand=True).stack()
    dfD2 = dfD2.to_frame()
    dfD2.columns = ['Director']
    dfD3 = dfD2.groupby(['Director']).size().reset_index(name='counts')
    dfD3 = dfD3[dfD3['Director'] != 'No Director Specified']
    dfD3 = dfD3.sort_values(by='counts', ascending=False)
    if dfD3.empty:
        val4 = "Director data from this country is not available"
    else:
        val4 = dfD3.iloc[0]['Director']
    return val1, val2, val3, val4
