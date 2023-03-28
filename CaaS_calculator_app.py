#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash


from dash import dcc
from dash import html
#import dash_core_components as dcc
#import dash_html_components as html
from dash_table import DataTable
from dash_table import FormatTemplate
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

from datetime import datetime

import csv
import numpy as np

import math

import base64



def round_didgit(dataset,variable,round_lvl):
    for index, row in dataset.iterrows():
        if math.isnan(dataset[variable].loc[index]):
            pass
        else:
            dataset[variable].loc[index]=round(dataset[variable].loc[index],round_lvl)

            
def extract_avg_df(df_,ticker):
    avg_df=df_[df_['Ticker']==ticker]
    avg_df=avg_df.select_dtypes(exclude=['object'])
    del avg_df['Longitude ($ Millions)']
    del avg_df['Latitude ($ Millions)']
    return avg_df.mean()
            
def quarterized(df_,date_format):
    df_r=df_.copy()
    for index, row in df_r.iterrows():
        if row[date_format][5:7]=='12':
            df_r[date_format].iloc[index]='Q4 '+str(row[date_format][:4])
        if row[date_format][5:7]=='03' or row[date_format][5:7]=='04' or row[date_format][5:7]=='05':
            df_r[date_format].iloc[index]='Q1 '+str(row[date_format][:4])
        if row[date_format][5:7]=='06' or row[date_format][5:7]=='07':
            df_r[date_format].iloc[index]='Q2 '+str(row[date_format][:4])
        if row[date_format][5:7]=='09' or row[date_format][5:7]=='10':
            df_r[date_format].iloc[index]='Q3 '+str(row[date_format][:4])
        if row[date_format][5:7]=='12':
            df_r[date_format].iloc[index]='Q4 '+str(row[date_format][:4])
        if row[date_format][5:7]=='01':
            df_r[date_format].iloc[index]='Q4 '+str(int(row[date_format][:4])-1)
    return df_r
            
def display_formating(df__di):
    
    df_d=df__di.copy()
    
    for name, values in df_d.iteritems():
    
        if name != 'date2':
            if df_d[name].dtype==np.int64 or df_d[name].dtype==np.float64:
                df_d.rename(columns = {name:str(name)+' ($ Millions)'}, inplace = True)

                for index, row in df_d.iterrows():
                    if math.isnan(df_d[str(name)+' ($ Millions)'].loc[index]):
                        pass
                    else:
                        numform=df_d[str(name)+' ($ Millions)'].loc[index]/1000000
                        numform=int(numform)
                        df_d[str(name)+' ($ Millions)'].loc[index]=numform
                    
    return df_d

def average_df(df_, tck):
    df_hypo_float = df_[df_['ticker'] == tck].select_dtypes('float')
    df_hypo = df_hypo_float.mean()
    return df_hypo



df_financials_annual = pd.read_csv('financials.csv')
df_financials_annual['EBITDA_']=df_financials_annual['ebit']+df_financials_annual['depreciationAndAmortization']
df_ratios_annual = pd.read_csv('ratios.csv')
encoded_image = base64.b64encode(open('logo.png', 'rb').read())

All_columns_fin_simple = list(df_financials_annual)
options_fin_simple = [{'label': col, 'value': col} for col in All_columns_fin_simple]

All_columns_ratio_simple = list(df_ratios_annual)
options_ratio_simple = [{'label': col, 'value': col} for col in All_columns_ratio_simple]



# Data Files

ucr_csv_annual = 'https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/01_list_of_companies/annual_data.csv'
ucr_csv_annual_new = 'https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/01_list_of_companies/annual_data_new.csv'
ucr_csv_quartal = 'https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/01_list_of_companies/quartal_data.csv'

df_annual = pd.read_csv(ucr_csv_annual)
df_annual = df_annual[df_annual['date'] > '2018-01-01']
df_annual_new = pd.read_csv(ucr_csv_annual_new)




src1 = 'https://raw.githubusercontent.com/Bayan2019/CaaSculator_Python/main/01_list_of_companies/companies_info.csv'

tickers = pd.read_csv(src1)


Big_df_annual = df_annual
Big_df_annual = Big_df_annual.drop(['ticker', 'date', 'currency'], axis=1)

All_columns0 = list(Big_df_annual.columns)

Big_df_annual = df_annual
Big_df_annual = Big_df_annual.drop(['currency'], axis=1)

Big_df_melt = pd.melt(Big_df_annual, id_vars=['date', 'ticker'])
Big_df_melt = Big_df_melt.dropna()

All_columns = []

for col in All_columns0:
    if (col in list(Big_df_melt['variable'])): All_columns.append(col)

All_columns_pos = []

for col in All_columns:
    if Big_df_annual[col].dtypes == 'float64':
        if (Big_df_annual[col].dropna() > 0.1).all(): All_columns_pos.append(col)

All_columns_pos1 = All_columns_pos + ['inventory_to_assets']

options_period = [{'label': 'Annual', 'value': 'annual'}, {'label': 'Quartal', 'value': 'quarterly'}]

# options_ratio_tcc = [{'label': 'EBIT to Interest Expense', 'value': 'EBIT to Interest Expense'}, 
#                     {'label': 'EBITDA to Interest Expense', 'value': 'EBITDA to Interest Expense'},
#                     {'label': 'Return On Capital', 'value': 'Return On Capital'},
#                     {'label': 'EBITDA to Revenue', 'value': 'EBITDA to Revenue'},
#                     {'label': 'Free Operating Cash Flow to Total Debt', 'value': 'Free Operating Cash Flow to Total Debt'},
#                     {'label': 'Funds From Operations to Total Debt', 'value': 'Funds From Operations to Total Debt'},]

