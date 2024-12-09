import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
topo = ['Data',
'Hora',
'Temperatura',
'Temp. Máxima',
'Temp. Mínima',
'Umidade',
'Ponto de Orvalho',
'Velocidade do Vento',
'Direção do Vento',
'Distância Percorrida pelo Vento',
'Velocidade Máxima',
'Direção Máxima',
'Sensação Térmica',
'Índice de Calor',
'Índice THW',
'Índice THSW',
'Pressão Atmosférica',
'Precipitação',
'Taxa de Chuva',
'Radiação Solar',
'Energia Solar',
'Radiação Solar Máxima',
'UVI',
'Dose UV',
'Índice UV Máximo',
'Grau-dias de Aquecimento',
'Grau-dias de Resfriamento',
'Temp. Interna',
'Umidade Interna',
'Ponto de Orvalho Interno',
'Calor Interno',
'EMC Interno (Conteúdo de Umidade em Equilíbrio)',
'Densidade do Ar Interna',
'Evapotranspiração',
'Amostragem do Vento',
'Transmissão do Vento',
'Receptor ISS',
'Intervalo de Arquivamento']

if 1!=2:
    dados='c:/AVELL/Davis/davis_teste_dash.txt'
    
    davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float,'UV Dose':float,'Bar':float,'Dew Pt.':float,'Heat Index':float}, na_values=['---','------'], header=1,names=topo)

    #davis=davis.sort_values(by='Date')
    davis["Data"] = pd.to_datetime(davis["Data"])
    davis['Dia']=davis['Data'].dt.day
    davis['Year']=davis['Data'].dt.year
    davis['Mês']=davis['Data'].dt.month
    davis['Mês2']=davis['Data'].dt.month
    davis['Year']= pd.to_numeric(davis['Year'], errors='coerce')
   # bar_avg=davis[['Bar','Year']].groupby('Year').mean()
    

    davis_2024=davis[davis['Year']==2024]
    '''davis['Mês'] = davis['Mês'].replace({1: 'Janeiro', 2: 'Fevereiro', 3:'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
                                              7: 'Julho',8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
                                              })
    
    davis = davis[davis['Year'] != 2018]'''

davis['Data'] = pd.to_datetime(davis['Data'])

# Extrai a data no formato 'YYYY-MM-DD'
dias = davis['Data'].dt.strftime('%Y-%m-%d')
dias_lista=dias.unique()
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
d_t_mes=davis[['Data','Year','Dia','Mês2','UVI']]
d_t_mes=d_t_mes.sort_values(by='Data')
d_t_mes=d_t_mes.sort_values(by='Data')
anos_do_df=d_t_mes['Year'].unique()
messes_do_df=d_t_mes['Mês2'].unique()
anos_do_df_lista=list(anos_do_df)
dias_do_df=d_t_mes['Dia'].unique()
dias_do_df_lista=list(dias_do_df)
topo_lista=list(topo)

