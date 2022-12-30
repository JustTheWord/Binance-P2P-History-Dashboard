from datetime import datetime as dt
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import json

CONFIG = json.load(open('../config.json', 'r'))
trade_method = 'buy'  # for interactive toggle button


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

main = html.Div(className='main', children=[

    html.Div(className='info-container', children=[

        html.Div(className='interface-container', children=[

            html.Div(className='trade-method-container', children=[
                dbc.Button("BUY", id='buy-toggle', color="white", className="mr-1",  n_clicks=0, value='on'),
                dbc.Button("SELL", id='sell-toggle', color="white", className="mr-1",  n_clicks=0, value='off')
            ]),

            html.Div(className='count-method', children=[
                dbc.Button("TOP", id='top-toggle', color="white", className="mr-1",  n_clicks=0, value='off'),
                dbc.Button("AVERAGE", id='average-toggle', color="white", className="mr-1",  n_clicks=0, value='on')
            ]),

            html.Div(className='date-container', children=[

                html.H1('Choose date:'),

                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(2022, 12, 23),
                    max_date_allowed=dt(2030, 1, 1),
                    date=dt.date(dt.now()),
                    display_format='DD.MM.YYYY',
                ),
            ])
        ]),
        dcc.Graph(id='line_chart', figure={})


    ]),
    html.Div(className='configuration-container', children=[
        html.H1('Configuration:'),

        html.Div(className='config-info-container', children=[

            html.Div(className='config-info', children=[
                html.H2(id='asset'),
                html.H2(id='fiat'),
            ]),

            html.Div(className='config-info', children=[
                html.H2(id='tradeMethods'),
                html.H2(id='finishRate'),
            ]),

            html.Div(className='config-info', children=[
                html.H2(id='orderCount'),
                html.H2(id='surplusAmount'),
            ]),

            html.Div(className='config-info', children=[
                html.H2(id='minSingleTransAmount'),
            ]),
        ])
    ])
])

# *********************************************************************************************************
app.layout = main
# *********************************************************************************************************


@app.callback(
    [Output('buy-toggle', 'style'),
     Output('sell-toggle', 'style'),
     Output('buy-toggle', 'value'),
     Output('sell-toggle', 'value'),
     Output('buy-toggle', 'n_clicks'),
     Output('sell-toggle', 'n_clicks')],

    [Input('buy-toggle', 'n_clicks'),
     Input('sell-toggle', 'n_clicks')],
)
def on_click(buy_click, sell_click):
    if buy_click < sell_click:
        return [{'backgroundColor': 'white', 'color': 'black'}, {'backgroundColor': '#007bff', 'color': 'white'},
                'off', 'on', 0, 0]
    else:
        return [{'backgroundColor': '#007bff', 'color': 'white'}, {'backgroundColor': 'white', 'color': 'black'},
                'on', 'off', 0, 0]



@app.callback(
    [Output('top-toggle', 'style'),
     Output('average-toggle', 'style'),
     Output('top-toggle', 'value'),
     Output('average-toggle', 'value'),
     Output('top-toggle', 'n_clicks'),
     Output('average-toggle', 'n_clicks')],

    [Input('top-toggle', 'n_clicks'),
     Input('average-toggle', 'n_clicks')],
)
def on_click(top_click, average_click):
    if top_click > average_click:
        return [{'backgroundColor': '#007bff', 'color': 'white'}, {'backgroundColor': 'white', 'color': 'black'},
                'on', 'off', 0, 0]
    else:
        return [{'backgroundColor': 'white', 'color': 'black'}, {'backgroundColor': '#007bff', 'color': 'white'},
                'off', 'on', 0, 0]



@app.callback(
    Output('line_chart', 'figure'),
    [Input('my-date-picker-single', 'date'),
        Input('buy-toggle', 'value'),
        Input('sell-toggle', 'value'),
        Input('top-toggle', 'value'),
        Input('average-toggle', 'value')]
)
def update_dashboard(
        date,
        buy_toggle,
        sell_toggle,
        top_toggle,
        average_toggle
):
    global trade_method
    count_method = 'averagePrice'

    if buy_toggle == 'on':
        trade_method = 'buy'
    elif sell_toggle == 'on':
        trade_method = 'sell'

    if top_toggle == 'on':
        count_method = 'topPrice'
    elif average_toggle == 'on':
        count_method = 'averagePrice'

    year, month, day = date.split('-')
    date = f'{day}.{month}.{year[2:]}'

    asset = CONFIG[trade_method]['data']['asset']
    fiat = CONFIG[trade_method]['data']['fiat']

    df = pd.read_csv(f'../data/{date}_{trade_method}.csv', sep=';')
    fig = px.line(x=df['date'], y=df[count_method],
                  labels={'x': 'Date', 'y': 'Price'},
                  title=f"P2P {asset}-{fiat} {date}")

    return fig


@app.callback(
    [Output('asset', 'children'),
     Output('fiat', 'children'),
     Output('tradeMethods', 'children'),
     Output('finishRate', 'children'),
     Output('orderCount', 'children'),
     Output('surplusAmount', 'children'),
     Output('minSingleTransAmount', 'children')],
    [Input('buy-toggle', 'value'),
     Input('sell-toggle', 'value')]
)
def update_config(buy_toggle, sell_toggle):
    global trade_method

    if buy_toggle == 'on':
        trade_method = 'buy'
    elif sell_toggle == 'on':
        trade_method = 'sell'

    asset = CONFIG[trade_method]['data']['asset']
    fiat = CONFIG[trade_method]['data']['fiat']
    trade_methods = CONFIG[trade_method]['data']['payTypes']
    finish_rate = CONFIG[trade_method]['monthFinishRate']
    order_count = CONFIG[trade_method]['monthOrderCount']
    surplus_amount = CONFIG[trade_method]['surplusAmount']

    return f"Asset: {asset}", f"Fiat: {fiat}", f"Trading methods: {', '.join(trade_methods)}", \
        f"Advertiser monthly finish rate: {finish_rate}", f"Minimum advertiser's monthly order count: {order_count}", \
        f"Minimum available amount of an advertisement: {surplus_amount} {asset}", \
        f"Maximum high limit of an advertisement: {CONFIG[trade_method]['minSingleTransAmount']} {fiat}"


if __name__ == "__main__":
    app.run_server(port=8000, debug=True)
