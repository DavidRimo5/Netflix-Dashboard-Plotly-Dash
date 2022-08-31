import json
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from app import app
with open('world.geojson') as f:
    Countries = json.load(f)

mapbox_access_token = 'pk.eyJ1IjoiZGF2aWRyaW1vIiwiYSI6ImNsNmFsdWthZDFndWszbm9ieXhtNWI4aTYifQ.1pfKom3-Glp6O-6HL4-Pzw'

df_1 = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_G.csv')
df_2 = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_map.csv')
df_color = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\countrywise_color.csv')

def function(typeName):
    df_m_mov = df_2[df_2['type'] == typeName]
    df_g_mov = df_1[df_1['type'] == typeName]
    df_M_mov = df_m_mov['country']
    df_G_mov = df_g_mov['listed_in']
    df_map = pd.concat([df_M_mov, df_G_mov], axis=1)
    df_map = df_map.dropna()
    df_map = df_map.groupby(['listed_in', 'country']).size().reset_index(name='count')
    return df_map


df_map_mov = function('Movie')
df_map_show = function('TV Show')


def geojson_func(geo):
    found = []
    missing = []
    countries_geo = []

    tmp = geo.set_index('country')
    for country in Countries['features']:
        country_name = country['properties']['NAME']

        if country_name in tmp.index:
            found.append(country_name)
            geometry = country['geometry']
            countries_geo.append({
                'type': 'Feature',
                'geometry': geometry,
                'id': country_name
            })
        else:
            missing.append(country_name)
    new_geojson = {'type': 'FeatureCollection', 'features': countries_geo}
    return new_geojson


geosjon_mov = geojson_func(df_map_mov)
geojson_show = geojson_func(df_map_show)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Top 10 Genre Country (Movie)", style={'textAlign': 'center', 'color': 'red', 'fontWeight': 'bold'}),
            html.P("Select a Genre: "),
            dcc.Dropdown(id='choro_mov_dd',
                         options=[{'label': i, 'value': i}
                                  for i in df_map_mov['listed_in'].unique()],
                         value='Documentaries',
                         clearable=False,
                         style={'color': 'green', 'width': "70%"},
                         multi=False
                         ),
            html.Br(),
            dcc.Graph(id='choro_mov_graph', className="growHover")
        ], style={'color': "rgba(0,0,0,0)"}, xs=10, sm=10, md=10, lg=6, xl=6),
        dbc.Col([
            html.H4("Top 10 Genre Country (TV Shows)", style={'textAlign': 'center', 'color': 'red', 'fontWeight': 'bold'}),
            html.P("Select a Genre: "),
            dcc.Dropdown(id='choro_show_dd',
                         options=[{'label': i, 'value': i}
                                  for i in df_map_show['listed_in'].unique()],
                         value='International TV Shows',
                         clearable=False,
                         style={'color': 'green', 'width': "70%"},
                         multi=False
                         ),
            html.Br(),
            dcc.Graph(id='choro_show_graph', className="growHover", config={
                           'displayModeBar': False })
        ], style={'color': "rgba(0,0,0,0)"}, xs=10, sm=10, md=10, lg=6, xl=6)
    ], justify="around")
], className="container-fluid")


@app.callback(
    Output('choro_mov_graph', 'figure'),
    Output('choro_show_graph', 'figure'),
    [
        Input('choro_mov_dd', 'value'),
        Input('choro_show_dd', 'value'),
    ]
)
def update_graph(selected_mov, selected_show):
    map1 = lambda map: map[map['listed_in'] == selected_mov]
    new_map_mov = map1(df_map_mov)
    new_map_mov = new_map_mov.sort_values('count', ascending=False).head(20)
    new_map_mov = pd.merge(new_map_mov, df_color, on='country', how='inner')
    map2 = lambda map: map[map['listed_in'] == selected_show]
    new_map_show = map2(df_map_show)
    new_map_show = new_map_show.sort_values('count', ascending=False).head(20)
    new_map_show = pd.merge(new_map_show, df_color, on='country', how='inner')


    def update_json(name, json_df):
        fig_choro_mov = px.choropleth_mapbox(name,
                                             geojson=json_df,
                                             locations='country',
                                             color='country',
                                             mapbox_style='open-street-map',
                                             zoom=1,
                                             center={'lat': 19, 'lon': 11},
                                             opacity=1,
                                             )
        fig_choro_mov.update_layout(
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            mapbox=dict(accesstoken=mapbox_access_token, style='dark'),
            legend_title='Countries',
            font_color="white",
            title_font_color = "red"
        )
        return fig_choro_mov
    choro_map_mov = update_json(new_map_mov, geosjon_mov)
    choro_map_show = update_json(new_map_show, geojson_show)

    return choro_map_mov, choro_map_show
