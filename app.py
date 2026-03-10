from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio

import pandas as pd
import numpy as np

df = pd.read_csv('vgsales.csv')

df = df.dropna(subset=['Year', 'Publisher'])
df['Year'] = df['Year'].astype(int)

genres = sorted(df['Genre'].unique().tolist())
all_genres = ['All Genres'] + genres

colors = {
    'background': '#1a1a2e',
    'text': '#e0e0e0'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1('Video Game Sales Explorer',
            style={'textAlign': 'center', 'color': colors['text']}),

    html.Div('Use the controls below to explore video game sales data from 1980 to 2016.',
             style={'textAlign': 'center', 'color': colors['text']}),

    html.Br(),

    html.Div([

        html.Div([
            html.Label('Region', style={'color': colors['text'], 'font-weight': 'bold'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Global',        'value': 'Global_Sales'},
                    {'label': 'North America', 'value': 'NA_Sales'},
                    {'label': 'Europe',        'value': 'EU_Sales'},
                    {'label': 'Japan',         'value': 'JP_Sales'},
                    {'label': 'Other',         'value': 'Other_Sales'}
                ],
                value='Global_Sales',
                id='region-selection'
            )
        ], style={'width': '28%', 'padding': '10px', 'display': 'inline-block'}),

        html.Div([
            html.Label('Genre', style={'color': colors['text'], 'font-weight': 'bold'}),
            dcc.Dropdown(
                options=[{'label': g, 'value': g} for g in all_genres],
                value='All Genres',
                id='genre-selection'
            )
        ], style={'width': '28%', 'padding': '10px', 'display': 'inline-block'}),

        html.Div([
            html.Label('Chart Type', style={'color': colors['text'], 'font-weight': 'bold'}),
            dcc.RadioItems(
                options=[
                    {'label': ' Vertical',   'value': 'bar'},
                    {'label': ' Horizontal', 'value': 'hbar'}
                ],
                value='bar',
                id='chart-style',
                inline=True,
                style={'color': colors['text']}
            )
        ], style={'width': '28%', 'padding': '10px', 'display': 'inline-block'}),

    ], style={'backgroundColor': colors['background']}),

    html.Div([
        html.Label('Year', style={'color': colors['text'], 'font-weight': 'bold'}),
        dcc.Slider(
            min=df['Year'].min(),
            max=df['Year'].max(),
            step=None,
            value=2010,
            marks={str(y): str(y) for y in range(df['Year'].min(), df['Year'].max() + 1, 5)},
            id='year-slider'
        )
    ], style={'padding': '10px', 'backgroundColor': colors['background']}),

    html.Br(),

    html.Div([
        html.Div([
            dcc.Graph(id='top-games-chart')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='sales-trend-chart')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(id='genre-breakdown-chart')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='publisher-chart')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ])

])


@app.callback(
    Output('top-games-chart', 'figure'),
    Output('sales-trend-chart', 'figure'),
    Output('genre-breakdown-chart', 'figure'),
    Output('publisher-chart', 'figure'),
    Input('region-selection', 'value'),
    Input('genre-selection', 'value'),
    Input('chart-style', 'value'),
    Input('year-slider', 'value'))
def update_charts(region, genre, chart_style, year):
    pio.templates.default = 'plotly_dark'

    filtered = df[df['Year'] <= year].copy()

    if genre != 'All Genres':
        filtered = filtered[filtered['Genre'] == genre]

    top10 = filtered.groupby('Name')[region].sum().sort_values(ascending=False).head(10).reset_index()
    top10.columns = ['Game', 'Sales']

    if chart_style == 'bar':
        fig1 = px.bar(top10, x='Game', y='Sales',
                      color='Sales',
                      color_continuous_scale='Viridis',
                      labels={'Sales': 'Sales (M)', 'Game': ''},
                      height=400)
        fig1.update_xaxes(tickangle=30)
    else:
        fig1 = px.bar(top10.sort_values('Sales'), x='Sales', y='Game',
                      orientation='h',
                      color='Sales',
                      color_continuous_scale='Viridis',
                      labels={'Sales': 'Sales (M)', 'Game': ''},
                      height=400)

    fig1.update_layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       title='Top 10 Games by Sales')

    trend = filtered.groupby(['Year', 'Genre'])[region].sum().reset_index()
    trend.columns = ['Year', 'Genre', 'Sales']

    fig2 = px.line(trend, x='Year', y='Sales',
                   color='Genre',
                   labels={'Sales': 'Sales (M)'},
                   height=400)

    fig2.update_layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       title='Sales Over Time by Genre')

    genre_totals = filtered.groupby('Genre')[region].sum().sort_values(ascending=False).reset_index()
    genre_totals.columns = ['Genre', 'Sales']

    fig3 = px.bar(genre_totals, x='Genre', y='Sales',
                  color='Genre',
                  color_discrete_sequence=px.colors.qualitative.G10,
                  labels={'Sales': 'Sales (M)', 'Genre': ''},
                  height=400)

    fig3.update_layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       showlegend=False,
                       title='Sales by Genre')

    fig3.update_xaxes(tickangle=30)

    pub_totals = filtered.groupby('Publisher')[region].sum().sort_values(ascending=False).head(10).reset_index()
    pub_totals.columns = ['Publisher', 'Sales']

    fig4 = px.bar(pub_totals.sort_values('Sales'), x='Sales', y='Publisher',
                  orientation='h',
                  color='Sales',
                  color_continuous_scale='icefire',
                  labels={'Sales': 'Sales (M)', 'Publisher': ''},
                  height=400)

    fig4.update_layout(plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       title='Top 10 Publishers by Sales')

    return fig1, fig2, fig3, fig4


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
