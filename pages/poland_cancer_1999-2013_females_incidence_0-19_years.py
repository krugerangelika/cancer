# przypadki
import pandas as pd
import plotly
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table
dash.register_page(__name__, path="/poland_cancer_1999-2013_females_incidence0_19", suppress_callback_exceptions=True)
# ---------------------------------------------------------------
# źródło https://ecis.jrc.ec.europa.eu/explorer.php?$0-0$1-AEE$2-All$4-2$3-All$6-0,85$5-2020,2020$7-7$CEstByCancer$X0_8-3$CEstRelativeCanc$X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1
df = pd.read_excel(r"C:\Users\kruge\PycharmProjects\cancer\pages\dataset\Incidence_by_cancer_summary_Poland\Incidence_by_cancer_summary_Poland_0-19_Years_1999_2013.xlsx")
dff = df.groupby('Cancer', as_index=False)[
    ['Number','Crude rate','ASR (W)','ASR (E Old)','ASR (E New)','ICD-10']].sum()
print(dff[:5])
# ---------------------------------------------------------------
layout = html.Div([
    html.Div([
        dash_table.DataTable(
            id='datatable_id',
            data=dff.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell={
            'font_family': 'serif',
            'font_size': '26px',
            'padding': '20px',
            'minWidth': '280px',
            'width': '280px',
            'maxWidth': '280px',
            'whiteSpace': 'normal'
            },
            style_header={
            #'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'black',
            'fontWeight': 'regular'},
            style_data={
            #'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'black',
            'fontWeight': 'regular'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Cancer'},
                 'width': '40%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Number'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Crude rate'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (W)'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (E Old)'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (E New)'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
               # {'if': {'column_id': 'Cumulative Risk'},
                # 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ICD-10'},
                 'width': '10%', 'textAlign': 'left', 'height':'72%', 'fontWeight': 'bold', 'textDecoration': 'underline'},

            ],
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='bardropdown',
                         options=[
                             {'label': 'Number', 'value': 'Number'},
                             {'label': 'Crude rate', 'value': 'Crude rate'}
                         ],
                         value='Number of cases',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),
        html.Div([
            dcc.Dropdown(id='piedropdown',
                         options=[
                             {'label': 'Number', 'value': 'Number'},
                             {'label': 'Crude rate', 'value': 'Crude rate'}
                         ],
                         value='Crude rate',
                         multi=False,
                         clearable=False
                         ),
        ], className='six columns'),

    ], className='row'),
    html.Div([
        html.Div([
            dcc.Graph(id='barchart_5'),
        ], className='six columns'),

        html.Div([
            dcc.Graph(id='piechart_5'),
        ], className='six columns'),

    ], className='row'),

])
# ------------------------------------------------------------------
@callback(
    [Output('piechart_5', 'figure'),
     Output('barchart_5', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('bardropdown', 'value')]
)
def update_data(chosen_rows, piedropval, bardropval):
    if len(chosen_rows) == 0:
        df_filtered = dff[dff['Cancer'].isin(
            ['Leukaemia', 'Brain and other CNS', 'Lymphocytic Leukemia', 'Soft tissue', 'Thyroid gland', 'Bones and joints','Kidney',
             'Myeloid and Monocytic Leukemia', 'Ovary', 'Non Hodgkin lymphoma', 'Endocrine', 'Eye and adnexa',
             'Ovary'])]
    else:
        print(chosen_rows)
        df_filtered = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filtered,
        names='Cancer',
        values=piedropval,
        hole=.3,
        labels={'Cancer': 'cancer type'},
        width=2500,  # figure width in pixels
        height=720,  # figure height in pixels
        template='seaborn',
    )
    #list_chosen_cancer = df_filtered['Cancer site'].tolist()
    #df_line = df[df['Cancer site'].isin(list_chosen_cancer)]
    #line_chart = px.line(dff, x='Cancer site', y='Number of cases', color='year', height=600)
    #line_chart.update_layout(uirevision='foo')
    bar_chart = px.bar(
        data_frame=dff,
        x="Cancer",
        y="Number",
        color='Number',
        opacity=0.9,

        orientation="v",
        barmode='relative',
        labels={"Cancer": "cancer",},  # map the labels of the figure
        title='Incidence by cancer - Poland - 1999-2013 - 0-19 years - Females',  # figure title
        width=2500,  # figure width in pixels
        height=720,  # figure height in pixels
        template='ggplot2', #'seaborn', 'ggplot2', 'plotly_dark', 'xgridoff'
        log_y=True,                 # y-axis is log-scaled
        #animation_frame='year',
        color_continuous_midpoint=200,


    ).update_layout(showlegend=True, xaxis={'categoryorder': 'total ascending'})
    return pie_chart, bar_chart


# ------------------------------------------------------------------