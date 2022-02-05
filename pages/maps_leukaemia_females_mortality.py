import pandas as pd
import plotly
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State

df = pd.read_csv(r"C:\Users\kruge\PycharmProjects\cancer\pages\dataset\maps_leukaemia_females_mortality.csv", sep=';',
                 encoding='latin-1')
df = df[df['Year'] == 2020]

df['id'] = df['ISO code']
df.set_index('id', inplace=True, drop=True)
print(df.columns)

dash.register_page(__name__, path="/maps_leukaemia_females_mortality", suppress_callback_exceptions=True, prevent_initial_callbacks=True)

layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity_1',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": False}
            if i == "ISO code" or i == "Year" or i == "id"
            else {"name": i, "id": i, "deletable": True, "selectable": True}
            for i in df.columns
        ],
        data=df.to_dict('records'),  # the contents of the table
        editable=True,  # allow editing of data inside all cells
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",  # allow users to select 'multi' or 'single' rows
        row_deletable=True,  # choose if user can delete a row (True) or not (False)
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=15,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'minWidth': 100, 'maxWidth': 100, 'width': 100
        },
        style_cell_conditional=[  # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Population', 'ISO code']
        ],
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container_2'),
    html.Div(id='choromap-container_7'),
    html.Div(id='choromap-container_8'),
    html.Div(id='choromap-container_9'),
    html.Div(id='choromap-container_10'),
    html.Div(id='choromap-container_11'),
    html.Div(id='choromap-container_12')
])


# -------------------------------------------------------------------------------------
# Create bar chart
@callback(
    Output(component_id='bar-container_2', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity_1', component_property='selected_rows'),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity_1', component_property='active_cell'),
     Input(component_id='datatable-interactivity_1', component_property='selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    dff = pd.DataFrame(all_rows_data)

    # used to highlight selected countries on bar chart
    colors = ['#b55573' if i in slctd_row_indices else '#cf446b'
              for i in range(len(dff))]

    if "Population" in dff and "Value" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="Population",
                          y='Value',
                          labels={"x"},
                          width=2500,  # figure width in pixels
                          height=720,  # figure height in pixels
                      ).update_layout(showlegend=True, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors)
                      )
        ]


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# Create choropleth map
@callback(
    Output(component_id='choromap-container_7', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="europe",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, leukaemia, females, all ages, Europe",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------
@callback(
    Output(component_id='choromap-container_8', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="asia",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, leukaemia, females, all ages, Asia",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------
@callback(
    Output(component_id='choromap-container_9', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="africa",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, leukaemia, females, all ages, Africa",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------
@callback(
    Output(component_id='choromap-container_10', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="north america",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, leukaemia, females, all ages, Europe, North America",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------
@callback(
    Output(component_id='choromap-container_11', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="south america",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, leukaemia, females, all ages, Europe, South America",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------
@callback(
    Output(component_id='choromap-container_12', component_property='children'),
    [Input(component_id='datatable-interactivity_1', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity_1', component_property='derived_virtual_selected_rows')]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [5 if i in slctd_row_indices else 1
               for i in range(len(dff))]

    if "ISO code" in dff and "Value" in dff and "Population" in dff:
        return [
            dcc.Graph(id='choropleth',
                      style={'height': 700},
                      figure=px.choropleth(
                          color_continuous_scale="rdbu",
                          range_color=(0, 12),
                          data_frame=dff,
                          locations="ISO code",
                          scope="world",
                          color="Value",
                          title="Estimated crude mortality rates in 2020, all cancers, females, all ages, World",
                          template='seaborn',
                          hover_data=['Population', 'Value'],

                      ).update_layout(showlegend=True, title=dict(font=dict(size=28), x=0.5, xanchor='center'))
                      .update_traces(marker_line_width=borders, hovertemplate="<b>%{customdata[0]}</b><br><br>" +
                                                                              "%{customdata[1]}")
                      )

        ]


# -------------------------------------------------------------------------------------

# Highlight selected column
@callback(
    Output('datatable-interactivity_1', 'style_data_conditional'),
    [Input('datatable-interactivity_1', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#964d70'
    } for i in selected_columns]

# -------------------------------------------------------------------------------------
