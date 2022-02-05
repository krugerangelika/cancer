# Śmiertelność
import pandas as pd
import plotly
import plotly.express as px

import dash
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table

dash.register_page(__name__, suppress_callback_exceptions=True,  path="/europe_cancer_2020_females_mortality")

# ---------------------------------------------------------------
# źródło https://ecis.jrc.ec.europa.eu/explorer.php?$0-0$1-AEE$2-All$4-2$3-All$6-0,85$5-2020,2020$7-7$CEstByCancer$X0_8-3$CEstRelativeCanc$X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1X1_8-3$X1_9-AE27$CEstBySexByCancer$X2_8-3$X2_-1-1
df = pd.read_excel(
    r"C:\Users\kruge\PycharmProjects\cancer\pages\dataset\Estimated_mortality_by_cancer_summary_europe\Estimated_mortality_by_cancer_summary_female_europe.xlsx")

dff = df.groupby('Cancer site', as_index=False)[
    ['Number of cases', 'Crude rate', 'ASR (European new)', 'ASR (European old)', 'ASR (world)', 'Cumulative risk',
     'year']].sum()
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
                # 'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'black',
                'fontWeight': 'regular'},
            style_data={
                # 'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'black',
                'fontWeight': 'regular'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Cancer site'},
                 'width': '15%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Number of cases'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Crude rate'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (European new)'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (European old)'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'ASR (world)'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Cumulative risk'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold'},
                {'if': {'column_id': 'year'},
                 'width': '10%', 'textAlign': 'left', 'height': '72%', 'fontWeight': 'bold',
                 'textDecoration': 'underline'},

            ],
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='bardropdown',
                         options=[
                             {'label': 'Number of cases', 'value': 'Number of cases'},
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
                             {'label': 'Number of cases', 'value': 'Number of cases'},
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
            dcc.Graph(id='barchart_19'),
        ], className='six columns'),

        html.Div([
            dcc.Graph(id='piechart_19'),
        ], className='six columns'),

    ], className='row'),

])


# ------------------------------------------------------------------
@callback(
    [Output('piechart_19', 'figure'),
     Output('barchart_19', 'figure')],
    [Input('datatable_id', 'selected_rows'),
     Input('piedropdown', 'value'),
     Input('bardropdown', 'value')]
)
def update_data(chosen_rows, piedropval, bardropval):
    if len(chosen_rows) == 0:
        df_filtered = dff[dff['Cancer site'].isin(
            ['Breast', 'Colorectum', 'Corpus Uteri', 'Lung', 'Kidney', 'Cervic uteri', 'Leukaemia',
             'Hodgkin lymphoma', 'Ovary', 'Pancreas', 'Stomach', 'Thyroid',
             'Ovary'])]
    else:
        print(chosen_rows)
        df_filtered = dff[dff.index.isin(chosen_rows)]

    pie_chart = px.pie(
        data_frame=df_filtered,
        names='Cancer site',
        values=piedropval,
        hole=.3,
        labels={'Cancer site': 'cancer type'},
        width=2500,  # figure width in pixels
        height=720,  # figure height in pixels
        template='seaborn',
    )
    # list_chosen_cancer = df_filtered['Cancer site'].tolist()
    # df_line = df[df['Cancer site'].isin(list_chosen_cancer)]
    # line_chart = px.line(dff, x='Cancer site', y='Number of cases', color='year', height=600)
    # line_chart.update_layout(uirevision='foo')
    bar_chart = px.bar(
        data_frame=dff,
        x="Cancer site",
        y="Number of cases",
        color='Number of cases',
        opacity=0.9,
        orientation="v",
        barmode='relative',
        labels={"Cancer Site": "cancer site",
                "gender": "Gender"},  # map the labels of the figure
        title='Incidence',  # figure title
        width=2500,  # figure width in pixels
        height=720,  # figure height in pixels
        template='ggplot2',  # 'seaborn', 'ggplot2', 'plotly_dark', 'xgridoff'
        log_y=True,  # y-axis is log-scaled
        animation_frame='year',
        color_continuous_midpoint=200,

    ).update_layout(showlegend=True, xaxis={'categoryorder': 'total ascending'})
    return pie_chart, bar_chart