options_ratio_tcc = [{'label': 'EBIT to Interest Expense', 'value': 'ebit_to_interestExpense'}, 
                    {'label': 'EBITDA to Interest Expense', 'value': 'ebitda_to_interestExpense'},
                    {'label': 'Return On Capital', 'value': 'Return_on_Capital'},
                    {'label': 'EBITDA to Revenue', 'value': 'ebitda_to_Revenue'},
                    {'label': 'Free Operating Cash Flow to Total Debt', 'value': 'FreeOperCF_to_TotalDebt'},
                    {'label': 'Funds From Operations to Total Debt', 'value': 'FFO_to_TotalDebt'},]

options_ratio_tcc_formatted = [{'label': 'EBIT to Interest Expense', 'value': 'EBIT to Interest Expense'}, 
                    {'label': 'EBITDA to Interest Expense', 'value': 'EBITDA to Interest Expense'},
                    {'label': 'Return On Capital', 'value': 'Return On Capital'},
                    {'label': 'EBITDA to Revenue', 'value': 'EBITDA to Revenue'},
                    {'label': 'Free Operating Cash Flow to Total Debt', 'value': 'Free Operating Cash Flow to Total Debt'},
                    {'label': 'Funds From Operations to Total Debt', 'value': 'Funds From Operations to Total Debt'},]

options_fin_tcc = [{'label': 'EBITDA', 'value': 'EBITDA_'},
                   {'label': 'EBIT', 'value': 'ebit'},
                    {'label': 'Current Debt', 'value': 'totalDebt'},
                    {'label': 'Operating Income', 'value': 'operatingIncome'},
                    {'label': 'Interest Expense', 'value': 'interestExpense'}]


options_ticker = [{'label': tickers.loc[i, 'name'],
                   'value': tickers.loc[i, 'ticker']}
                  for i in tickers.sort_values(['name']).index]

options_columns = [{'label': col, 'value': col} for col in All_columns]

options_columns_pos = [{'label': col, 'value': col} for col in All_columns_pos]

options_columns_pos1 = [{'label': col, 'value': col} for col in All_columns_pos1]

options_tickers_exclude = [tickers.loc[i, 'ticker'] for i in tickers.index]


def get_title(ticker):
    df = tickers.set_index('ticker')
    title = df.loc[ticker, 'name']

    return title

def plot_style(paper_bg='white', plot_bg='rgb(237, 239, 255)', font='rgb(79, 79, 79)'):
    plot_style = {'paper_bgcolor': paper_bg, 'plot_bgcolor': plot_bg,
                  'font': {'color': font , 'size' : 14, 'family':'sans-serif'}}
    return plot_style

def plot_style_treemap(paper_bg='white', plot_bg='rgb(237, 239, 255)', font='rgb(79, 79, 79)'):
    plot_style = {'paper_bgcolor': paper_bg, 'plot_bgcolor': plot_bg,
                  'font': {'color': font , 'size' : 18, 'family':'sans-serif'}}
    return plot_style

def plot_style_blue(paper_bg='rgb(232, 241, 255)', plot_bg='rgb(247, 249, 255)', font='rgb(79, 79, 79)'):
    plot_style = {'paper_bgcolor': paper_bg, 'plot_bgcolor': plot_bg,
                  'font': {'color': font , 'size' : 18, 'family':'sans-serif'}}
    return plot_style


# Create the Dash app

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

app.layout = html.Div([
    
    
    html.Div(children=[
            html.Div(children=[
                dbc.Row(
                    html.H3('CaaS Calculator',style={'color': 'white','font-family':'sans-serif',
                                                                        'fontSize': 45,'verticalAlign': 'top','display':'inline-block',
                                                                                   'margin' : '10px 60px 10px 60px','width': '90',
                                                                      'align-items': 'center',  'justify-content':'left'}),
                ),

            ],style={'verticalAlign': 'top',
                   'margin' : '10px','width': '5%',
                  'align-items': 'center','flex':1,
                    'display': 'flex',  'justify-content':'left'}),

            html.Div(children=[
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode())),           
            ],style={'verticalAlign': 'top',
                   'margin' : '10px','width': '5%',
                  'align-items': 'center','flex':1,
                    'display': 'flex',  'justify-content':'right'}),


                    ],style={'background-color': 'rgb(52, 56, 52)', 'display': 'flex',
                              'flex':'row','horizontalAlign': 'center','height':'120px'},),
    
  

    # Overall Summary
    dcc.Tabs(
        id="tabs_common_summary", value='tab_calc',
        className='custom-tabs', vertical=False,
        children=[
            
            dcc.Tab(label='CaaS Simulation', value='tab_calc', className='custom-tab',
                    selected_className='custom-tab--selected',
                    style={'background-color':'rgb(250, 213, 165)'}),

            
        ], style={'height': '0px','font-family':'sans-serif',
                  'fontSize': 0,'color':'rgb(25, 25, 25)'}),
    html.Br(),
    html.Div(id='tabs_common_summary_content'),
    html.Br(),

    # Individual Summary
    html.Footer(
            children=[
                html.Br(),
                html.H1('1TCC © 2023', style={'color': 'white',#'pading':'50px 0px 50px 0px', 
                                                'textAlign': 'center','font-family':'sans-serif' ,'fontSize': 20,}),
                html.Br(),


            ]
            ,style={'background-color': 'rgb(52, 56, 52)',"width": "100%"}

            ),

    # Closing
    ],
    style={'text-align': 'center', 'display': 'inline-block', 'width': '100%',
           'background-color': 'white', 'color': 'rgb(79, 79, 79)'})

