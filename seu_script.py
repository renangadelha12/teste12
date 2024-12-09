import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

topo = ['Date',
'Time',
'Temperatura',
'Hi temp',
'Low Temp',
'Umidade',
'Dew Pt.',
'Velocidade do Vento',
'Wind Dir',
'Wind Run',
'Hi Speed',
'Hi Dir',
'Wind Chill',
'Heat Index',
'THW Index',
'THSW Index',
'Pressão Atm.',
'Precipitação',
'Rain Rate',
'Solar Rad',
'Solar Energy',
'Hi Solar Rad',
'UVI',
'UV Dose',
'Hi UV',
'Heat D-D',
'Cool D-D',
'In Temp',
'In Hum',
'In Dew',
'In Heat',
'In EMC',
'In Air Density',
'ET',
'Wind Samp',
'Wind TX',
'ISS Recept',
'Arc Int.']
if 1!=2:
    dados='davis_teste.txt'
    
    davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float,'UV Dose':float,'Bar':float,'Dew Pt.':float,'Heat Index':float}, na_values=['---','------'], header=1,names=topo)

    #davis=davis.sort_values(by='Date')
    davis["Date"] = pd.to_datetime(davis["Date"])
    davis['Dia']=davis['Date'].dt.day
    davis['Year']=davis['Date'].dt.year
    davis['Mês']=davis['Date'].dt.month
    davis['Mês2']=davis['Date'].dt.month
    davis['Year']= pd.to_numeric(davis['Year'], errors='coerce')
   # bar_avg=davis[['Bar','Year']].groupby('Year').mean()
    

    davis_2024=davis[davis['Year']==2024]
    '''davis['Mês'] = davis['Mês'].replace({1: 'Janeiro', 2: 'Fevereiro', 3:'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                                              7: 'Julho',8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
                                              })
    
    davis = davis[davis['Year'] != 2018]'''

from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])

ano_selecionado = 2020
anos = davis['Year'].unique()
anos_lista = list(anos)
ano_selecionado = anos_lista[0]
messes = davis['Mês'].unique()
messes_lista = list(messes)
mes_selecionado = messes_lista[0]
##############
d_t_mes=davis[['Date','Year','Dia','Mês2','UVI']]
d_t_mes=d_t_mes.sort_values(by='Date')
d_t_mes=d_t_mes.sort_values(by='Date')
anos_do_df=d_t_mes['Year'].unique()
messes_do_df=d_t_mes['Mês2'].unique()
anos_do_df_lista=list(anos_do_df)
dias_do_df=d_t_mes['Dia'].unique()
dias_do_df_lista=list(dias_do_df)
topo_lista=list(topo)