tipo_de_analise = ['Média', 'Máximo', 'Mínimo']
tipo_lista = list(tipo_de_analise)
data = {
    'Ano': davis['Year'],
    'Mês': davis['Mês2'],
    'Variável': davis['UVI']
}
df = pd.DataFrame(data)

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
            options=[{"label": x, "value": x} for x in ['Pressão Atmosférica', 'Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'UVI']],
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
    
    html.H4(children='Aqui selecione um Dia:'),

    dcc.Dropdown(
        id='dia_nv-dropdown',
        options=[{'label': str(dias), 'value': dias} for dias in dias_lista],
        value=dias[0]
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
    html.H1("Heatmap de Análises Mensais por Ano"),
    html.H4(children='Entre com a Variável que você deseja verificar:'),
    dcc.Dropdown(
        id='variaveis-2',
        options=[{'label': str(topo), 'value': topo} for topo in topo_lista],
        value=topo_lista[3],  # Ajuste conforme necessário
    ),
    html.H4(children='Entre com o tipo de análise (Máximo, Média ou Mínimo):'),
    dcc.Dropdown(
        id='tipo_de_analise-2',
        options=[{'label': tipo, 'value': tipo} for tipo in tipo_lista],
        value=tipo_lista[0],  # Valor padrão
    ),
    dcc.Graph(id='heatmap-graph')
    
], fluid=True)

@app.callback(
    [Output(component_id='my-first-graph-final', component_property='figure'),
     Output('pie-chart', 'figure'),
     Output('fig3', 'figure'),
     Output('heatmap-graph', 'figure'),
     Output('output-text', 'children'),
     Output('my-table', 'columns'),
     Output('my-table', 'data'),
     #Output(component_id='heatmap-graph', component_property='figure'),
     
     ],
    [Input(component_id='anos-dropdown', component_property='value'),
     Input(component_id='radio-buttons-final', component_property='value'),
     Input(component_id='dia_nv-dropdown', component_property='value'),
     Input(component_id='variaveis', component_property='value'),
     Input(component_id='variaveis-2', component_property='value'),
     Input(component_id='tipo_de_analise-2', component_property='value')
     ]
)
def update_output(selected_year, col_chosen,dia_s,variavel,v_selected,s_type):    
    global davis2
    global s_day
    ano_selecionado = selected_year
    variavel_heatmap=v_selected
    static=s_type

    s_day=dia_s
    variavels=variavel
    
    
    davis2 = davis[davis['Year'] == ano_selecionado]
    
    d_dash_max = davis2[['Mês2', 'Mês', 'UVI']].groupby('Mês2').max()
    d_dash_sum = davis2[['Mês2', 'Precipitação']].groupby('Mês2').sum()
    d_dash_médias = davis2[['Mês2', 'Mês', 'Pressão Atmosférica', 'Temperatura', 'Umidade', 'Velocidade do Vento', 'Precipitação', 'UVI']].groupby('Mês2').mean()
    d_dash_precp = pd.DataFrame({
        'Mês': d_dash_médias['Mês'],
        'Precipitação': d_dash_sum['Precipitação']
    })
    d_table_p1 = davis2[['Mês2', 'Mês', 'Pressão Atmosférica', 'Temperatura', 'Umidade', 'Velocidade do Vento']].groupby('Mês2').mean()
    d_table_p2 = davis2[['Mês2', 'Precipitação']].groupby('Mês2').sum()
    d_table_p3 = davis2[['Mês2', 'UVI']].groupby('Mês2').max()
    
    
    
    d_t = pd.DataFrame({
        'Mês': d_table_p1['Mês'],
        'Mês_c': d_table_p1['Mês'],
        'Pressão Atmosférica (hPa).': d_table_p1['Pressão Atmosférica'],
        'Temperatura (°C)': d_table_p1['Temperatura'],
        'Umidade (%)': d_table_p1['Umidade'],
        'Velocidade do Vento (m/s)': d_table_p1['Velocidade do Vento'],
        'Precipitação (mm/mês)': d_table_p2['Precipitação'],
        'UVI': d_table_p3['UVI'],
    })
    
    output_text = f'Dash Board Davis LAVAT - Ano Observado: {selected_year} - {variavel_heatmap} -{static} '
    
    dia_escholido_dropdown=davis[davis['Data'] == s_day]
    dia_escholido_dropdown["Date"] = pd.to_datetime(dia_escholido_dropdown["Data"])
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
    fig3 = px.line(dia_escholido_dropdown, x=dia_escholido_dropdown['Hora'], y=variavels)

    df['Variável'] = davis[variavel_heatmap]
    selected_analysis=static
    # Definindo a função de agregação com base no tipo de análise selecionada
    if selected_analysis == 'Média':
        agg_func = 'mean'
    elif selected_analysis == 'Máximo':
        agg_func = 'max'
    elif selected_analysis == 'Mínimo':
        agg_func = 'min'

    # Calculando a análise da variável por Ano e Mês
    df_pivot = df.pivot_table(index='Ano', columns='Mês', values='Variável', aggfunc=agg_func)
    
    # Garantir que todos os meses de 1 a 12 estejam presentes
    df_pivot = df_pivot.reindex(columns=np.arange(1, 13))

    # Gerando o heatmap
    fig_h = px.imshow(df_pivot, 
                    labels=dict(x="Mês", y="Ano", color=selected_analysis),
                    x=df_pivot.columns,  # Colunas são os meses
                    y=df_pivot.index,    # Linhas são os anos
                    aspect="auto",
                    text_auto=True)

    # Atualizando layout para garantir que todos os anos apareçam no eixo y
    fig_h.update_yaxes(tickvals=df_pivot.index,  # Garantindo que todos os anos sejam mostrados
                     ticktext=[str(year) for year in df_pivot.index])  # Convertendo anos para string
    
    fig_h.update_layout(title=f'{selected_analysis} Mensais de {variavel_heatmap} ao Longo dos Anos',
                      xaxis_title="Mês",
                      yaxis_title="Ano")



    columns = [{'name': col, 'id': col} for col in d_t.columns]
    data = d_t.reset_index().to_dict('records')
    
    return fig, fig2,fig3,fig_h, output_text, columns, data




if __name__ == '__main__':
    app.run_server(debug=True)