# Overall Summary tabs





@app.callback(
    Output('tabs_common_summary_content', 'children'),
    Input('tabs_common_summary', 'value'),
    #Input('comp_general', 'value')
)
def render_common_content(tab):

    if tab=='tab_calc':
        return(
        #-----------------------------------------------SELECT A COMPANY----------    
            html.Div(
                children=[
                    html.Div(
                            children=[

                                
                                dcc.Dropdown(id='tcc1_ticker', options=options_ticker, value='TEVA',disabled=True,
                                             style={'width': '600px',  'display': 'inline-block','margin' : '0px 0px 0px 0px',
                                                    'color': 'blue', 'horizontalAlign': 'right','verticalAlign': 'top',
                                                    'font-family':'sans-serif' ,'fontSize': 20}),
                            ],style={'width': '80%', 'display': 'inline-block','horizontalAlign': 'center','margin' : '80px 10px 10px 10px'}),



                ]
                #,style={'background-color': 'rgb(255, 154, 38)'}

                ),
            html.Div(id='tab_simu'),
        #-----------------------------------------------SELECT A COMPANY----------  
        )
    
    

    

    
    
    
@app.callback(
    Output('radio_param', 'children'),
    Input('tcc1_radio', 'value')

)
def render_radio_param(radio):
    if radio=='pour':
        return(
        html.Br(),
        html.H3('Select (%)',style={'color': 'rgb(22, 73, 161)','font-family':'sans-serif' ,
                                                                     'fontSize': 25,'verticalAlign': 'top','margin' : '20px 20px 20px 20px',
                                                  'display': 'inline-block','horizontalAlign': 'left','width': '300px'}),
        dcc.Slider(id='tcc1_slider', min=0, max=100,
                   marks=None, value=50, step=1, 
                   tooltip={"placement": "bottom", "always_visible": True}),
        html.Br(),
        dcc.Input(id='tcc_amount', type='number', min=0, max=1000, value=0, step=1,placeholder="$ Millions",
                  style={'height': '0px','width': '0px', 'display': 'inline-block','margin' : '0px 0px 0px 0px',
                         'color': 'blue', 'horizontalAlign': 'right','verticalAlign': 'top',
                         'font-family':'sans-serif','margin' : '20px 20px 20px 20px' ,'fontSize': 1}),
        html.Br(),
        )
        
    else:
        return(
        html.Br(),
        html.H3('Amount of inventory to fund ($ Millions)',
                style={'color': 'rgb(22, 73, 161)','font-family':'sans-serif',
                       'fontSize': 25,'verticalAlign': 'top','margin' : '20px 20px 20px 20px',
                       'display': 'inline-block','horizontalAlign': 'left','width': '50%'}),
        html.Br(),
        dcc.Input(id='tcc_amount', type='number', min=0, max=1000, value=0, step=1,placeholder="$ Millions",
                  style={'width': '300px',  'display': 'inline-block','margin' : '0px 0px 0px 0px',
                         'color': 'blue', 'horizontalAlign': 'right','verticalAlign': 'top',
                         'font-family':'sans-serif','margin' : '20px 20px 20px 20px' ,'fontSize': 20}),
        html.Br(),
        dcc.Input(id='tcc1_slider', type='number', min=0, max=1000, value=0, step=1,placeholder="$ Millions",
                  style={'height': '0px','width': '0px',
                         'display': 'inline-block','margin' : '0px 0px 0px 0px',
                         'color': 'blue', 'horizontalAlign': 'right','verticalAlign': 'top',
                         'font-family':'sans-serif','margin' : '20px 20px 20px 20px' ,'fontSize': 1}),
        )

    



                #---------------------------CONTENT----------------------------------------
