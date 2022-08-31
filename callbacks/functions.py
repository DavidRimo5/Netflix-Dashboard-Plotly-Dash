import pandas as pd
import plotly.express as px
import json

with open('world.geojson') as f:
    Countries = json.load(f)
mapbox_access_token = 'pk.eyJ1IjoiZGF2aWRyaW1vIiwiYSI6ImNsNmFsdWthZDFndWszbm9ieXhtNWI4aTYifQ.1pfKom3-Glp6O-6HL4-Pzw'

df_map = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_map.csv')

df = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles.csv')
df_d = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_D.csv')
df_c = pd.read_csv(r'C:\Users\David Rimo\Desktop\Vantage Circle\intern assessment\DashBoard\datasets\netflix_titles_C.csv')
df['date_added'] = pd.to_datetime(df['date_added'])
df_map['date_added'] = pd.to_datetime(df_map['date_added'])
df_map['year_added'] = df_map['date_added'].dt.year
df['duration'] = df['duration'].str.replace(r'\D', '')
df["duration"] = pd.to_numeric(df["duration"], errors='coerce')


def total(typeName):
    df1 = df[df['type'] == typeName]
    df_total = df1['type'].count()
    return df_total

total_mov = total('Movie')
total_show = total("TV Show")

total_dir = df_d['director'].count()
total_cast = df_c['cast'].count()


def ratings(ratType):
    df_type = df[df['type'] == ratType]
    df_rat = df_type.groupby(['rating', 'type']).size().reset_index(name='count')
    df_rat.rename(columns={'rating': 'xName'}, inplace=True)
    return df_rat


df_mov_rat = ratings('Movie')
df_show_rat = ratings('TV Show')

# DIRECTOR FUNCTION======================================================================
def director(dirType):
    df_type = df_d[df_d['type'] == dirType]
    df_dir = df_type.groupby(['director', 'type']).size().reset_index(name='count')
    df_dir = df_dir.sort_values('count', ascending=False).head(10)
    df_dir.rename(columns={'director': 'xName'}, inplace=True)
    return df_dir


df_mov_dir = director('Movie')
df_show_dir = director('TV Show')


# CAST FUNCTION======================================================================
def cast(castType):
    df_type = df_c[df_c['type'] == castType]
    df_cast = df_type.groupby(['cast', 'type']).size().reset_index(name='count')
    df_cast = df_cast.sort_values('count', ascending=False).head(10)
    df_cast.rename(columns={'cast': 'xName'}, inplace=True)
    return df_cast


df_mov_cast = cast('Movie')
df_show_cast = cast('TV Show')


# BARCHART FUNCTION======================================================================


def updateBarchart(ratingGraph, xName):
    fig = px.bar(ratingGraph, x="xName", y='count', color='count',
                 # color_continuous_scale='Reds',
                 labels={"xName": xName}).update_xaxes(categoryorder='total descending',)
    fig.update_layout(hovermode='closest',
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False),
                      font=dict(size=14, color='#c5c7c9'),
                      title=f"Total count per {xName}"
                      )
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',)
    fig.update_traces(marker_color='#b20710')
    fig.update_coloraxes(showscale=False)
    return fig


mov_rating_fig = updateBarchart(df_mov_rat, "Ratings")
show_rating_fig = updateBarchart(df_show_rat, "Ratings")

mov_dir_fig = updateBarchart(df_mov_dir, 'Director')
show_dir_fig = updateBarchart(df_show_dir, "Director")

mov_cast_fig = updateBarchart(df_mov_cast, "Cast Name")
show_cast_fig = updateBarchart(df_show_cast, "CastName")


df_country = df_map.groupby('year_added')['country'].value_counts().reset_index(name='counts')
fig_country = px.choropleth(df_country, locations="country", color="counts",
                            locationmode='country names',
                            animation_frame='year_added',
                            title='Country Vs Year',
                            range_color=[0,200],
                            color_continuous_scale=px.colors.sequential.matter,
                   )
fig_country.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)',
                          title_font=dict(size=30, color='#8a8d93',
                                        family="Lato, sans-serif"),
                          font=dict(size=17, color='#c5c7c9'))
fig_country.update_coloraxes(showscale=False),


fig_donut = px.pie(df, names='type', hole=0.7,
                   title='Most watched on Netflix',
                   color_discrete_sequence=['#b20710', '#221f1f'])
fig_donut.update_traces(hovertemplate=None, textposition='outside',
                        textinfo='percent+label', rotation=90)
fig_donut.update_layout(
    title_x=0.5,
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    title_font=dict(size=20, color='white',
                    family="Lato, sans-serif"),
    font=dict(size=17, color='#8a8d93'),
    hoverlabel=dict(bgcolor="#444", font_size=13,
                    font_family="Lato, sans-serif"),

)