app.layout = dbc.Container([
    html.H2(children='Selecione um ano'),
    dcc.Dropdown(
        id='anos-dropdown',
        options=[{'label': str(ano), 'value': ano} for ano in anos_lista],
        value=ano_selecionado
    ),
    html.Div(id='output-container'),

    dbc.Row([
        html.Div(id='output-text', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.RadioItems(
            options=[{"label": x, "value": x} for x in ['Pressão Atm.', 'Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'UVI']],
            value='Temperatura',
            inline=True,
            id='radio-buttons-final'
        )
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(id='my-table', page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),
    html.Div([
    html.H2("Distribuição Pluviométrica"),
    dcc.Graph(id='pie-chart')
    ]),
    html.H1(children='Para fazer uma análise em um dia específico, selecione um dia nos quadros abaixo.'),
    html.H4(children='Aqui selecione um Ano:'),
    
    dcc.Dropdown(
        id='a-dropdown',
        options=[{'label': str(anos_do_df), 'value': anos_do_df} for anos_do_df in anos_do_df_lista],
        value=anos_do_df[0]
    ),
    html.H4(children='Aqui selecione um Mês:'),

    dcc.Dropdown(
        id='messes-dropdown',
        options=[{'label': str(messes), 'value': messes} for messes in messes_lista],
        value=messes[0]
    ),
    html.H4(children='Aqui selecione um Dia:'),

    dcc.Dropdown(
        id='dia-dropdown',
        options=[{'label': str(dias_do_df), 'value': dias_do_df} for dias_do_df in dias_do_df_lista],
        value=messes[0]
    ),
    
    html.Div(id='output-container2'),
    html.Div([
    html.H2("Gráfico Selecionável"),
    html.H4(children='Entre com a Variável que você deseja verificar:'),
    dcc.Dropdown(
        id='variaveis',
        options=[{'label': str(topo), 'value': topo} for topo in topo_lista],
        value=topo[3]
    ),
    dcc.Graph(id='fig3')
    ]),
    
], fluid=True)

@app.callback(
    [Output(component_id='my-first-graph-final', component_property='figure'),
     Output('pie-chart', 'figure'),
     Output('fig3', 'figure'),
     Output('output-text', 'children'),
     Output('my-table', 'columns'),
     Output('my-table', 'data'),
     
     ],
    [Input(component_id='anos-dropdown', component_property='value'),
     Input(component_id='radio-buttons-final', component_property='value'),
     Input(component_id='messes-dropdown', component_property='value'),
     Input(component_id='a-dropdown', component_property='value'),
     Input(component_id='dia-dropdown', component_property='value'),
     Input(component_id='variaveis', component_property='value'),
     ]
)
def update_output(selected_year, col_chosen, selected_mes,selected_ano,selected_dia,variavel):
    global davis2
    global ano_selecionado
    global mes_selecionado
    global dia_selecionado
    ano_selecionado = selected_year
    ano_especifico=selected_ano
    mes_selecionado = selected_mes
    dia_selecionado=selected_dia
    variavels=variavel
    
    
    davis2 = davis[davis['Year'] == ano_selecionado]
    
    d_dash_max = davis2[['Mês2', 'Mês', 'UVI']].groupby('Mês2').max()
    d_dash_sum = davis2[['Mês2', 'Precipitação']].groupby('Mês2').sum()
    d_dash_médias = davis2[['Mês2', 'Mês', 'Pressão Atm.', 'Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'UVI']].groupby('Mês2').mean()
    d_dash_precp = pd.DataFrame({
        'Mês': d_dash_médias['Mês'],
        'Precipitação': d_dash_sum['Precipitação']
    })
    d_table_p1 = davis2[['Mês2', 'Mês', 'Pressão Atm.', 'Temperatura', 'Umidade', 'Velocidade do Vento']].groupby('Mês2').mean()
    d_table_p2 = davis2[['Mês2', 'Precipitação']].groupby('Mês2').sum()
    d_table_p3 = davis2[['Mês2', 'UVI']].groupby('Mês2').max()
    
    
    
    d_t = pd.DataFrame({
        'Mês': d_table_p1['Mês'],
        'Mês_c': d_table_p1['Mês'],
        'Pressão Atm (hPa).': d_table_p1['Pressão Atm.'],
        'Temperatura (°C)': d_table_p1['Temperatura'],
        'Umidade (%)': d_table_p1['Umidade'],
        'Velocidade do Vento (m/s)': d_table_p1['Velocidade do Vento'],
        'Precipitação (mm/mês)': d_table_p2['Precipitação'],
        'UVI': d_table_p3['UVI'],
    })
    
    output_text = f'Dash Board Davis LAVAT - Ano Observado: {selected_year} '
    if mes_selecionado <10:
        mes_selecionado=f'0{mes_selecionado}'
    if dia_selecionado<10:
        dia_selecionado=f'0{dia_selecionado}'

    dia_select=f'{ano_especifico}-{mes_selecionado}-{dia_selecionado}'
    dia_escholido_dropdown=davis[davis['Date'] == dia_select]
    dia_escholido_dropdown["Date"] = pd.to_datetime(dia_escholido_dropdown["Date"])
    #dia_escholido_dropdown=dia_escholido_dropdown.sort_values(by='Time')
    #dia_escholido_dropdown=davis[davis['Date'] == '2023-12-12']
    d_t['Mês_c'] = d_t['Mês_c'].replace({1: 'Janeiro', 2: 'Fevereiro', 3:'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                                          7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'})
    messes_c = d_t['Mês_c']
    
    
    if col_chosen == 'UVI':
        fig = px.line(d_dash_max, x='Mês', y=col_chosen)
    elif col_chosen == 'Precipitação':
        fig = px.line(d_dash_precp, x='Mês', y=col_chosen)
    else:
        fig = px.line(d_dash_médias, x='Mês', y=col_chosen)
    
   
    fig2 = px.pie(d_t, values='Precipitação (mm/mês)', names=messes_c, title='Distribuição Pluviométrica')
    fig3 = px.line(dia_escholido_dropdown, x=dia_escholido_dropdown['Time'], y=variavels)

    columns = [{'name': col, 'id': col} for col in d_t.columns]
    data = d_t.reset_index().to_dict('records')
    
    print(dia_escholido_dropdown)
    return fig, fig2,fig3, output_text, columns, data





if __name__ == '__main__':
    app.run_server(debug=True, port=8052)