@app.callback(
    Output('tab_simu', 'children'),
    Input('tcc1_ticker', 'value')

)
def render_compare_content(comp):
    #return(html.H1('TEST TEST TES'),)
    if comp == None:
            return html.Div(children=
                            [html.H3('Please select a Company',
                                     style={'color': 'rgb(207, 207, 207)',
                                            'font-family':'sans-serif' ,
                                            'fontSize': 40,
                                            'margin': '20px 30px 1000px 20px'})],)
        
    else: 
        return html.Div(
            children=[
                html.Br(),
                
                #----------------------------------------------------------------------------------------------
                html.Br(),
                html.Div(
                    children=[

                    html.H3('General info',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 42,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),

                    html.Div(
                    children=[
                        html.H3('Financials',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 35,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),

                        html.Br(),

                        html.H3('Display specific financial:',
                                style={'color': 'rgb(22, 73, 161)',
                                       'font-family':'sans-serif',
                                       'fontSize': 20,
                                       'verticalAlign': 'top',
                                       'margin' : '7px 0px 0px 0px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'left',
                                       'width': '400px'}),

                        html.Br(),
                        dcc.Dropdown(id='bar_fin_var_simple',
                                     options=options_fin_simple,
                                     value='inventory',
                                     style={'width': '400px',
                                            'display': 'inline-block',
                                            'margin' : '0px 0px 0px 0px',
                                            'color': 'blue',
                                            'margin':'10px 0px 0px 0px',
                                            'font-family':'sans-serif',
                                            'fontSize': 20}),

                        html.Br(),

                                html.Div(
                                    children=[dcc.Graph(id='bar_fin_simple')],
                                    style={'width': '80%',
                                           'horizontalAlign': 'center',
                                           'display': 'inline-block',
                                           'margin':'50px 0px 0px 0px'}),
                                html.Br(),


                        html.Br(),
                        html.Br(),


                        ],
                    style={'width': '100%', 'display': 'inline-block',
                           'border': '0px solid orange',
                           'border-radius': 20,'margin':'50px 0px 0px 0px',
                           'background-color':'rgb(232, 241, 255)'}),
                        
                        
                    html.Div(
                    children=[
                        html.H3('Ratios',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 35,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),

                        html.Br(),

                        html.H3('Display specific ratios:',
                                style={'color': 'rgb(22, 73, 161)',
                                       'font-family':'sans-serif',
                                       'fontSize': 20,
                                       'verticalAlign': 'top',
                                       'margin' : '7px 0px 0px 0px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'left',
                                       'width': '400px'}),

                        html.Br(),
                        dcc.Dropdown(id='bar_ratio_var_simple',
                                     options=options_ratio_simple,
                                     value='Return_on_Capital',
                                     style={'width': '400px',
                                            'display': 'inline-block',
                                            'margin' : '0px 0px 0px 0px',
                                            'color': 'blue',
                                            'margin':'10px 0px 0px 0px',
                                            'font-family':'sans-serif',
                                            'fontSize': 20}),

                        html.Br(),

                                html.Div(
                                    children=[dcc.Graph(id='bar_ratio_simple')],
                                    style={'width': '80%',
                                           'horizontalAlign': 'center',
                                           'display': 'inline-block',
                                           'margin':'50px 0px 0px 0px'}),
                                html.Br(),


                        html.Br(),
                        html.Br(),


                        ],
                    style={'width': '100%', 'display': 'inline-block',
                           'border': '0px solid orange',
                           'border-radius': 20,'margin':'50px 0px 0px 0px',
                           'background-color':'rgb(232, 241, 255)'}),
                    #*************************************----------------------------------------------------------

                         
                        
                    ],style={'width':'95%','display': 'inline-block',
                             'border': '0px solid orange',
                             'horizontalAlign': 'center',
                             'border-radius': 20,
                             'background-color':'white',
                             'padding': '50px','box-shadow': '5px 5px 15px 8px lightgrey',
                             'margin': '20px 30px 20px 20px'}),

                
                html.Br(),
                html.Div(
                    children=[
                        html.H3('CaaS simulation',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 42,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),
                        
                        html.Div(
                            children=[
                                html.Br(),
                                html.H3('Inventory Funding Involvment',
                                        style={'color': 'rgb(15, 13, 37)',
                                               'font-family':'sans-serif',
                                               'fontSize': 35,'margin':'20px',
                                               'display': 'inline-block'}),

                                html.Br(),

                                html.Br(),
                                dcc.RadioItems(id='tcc1_radio', 
                                               options={'pour': 'By Percentage','number': 'By specific Amount'},
                                               value='pour',
                                               labelStyle={'width':'200','margin':"10px 10px 10px 10px"},
                                               style={'color': 'black','font-family':'sans-serif' ,
                                                      'fontSize': 22,'verticalAlign': 'top',
                                                      'margin' : '7px 0px 0px 0px',
                                                      'display': 'inline-block',
                                                      'horizontalAlign': 'left','width': '50%'}),
                                html.Br(),
                                
                                
                                html.Div(id='radio_param'),

                                

                            ],
                            style={'width': '60%',
                                   'display': 'inline-block',
                                   'border': '0px solid orange',
                                   'horizontalAlign': 'center',
                                   'border-radius': 20,'margin':'50px 0px 0px 0px',
                                   'background-color':'rgb(255, 247, 237)'}),

                        
                        html.Br(),


                    #*************************************
                        html.Div(
                    children=[
                        html.H3('Impact on Cash and Inventory',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 35,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),


                        html.Br(),

                                html.Div(
                                    children=[dcc.Graph(id='tcc_inv_cash')],
                                    style={'width': '80%',
                                           'horizontalAlign': 'center',
                                           'display': 'inline-block',
                                           'margin':'50px 0px 0px 0px'}),
                                html.Br(),


                        ],
                    style={'width': '100%', 'display': 'inline-block',
                           'border': '0px solid orange', 
                           'border-radius': 20,'margin':'50px 0px 0px 0px',
                           'background-color':'rgb(232, 241, 255)'}),
                    html.Br(),
                    #*************************************
                        
                        
                    #*************************************
                        html.Div(
                    children=[
                        html.H3('Other Impacted Financials',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 35,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),

                        html.Br(),

                        html.H3('Display specific financial:',
                                style={'color': 'rgb(22, 73, 161)',
                                       'font-family':'sans-serif',
                                       'fontSize': 20,
                                       'verticalAlign': 'top',
                                       'margin' : '7px 0px 0px 0px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'left',
                                       'width': '400px'}),

                        html.Br(),
                        dcc.Dropdown(id='bar_fin_var',
                                     options=options_fin_tcc,
                                     value='totalDebt',
                                     style={'width': '400px',
                                            'display': 'inline-block',
                                            'margin' : '0px 0px 0px 0px',
                                            'color': 'blue',
                                            'margin':'10px 0px 0px 0px',
                                            'font-family':'sans-serif',
                                            'fontSize': 20}),

                        html.Br(),

                                html.Div(
                                    children=[dcc.Graph(id='tcc_fin_fig')],
                                    style={'width': '80%',
                                           'horizontalAlign': 'center',
                                           'display': 'inline-block',
                                           'margin':'50px 0px 0px 0px'}),
                                html.Br(),


                        html.Br(),
                        html.Br(),


                        ],
                    style={'width': '100%', 'display': 'inline-block',
                           'border': '0px solid orange',
                           'border-radius': 20,'margin':'50px 0px 0px 0px',
                           'background-color':'rgb(232, 241, 255)'}),
                    html.Br(),
                    #*************************************
                        
                    #*************************************
                        html.Div(
                    children=[
                        html.H3('Impact on Ratios',
                                style={'color': 'rgb(15, 13, 37)',
                                       'font-family':'sans-serif',
                                       'fontSize': 35,'margin':'20px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'center',
                                       'width':'65%'}),

                        html.Br(),

                        html.H3('Display specific ratio:',
                                style={'color': 'rgb(22, 73, 161)',
                                       'font-family':'sans-serif',
                                       'fontSize': 20,'verticalAlign': 'top',
                                       'margin' : '7px 0px 0px 0px',
                                       'display': 'inline-block',
                                       'horizontalAlign': 'left',
                                       'width': '400px'}),

                        html.Br(),
                        dcc.Dropdown(id='bar_ratio_var',
                                     multi=True,
                                     options=options_ratio_tcc_formatted,
                                     value=['Return On Capital', 'Free Operating Cash Flow to Total Debt'],
                                                     style={'height':'100px', 'width': '400px',
                                                            'display': 'inline-block',
                                                            'margin' : '0px 0px 0px 0px',
                                                            'color': 'blue',
                                                            'margin':'10px 0px 0px 0px',
                                                            'font-family':'sans-serif',
                                                            'fontSize': 20}),

                        html.Br(),

                                html.Div(
                                    children=[dcc.Graph(id='tcc_ratio_fig')],
                                    style={'width': '80%',
                                           'horizontalAlign': 'center',
                                           'display': 'inline-block',
                                           'margin':'50px 0px 0px 0px'}),
                                html.Br(),


                        html.Br(),
                        html.Br(),


                        ],
                    style={'width': '100%', 'display': 'inline-block',
                           'border': '0px solid orange',
                           'border-radius': 20,'margin':'50px 0px 0px 0px',
                           'background-color':'rgb(232, 241, 255)'}),
                    html.Br(),
                    #*************************************
                         
                        
                    ],style={'width':'95%','display': 'inline-block',
                             'border': '0px solid orange',
                             'horizontalAlign': 'center',
                             'border-radius': 20,
                             'background-color':'white',
                             'padding': '50px','box-shadow': '5px 5px 15px 8px lightgrey',
                             'margin': '20px 30px 20px 20px'}),
                
                
                #----------------------------------------------------------------------------------------
                
                
                
                
                #html.Div(id='hypo'),
                
                
                
                                
                 ])
    

    
def millions_formatter(x):
    return '{:.2f}M'.format(x/1000000)


###################################################################### Salute! ##################################################################

@app.callback(
    Output(component_id='tcc_ratio_fig', component_property='figure'),
    Input(component_id='tcc1_ticker', component_property='value'),
    Input(component_id='bar_ratio_var', component_property='value'),
    Input(component_id='tcc1_slider', component_property='value'),
    Input(component_id='tcc_amount', component_property='value'),
    Input(component_id='tcc1_radio', component_property='value'),
    #Input(component_id='tcc1_period', component_property='value')
    
)
def update_tcc_ratio_fig(tick, focus_var, Lambda_slider, Lambda_amount, radio):

    '''if Lambda_slider>99:
        Lambda_slider=99'''
    
    period='annual'
    
    tickers_list = [tick]
        
    if period=='quartal':
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date']
    
    else:
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date'].astype(str).str[0:4]

    df1 = df0.copy()


    # df0['TCC'] = 'Without Inventory Funding'

    # df1['TCC'] = 'With Inventory Funding'
    
    # Calcul with funding amount -----------------------------------------------------------------------------

    if radio=='pour':
        Lambda=Lambda_slider/100
        df1['totalDebt'] = np.where(df0['inventory'].mul(Lambda)>df0['totalDebt'], df0['totalDebt'].mul(0.1), df0['totalDebt']-(df0['inventory'].mul(Lambda)))
        df1['interestExpense'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['interestExpense'].mul(0.1), ((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense']))
        df1['operatingIncome'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['operatingIncome'] - abs(df0['interestExpense']).mul(0.1), df0['operatingIncome'] - abs(df0['interestExpense']).mul(1-((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt']))))
        df1['EBITDA_'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['EBITDA_'] - abs(df0['interestExpense']).mul(1-0.1), df0['EBITDA_'] - abs(((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense'])))
        df1['ebit'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['ebit'] - abs(df0['interestExpense']).mul(1-0.1), df0['ebit'] - abs(df0['interestExpense']-(((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense']))))

    else:
        Lambda=Lambda_amount
        df1['totalDebt'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['totalDebt'].mul(0.1), df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))))
        df1['interestExpense'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['interestExpense'].mul(0.1), ((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense']))
        df1['operatingIncome'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['operatingIncome'] - abs(df0['interestExpense']).mul(0.1), df0['operatingIncome'] - abs(df0['interestExpense']).mul(1-((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt']))))
        df1['EBITDA_'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['EBITDA_'] - abs(df0['interestExpense']).mul(1-0.1), df0['EBITDA_'] - abs(((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense'])))
        df1['ebit'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['ebit'] - abs(df0['interestExpense']).mul(1-0.1), df0['ebit'] - abs(df0['interestExpense']-(((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense']))))


    #-----------------------------------------------------------------------------------------------------------

    df_grouped_0 = df0.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_0 = df_grouped_0.reset_index()

    df_grouped_1 = df1.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_1 = df_grouped_1.reset_index()

    df_grouped_0['TCC'] = 'Without Inventory Funding'

    df_grouped_1['TCC'] = 'With Inventory Funding'
    
    df = pd.concat([df_grouped_0, df_grouped_1], axis=0)

    df['name'] = get_title(tick)

    df_ratios = df[['ticker', 'Date_formated', 'TCC', 'name']]


    # Updated ratios --------------------------------------------------------------------------  
    
    df_ratios['EBIT to Interest Expense'] = df['ebit'].divide(abs(df['interestExpense']))
    df_ratios['EBITDA to Interest Expense'] = (df['operatingIncome']+ df['depreciationAndAmortization']).divide(abs(df['interestExpense']))
    df_ratios['Return On Capital'] = (df['operatingIncome']
                                      - df['interestExpense']).divide(df['stockholdersEquity']
                                                                       + df['totalDebt'] - df['cashAndCashEquivalents'])
    
    
    
    df_ratios['EBITDA to Revenue'] = (df['operatingIncome']+ df['depreciationAndAmortization']).divide(df['totalRevenue'])
    df_ratios['Free Operating Cash Flow to Total Debt'] = (df['operatingIncome'] + df['depreciationAndAmortization']
                                            - df['capitalExpenditure']).divide(df['totalDebt'])
    
    if period=="quartal":
        df_ratios['Funds From Operations to Total Debt'] = 0
    else:
        df_ratios['Funds From Operations to Total Debt'] = (df['operatingIncome']
                                     + df['depreciationAndAmortization'] + df['saleOfPPE']).divide(df['totalDebt'])
    
    
     # ------------------------------------------------------------------------------------------
        
    df_ratios=df_ratios.round(4)

    ratios_melt = pd.melt(df_ratios, id_vars=['ticker', 'Date_formated', 'TCC', 'name'])

    ratios_melt_cols3 = ratios_melt[ratios_melt.variable.isin(focus_var)]
    
    tcc3_bar = px.bar(ratios_melt_cols3, x="Date_formated", y="value", 
                          facet_col='TCC', hover_name='name', height=600,text_auto=True,
                          labels={
                                  "value":"Ratio",
                                  "variable":" ",
                                  "Date_formated": ""
                             },
                          color="variable", color_discrete_sequence=px.colors.qualitative.D3,
                          barmode="group")


    tcc3_bar.update_layout({"bargap": 0.2, 'bargroupgap': 0.1})
    tcc3_bar.update_layout({"bargap": 0.4, 'bargroupgap': 0.12})
    tcc3_bar.update_traces(textangle=0)
    tcc3_bar.update_layout(legend=dict(
        orientation="h",
        title= None,
        yanchor="bottom",
        y=1.1,
        xanchor="right",
        x=1,
        font=dict(
            size=18,
            color="black"
        ),
    ))

    tcc3_bar.update_xaxes(tickvals = list(ratios_melt_cols3['Date_formated']))
    tcc3_bar.update_layout(plot_style_blue())
    tcc3_bar.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    tcc3_bar.update_annotations(font_size=22)

    return tcc3_bar

###################################################################### Salute! ##################################################################

@app.callback(
    Output(component_id='tcc_fin_fig', component_property='figure'),
    Input(component_id='tcc1_ticker', component_property='value'),
    Input(component_id='bar_fin_var', component_property='value'),
    Input(component_id='tcc1_slider', component_property='value'),
    Input(component_id='tcc_amount', component_property='value'),
    Input(component_id='tcc1_radio', component_property='value'),
    #Input(component_id='tcc1_period', component_property='value')
    
)
def update_tcc_fin_fig(tick,focus_var ,Lambda_slider, Lambda_amount,radio):
    period='annual'
    if Lambda_slider>99:
        Lambda_slider=99

    tickers_list = [tick]

    focus_var=[focus_var]
    
    if period=='quartal':
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date']
    
    else:
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date'].astype(str).str[0:4]

    df1 = df0.copy()


    if radio=='pour':
        Lambda=Lambda_slider/100
        df1['totalDebt'] = np.where(df0['inventory'].mul(Lambda)>df0['totalDebt'], df0['totalDebt'].mul(0.1), df0['totalDebt']-(df0['inventory'].mul(Lambda)))
        df1['interestExpense'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['interestExpense'].mul(0.1), ((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense']))
        df1['operatingIncome'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['operatingIncome'] - abs(df0['interestExpense']).mul(0.1), df0['operatingIncome'] - abs(df0['interestExpense']).mul(1-((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt']))))
        df1['EBITDA_'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['EBITDA_'] - abs(df0['interestExpense']).mul(1-0.1), df0['EBITDA_'] - abs(((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense'])))
        df1['ebit'] = np.where(df0['inventory'].mul(Lambda/1000000)>df0['totalDebt'], df0['ebit'] - abs(df0['interestExpense']).mul(1-0.1), df0['ebit'] - abs(df0['interestExpense']-(((df0['totalDebt']-(df0['inventory'].mul(Lambda))).div(df0['totalDebt'])).mul(df0['interestExpense']))))

    else:
        Lambda=Lambda_amount
        df1['totalDebt'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['totalDebt'].mul(0.1), df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))))
        df1['interestExpense'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['interestExpense'].mul(0.1), ((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense']))
        df1['operatingIncome'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['operatingIncome'] - abs(df0['interestExpense']).mul(0.1), df0['operatingIncome'] - abs(df0['interestExpense']).mul(1-((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt']))))
        df1['EBITDA_'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['EBITDA_'] - abs(df0['interestExpense']).mul(1-0.1), df0['EBITDA_'] - abs(((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense'])))
        df1['ebit'] = np.where(df0['inventory'].mul((Lambda*1000000)/(df0['inventory']))>df0['totalDebt'], df0['ebit'] - abs(df0['interestExpense']).mul(1-0.1), df0['ebit'] - abs(df0['interestExpense']-(((df0['totalDebt']-(df0['inventory'].mul((Lambda*1000000)/(df0['inventory'])))).div(df0['totalDebt'])).mul(df0['interestExpense']))))


    df_grouped_0 = df0.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_0 = df_grouped_0.reset_index()

    df_grouped_1 = df1.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_1 = df_grouped_1.reset_index()

    df_grouped_0['TCC'] = 'Without Inventory Funding'

    df_grouped_1['TCC'] = 'With Inventory Funding'


    
    df = pd.concat([df_grouped_0, df_grouped_1], axis=0)

    df['name'] = get_title(tick)

    ratios_melt = pd.melt(df, id_vars=['ticker', 'Date_formated', 'TCC', 'name'])


    ratios_melt_cols3 = ratios_melt[ratios_melt.variable.isin(focus_var)]

    tcc3_bar = px.bar(ratios_melt_cols3, x="Date_formated", y="value", 
                          facet_col='TCC', hover_name='name', height=600,text_auto=True,
                          labels={
                                          "value":"Amount ($ Millions)",
                                          "variable":" ",
                                          "Date_formated": ""
                                     },
                          color="variable", color_discrete_sequence=px.colors.qualitative.D3,
                          barmode="group")


    tcc3_bar.update_layout({"bargap": 0.2, 'bargroupgap': 0.1})
    tcc3_bar.update_xaxes(tickvals = list(ratios_melt_cols3['Date_formated']))
    tcc3_bar.update_layout({"bargap": 0.4, 'bargroupgap': 0.12})
    tcc3_bar.update_traces(textangle=0)
    tcc3_bar.update_layout(showlegend=False)
    tcc3_bar.update_layout(plot_style_blue())
    tcc3_bar.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    tcc3_bar.update_annotations(font_size=22)

    return tcc3_bar

###################################################################### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##################################################################

@app.callback(
    Output(component_id='tcc_inv_cash', component_property='figure'),
    Input(component_id='tcc1_ticker', component_property='value'),
    Input(component_id='tcc1_slider', component_property='value'),
    Input(component_id='tcc_amount', component_property='value'),
    Input(component_id='tcc1_radio', component_property='value'),
    #Input(component_id='tcc1_period', component_property='value')
    
)
def update_tcc_inv_cash(tick, Lambda_slider, Lambda_amount,radio):
    period='annual'
    if period=='quartal':
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date']
    
    else:
        df0 = df_financials_annual
        df0['Date_formated']=df0['Date'].astype(str).str[0:4]
    
    df0=df0.round(-6)
    df1 = df0.copy()
    
    if radio=='pour':
        Lambda=Lambda_slider/100

        df0['cashAndCashEquivalents']=df0['cashAndCashEquivalents']
        df1['cashAndCashEquivalents']=df0['cashAndCashEquivalents'].add(df0['inventory'].mul(Lambda))

        df0['inventory']=df0['inventory']
        df1['inventory']=df0['inventory'].mul(1-Lambda)
        
    else:
        Lambda=Lambda_amount
        
        df0['cashAndCashEquivalents']=df0['cashAndCashEquivalents']
        df1['cashAndCashEquivalents']=df0['cashAndCashEquivalents'].add(Lambda*1000000)

        df0['inventory']=df0['inventory']
        df1['inventory']=df0['inventory'].sub(Lambda*1000000)
        

    df_grouped_0 = df0.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_0 = df_grouped_0.reset_index()

    df_grouped_1 = df1.groupby(['ticker', 'Date_formated']).mean()
    df_grouped_1 = df_grouped_1.reset_index()

    df_grouped_0['TCC'] = 'Without Inventory Funding'

    df_grouped_1['TCC'] = 'With Inventory Funding'
    
    df = pd.concat([df_grouped_0, df_grouped_1], axis=0)

    df['name'] = get_title(tick)


    df_ratios = df[['ticker', 'Date_formated', 'TCC', 'name']]

    df_ratios['inventory'] = df['inventory']
    df_ratios['cashAndCashEquivalents'] = df['cashAndCashEquivalents']

    ratios_melt = pd.melt(df_ratios, id_vars=['ticker', 'Date_formated', 'TCC', 'name'])

    ratios_melt_cols3 = ratios_melt[ratios_melt.variable.isin(['inventory',
                                                               'cashAndCashEquivalents'])]


    tcc3_bar = px.bar(ratios_melt_cols3, x="Date_formated", y="value", 
                      facet_col='TCC', hover_name='name', height=600, 
                      labels={
                              "Date_formated": "",
                              "value": "Amount ($ Millions)"
                         }, text_auto=True,
                      color="variable", color_discrete_sequence=px.colors.qualitative.D3,
                      barmode="group")


    
    tcc3_bar.update_layout({"bargap": 0.2, 'bargroupgap': 0.05})
    tcc3_bar.update_traces(textangle=0)
    tcc3_bar.update_layout(legend=dict(
        orientation="h",
        title= None,
        yanchor="bottom",
        y=1.1,
        xanchor="right",
        x=1,
        font=dict(
            size=18,
            color="black"
        ),
    ))
    tcc3_bar.update_xaxes(tickvals = list(ratios_melt_cols3['Date_formated']))
    tcc3_bar.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    tcc3_bar.update_annotations(font_size=22)
    tcc3_bar.update_layout(plot_style_blue())

    return tcc3_bar

@app.callback(
    Output(component_id='bar_fin_simple', component_property='figure'),
    Input(component_id='tcc1_ticker', component_property='value'),
    Input(component_id='bar_fin_var_simple', component_property='value'),
    #Input(component_id='tcc1_period_general', component_property='value'),
)
def update_fin_fig_general(tick, focus_var):
    period='annual'
    ticker = tick
    
    # for i in range(len(focus_var)):
    #     focus_var[i] = focus_var[i] + ' ($ Millions)'
    focus_var=[focus_var]

    if period=='quartal':
        df = df_financials_annual
        df['Date_formated']=df['Date']
    
    else:
        df = df_financials_annual
        df['Date_formated']=df['Date'].astype(str).str[0:4]


    df_melt1 = pd.melt(df, id_vars = ['ticker', 'Date_formated'])
    
    df4 = df_melt1[df_melt1.variable.isin(focus_var)]

    #df4 = df4.groupby(['ticker', 'variable', 'Date_formated']).mean()
    df4.reset_index(inplace=True)
    df4.sort_values(['variable', 'Date_formated'])
    
    bar_fig4 = px.bar(df4,
                      height=600, y='value', color='variable',text_auto=True,
                      color_discrete_sequence=px.colors.qualitative.D3,
                      labels={
                          "Date_formated": "",
                          "value": "Amount ($ Millions)"
                     },
                      x='Date_formated', barmode="group", custom_data=['Date_formated'])

    bar_fig4.update_layout({"bargap": 0.4, 'bargroupgap': 0.12})
    bar_fig4.update_traces(textangle=0)
    bar_fig4.update_layout(legend=dict(
        orientation="h",
        title= None,
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            size=18,
            color="black"
        ),
    ))
    bar_fig4.update_xaxes(tickvals = list(df4['Date_formated']))
    bar_fig4.update_layout(xaxis = dict(tickfont = dict(size=25)))
    bar_fig4.update_layout(plot_style())

    return bar_fig4



@app.callback(
    Output(component_id='bar_ratio_simple', component_property='figure'),
    Input(component_id='tcc1_ticker', component_property='value'),
    Input(component_id='bar_ratio_var_simple', component_property='value'),
    #Input(component_id='tcc1_period_general', component_property='value'),
)
def update_fin_fig_general(tick, focus_var):
    period='annual'
    ticker = tick
    
    # for i in range(len(focus_var)):
    #     focus_var[i] = focus_var[i] + ' ($ Millions)'
    focus_var=[focus_var]

    if period=='quartal':
        df = df_ratios_annual
        #df['Date_formated']=df['Date']
    
    else:
        df = df_ratios_annual
        #df['Date_formated']=df['Date'].astype(str).str[0:4]


    df_melt1 = pd.melt(df, id_vars = ['ticker', 'year'])
    
    df4 = df_melt1[df_melt1.variable.isin(focus_var)]

    df4 = df4.groupby(['ticker', 'variable', 'year']).mean()
    df4.reset_index(inplace=True)
    df4.sort_values(['variable', 'year'])
    
    bar_fig4 = px.bar(df4,
                      height=600, y='value', color='variable',text_auto=True,
                      color_discrete_sequence=px.colors.qualitative.D3,
                      labels={
                          "year": "",
                          "value": "RATIO"
                     },
                      x='year', barmode="group", custom_data=['year'])

    bar_fig4.update_layout({"bargap": 0.4, 'bargroupgap': 0.12})
    bar_fig4.update_traces(textangle=0,texttemplate='%{y:.2f}')
    bar_fig4.update_layout(legend=dict(
        orientation="h",
        title= None,
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            size=18,
            color="black"
        ),
    ))
    bar_fig4.update_xaxes(tickvals = list(df4['year']))
    bar_fig4.update_layout(xaxis = dict(tickfont = dict(size=25)))
    bar_fig4.update_layout(plot_style())

    return bar_fig4


if __name__ == '__main__':
    app.run_server(port=8000, debug=True, use_reloader=False)


# In[ ]:




