# -*- coding: utf-8 -*-
import sys
import base64
import datetime
import time
import io
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq  # #
import dash_html_components as html
import dash_table  # #
import pandas as pd
import plotly.graph_objects as go
from dash import no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from numpy import trapz
from openpyxl import Workbook

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

# connect OPC

# get data from MAF

getDataFromModbus = []

extra_data_list = [
    'Mass de Bois', 'Volume gaz', 'Vitesse de rotation', 'Puissance Thermique',
    'Puissance Electrique', 'CO', 'CO2', 'NO', 'NOX', 'Temperature de Fumée'
]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# 4 page
index_page = html.Div(className="indexpage",
                      children=[
                          dcc.Link(html.Button('Go to ENERBAT', id="indexPageStyle"), href='/page-1'),
                          html.Br(),
                          dcc.Link(html.Button('Go to X', id="indexPageStyle"), href='/page-2'),
                          html.Br(),
                          dcc.Link(html.Button('Go to Y', id="indexPageStyle"), href='/page-3'),
                          html.Br(),
                          dcc.Link(html.Button('Go to Z', id="indexPageStyle"), href='/page-4'),
                      ])

page_1_layout = html.Div(
    className='main_container',
    children=[
        html.Div(className="four-columns-div-user-controls",
                 children=[
                     html.Div([daq.PowerButton(id='my-toggle-switch',
                                               label={'label': 'Connect OPC',
                                                      'style': {'fontSize': '22px', 'fontWeight': "bold"}},
                                               labelPosition='bottom', on=False, size=100, color="green",
                                               className='dark-theme-control'), html.Div(
                         dcc.Upload(
                             id='upload-data',
                             children=html.Div([
                                 'Drag and Drop or ',
                                 html.A('Select Files for work')
                             ]),
                             style={
                                 'visibility': 'hidden',
                             },
                             # Allow multiple files to be uploaded
                             multiple=True,

                         ),

                     )], ),

                     html.Div(id="openOPCDiv", children=[], style={'visibility': 'hidden'}),
                     html.Div(className='userControlDownSide',
                              children=[
                                  html.Div(className='userControlDownLeftSide',
                                           children=[
                                               html.Div(id="opcLoad",
                                                        className='div-for-dropdown',
                                                        children=[], ),
                                               html.Div(dcc.Interval(
                                                   id='interval',
                                                   interval=5000,
                                                   n_intervals=3,

                                               )),
                                               # html.Div(id = 'ceyhun',
                                               #          style = {'visibility' : 'hidden', 'height' :'1rem' }),
                                               html.Div(className="file_db_button",
                                                        children=[
                                                            html.Button('File', id='file_save', n_clicks=0, ),
                                                            html.Button('Database', id='db_save', n_clicks=0, ),
                                                        ]),
                                               html.Div(id='pointLeftFirst', children=[], style={'display': 'None'}),
                                               html.Div(id='pointLeftSecond', children=[], style={'display': 'None'}),
                                               html.Div(id='pointRightFirst', children=[], style={'display': 'None'}),
                                               html.Div(id='pointRightSecond', children=[], style={'display': 'None'}),
                                               html.Div(id='leftSideChecklistValue', children=[],
                                                        style={'display': 'None'}),
                                               html.Div(id='leftSidedroptValue', children=[],
                                                        style={'display': 'None'}),
                                               html.Div(id='leftSideChecklistValueHidden', children=[],
                                                        style={'display': 'None'}),
                                               html.Div(id='tab2hiddenValuex_axis', style={'display': 'None'},
                                                        children=[]),
                                               html.Div(id='tab2hiddenValuey_axis', style={'display': 'None'},
                                                        children=[]),
                                               html.Div(id='hiddenTextHeader', children=[], style={'display': 'None'}),
                                               html.Div(id='hiddenTextNote', children=[], style={'display': 'None'}),
                                               html.Div(id='hiddenTextxaxis', children=[], style={'display': 'None'}),
                                               html.Div(id='hiddenTextyaxis', children=[], style={'display': 'None'}),
                                               html.Div(id='hiddenShapeVal', children=[], style={'display': 'None'}),
                                               html.Div(id='hiddenShapeDate', children=[],
                                                        style={'display': 'None'}), ], ),
                                  html.Div(id='hiddenDifferance', children=[], style={'display': 'None'}),
                                  html.Div(id='retrieve', children=[], style={'display': 'None'}),
                                  html.Div(id='datatablehidden', children=[], style={'display': 'None'}),
                                  html.Div(id='radiographhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='sliderHeightTab1hidden', children=[], style={'display': 'None'}),
                                  html.Div(id='sliderWidthTab1hidden', children=[], style={'display': 'None'}),
                                  html.Div(id='minimumValueGraphhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='firstchoosenvalhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='secondchoosenvalhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='leftintegralfirsthidden', children=[], style={'display': 'None'}),
                                  html.Div(id='leftintegralsecondhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='rightintegralfirsthidden', children=[], style={'display': 'None'}),
                                  html.Div(id='rightintegralsecondhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='tableinteractivehidden', children=[], style={'display': 'None'}),
                                  html.Div(id='writeexcelhidden', children=[], style={'display': 'None'}),
                                  html.Div(id='aaaa', children=[], style={'display': 'None'}),
                                  html.Div(id='bbbb', children=[], style={'display': 'None'})
                              ]),
                 ]),

        html.Div(className="eight-columns-div-for-charts",
                 children=[
                     html.Div(
                         className='right-upper',
                         children=[
                             html.Div([
                                 dcc.Tabs(
                                     id="tabs-with-classes",
                                     value='tab-1',
                                     parent_className='custom-tabs',
                                     className='custom-tabs-container',
                                     children=[
                                         dcc.Tab(
                                             id="tab1",
                                             label='Tab for one option',
                                             value='tab-1',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected',
                                             children=[],
                                         ),
                                         dcc.Tab(
                                             id='tab4',
                                             label='Tab for one option',
                                             value='tab-4',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected',
                                             children=[
                                             ]
                                         ),
                                         dcc.Tab(
                                             id='tab3',
                                             label='Tab for one option',
                                             value='tab-3', className='custom-tab',
                                             # style = {'visibility' : 'hidden'},
                                             selected_className='custom-tab--selected'
                                         ),
                                         dcc.Tab(
                                             id="tab2",
                                             label='Tab for one option',
                                             value='tab-2',
                                             className='custom-tab',
                                             style={'visibility': 'hidden'},
                                             selected_className='custom-tab--selected'
                                         ),
                                         dcc.Tab(
                                             id="tab5",
                                             label='Tab for one option',
                                             value='tab-5',
                                             className='custom-tab',
                                             style={'visibility': 'hidden'},
                                             selected_className='custom-tab--selected'
                                         ),
                                     ]),
                                 html.Div(id='tabs-content-classes'),

                             ]),

                         ]),

                 ]
                 ),
        # dcc.Graph(id = "first_value_graph", config = {'displayModeLine': True}, animate=True)
    ]),

page_2_layout = html.Div([
    dcc.Link('Go to MODBUS', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Y', href='/page-3'),
    html.Br(),
    dcc.Link('Go to Z', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_3_layout = html.Div([
    dcc.Link('Go to MODBUS', href='/page-1'),
    html.Br(),
    dcc.Link('Go to X', href='/page-2'),
    html.Br(),
    dcc.Link('Go to Z', href='/page-4'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_4_layout = html.Div([
    dcc.Link('Go to MODBUS', href='/page-1'),
    html.Br(),
    dcc.Link('Go to X', href='/page-2'),
    html.Br(),
    dcc.Link('Go to Y', href='/page-3'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


# surf between pages
# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    else:
        return index_page


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df['index'] = df.index
            df = df.reindex(columns=sorted(df.columns, reverse=True))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dash_table.DataTable(
            id='datatable-interactivity',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i, "deletable": True, "selectable": True} for i in df.columns],
            editable=True,
            page_size=50,
            style_table={'height': '500px', 'overflowY': 'auto', 'width': '98%'},
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0,
                'fontSize': '1rem',
                'TextAlign': 'center',
            },
            fixed_rows={'headers': True},
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'center',
                    'width': '8%'}

                for c in df.columns if c != 'date'],
            # style_cell_conditional=[
            # {'if': {'column_id': 'date'},
            #  'width': '15%'}

            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            # row_selectable="multi",
            # row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            export_format='xlsx',
            export_headers='display',
            merge_duplicate_headers=True
        ),

        html.Hr(),  # horizontal line
    ])


@app.callback([Output('datatablehidden', 'children'), Output('retrieve', 'children')],

              [Input('upload-data', 'contents'), Input("my-toggle-switch", "on"), ],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified'),
               State('retrieve', 'children'),
               State('datatablehidden', 'children')])
def update_output(list_of_contents, on, list_of_names, list_of_dates, retrieve, content):
    if on == 0:
        raise PreventUpdate
    if list_of_contents is not None:

        content = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        retrieve = list_of_names
        print('sahin', retrieve)
        return content, retrieve
    else:
        return (no_update, no_update)


@app.callback(Output('output-data-upload', 'children'),
              [Input('datatablehidden', 'children')],
              )
def retrieve(retrieve):
    #     # if len(choosen)==0:
    return retrieve
    # else : return no_update


@app.callback(Output('tab2DashTable', 'children'),
              [Input('datatablehidden', 'children')],
              )
def retrieve2(retrieve):
    #     # if len(choosen)==0:
    return retrieve
    # else : return no_update


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': 'red'
    } for i in selected_columns]

    # Output("opcLoad","children") : for load left and right side,
    # for this created a hiddev div as opcLoad,
    # Output('tab2','children') : also hidden tab, for the graph


@app.callback([Output("opcLoad", "children"), Output('upload-data', 'style')],
              [Input("my-toggle-switch", "on")]

              )
def opcLoadingData(on):
    ocploadlist = []

    if on == 1:
        visibilty = {'width': '100%',
                     'height': '35px',
                     'lineHeight': '25px',
                     'borderWidth': '1px',
                     'borderStyle': 'dashed',
                     'borderRadius': '5px',
                     'textAlign': 'center',
                     'margin': '20px',
                     'visibility': 'visible'}
        data_list = ['CoAd', 'ComManCoP2', 'ComManCoP3P4P5', 'ComManPompeSec', 'CompteurEnergie', 'CoP2',
                     'CtempDepChauff',
                     'D1', 'D2', 'D3', 'D4', 'MarcheBruleur', 'Teg', 'SdeBasBouMelange', 'SdeBasHauMelange', 'TambN3',
                     'Tb1',
                     'Tb2', 'Tb3', 'Tb4', 'TdepPLC', 'Teb', 'Tec', 'Teev', 'TempminMaf', 'Text', 'Tsb', 'Tsc', 'Tsev']

        ocploadlist = html.Div(className="userControlDownSideCreated",
                               children=[html.Div(className="userControlDownLeftSide",

                                                  children=[html.Div(className='aa',
                                                                     children=[html.Div(
                                                                         dcc.Dropdown(id='dropdownLeft',
                                                                                      options=[{'label': i, 'value': i}
                                                                                               for i in data_list if
                                                                                               i != 'date'],
                                                                                      multi=False,
                                                                                      style={"cursor": "pointer"},
                                                                                      className='stockSelectorClass',
                                                                                      clearable=False,
                                                                                      placeholder='Select your parameters...',
                                                                                      ),
                                                                     ),
                                                                         html.Div([html.Button('Show', id='showLeft',
                                                                                               n_clicks=0,
                                                                                               style={'height': '40px',
                                                                                                      'width': '80px',
                                                                                                      'fontSize': '1.2rem'}),
                                                                                   html.Button('Delete', id='clearLeft',
                                                                                               n_clicks=0,
                                                                                               style={'height': '40px',
                                                                                                      'width': '80px',
                                                                                                      'fontSize': '1.2rem'})],
                                                                                  className='buttons'),
                                                                         html.Div(id='leftSideDropdownHidden',
                                                                                  children=[],
                                                                                  style={'display': 'None'}),
                                                                         html.Div(id='leftSideDropdown', children=[]),
                                                                         html.Div(
                                                                             [

                                                                                 dbc.Modal(
                                                                                     [
                                                                                         dbc.ModalHeader("INFORMATION"),
                                                                                         dbc.ModalBody(
                                                                                             "Vous pouvez choisir maximum 20 valeur"),
                                                                                         dbc.ModalFooter(
                                                                                             dbc.Button("Close",
                                                                                                        id="close",
                                                                                                        className="ml-auto")
                                                                                         ),
                                                                                     ],
                                                                                     id="modal",
                                                                                 ),
                                                                             ])
                                                                     ])], ),
                                         html.Div(className="userControlDownRightSide",
                                                  children=[
                                                      html.Div(
                                                          className='div-for-dropdown',
                                                          children=[
                                                              html.Div(
                                                                  dcc.Dropdown(id='dropdownRight',
                                                                               options=[{'label': i, 'value': i} for i
                                                                                        in extra_data_list],
                                                                               multi=False,
                                                                               value='',
                                                                               style={"cursor": "pointer"},
                                                                               className='stockSelectorClass',
                                                                               clearable=False,
                                                                               placeholder='Select your parameters...',
                                                                               ),
                                                              ),
                                                              html.Div([html.Button('Show', id='showRight', n_clicks=0,
                                                                                    style={'height': '40px',
                                                                                           'width': '80px',
                                                                                           'fontSize': '1.2rem'}),
                                                                        html.Button('Delete', id='clearRight',
                                                                                    n_clicks=0, style={'height': '40px',
                                                                                                       'width': '80px',
                                                                                                       'fontSize': '1.2rem'})],
                                                                       className='buttons'),
                                                              html.Div(id='rightSideDropdownHidden', children=[],
                                                                       style={'visibility': 'hidden'}),
                                                              html.Div(id="rightSideDropdown", children=[])
                                                          ],
                                                      ),
                                                  ]),
                                         ])
        return (ocploadlist, visibilty)

    else:
        return (ocploadlist, {'visibility': 'hidden'})


@app.callback(Output("dropdownLeft", "options"),
              [Input("retrieve", "children")])
def dropdownlistcontrol(retrieve):
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        dff = [{'label': i, 'value': i} for i in df.columns]
        print('dff', dff)
        return dff
    else:
        return no_update


@app.callback(
    [Output("leftSideDropdownHidden", "children"), Output("leftSidedroptValue", "children")],
    [Input("dropdownLeft", "value")],
    [State("leftSideDropdownHidden", "children")]
)
def hiddendiv(val_dropdownLeft, children):
    if val_dropdownLeft == None or val_dropdownLeft == '':
        raise PreventUpdate
    print("childrenhidden", children)
    a = []
    a.append(val_dropdownLeft)
    for i in a:
        if i not in children:
            children.append(val_dropdownLeft)
            print('simdi oluyor', val_dropdownLeft)
    return children, children


@app.callback(

    Output("leftSideDropdown", "children"),
    [Input("showLeft", "n_clicks"),
     Input("clearLeft", "n_clicks"), ],
    [State("leftSideDropdownHidden", "children")],

)
# left side dropdown-checklist relation
#########

def displayLeftDropdown(n_clicks1, n_clicks2, valeur):
    # q1 = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    new_checklist = []
    if len(valeur) == 0:
        raise PreventUpdate
    print('valeeuuuuuuuuuuuurrrrrrrrrrrrrrr', valeur)
    # val = list(filter(lambda x: val.count(x)==1, val))
    if n_clicks1 > 0:
        a = []
        a.append(valeur)
        print('aaaaaaaaa', a)
        print('valeur', valeur)
        new_checklist += html.Div([dbc.Checklist(
            id='choosenChecklistLeft',
            options=[{'label': i, 'value': i} for i in valeur if i in a[0]],
            value=[],
            labelStyle={"display": "Block"},
        ), ], style={"marginTop": "10px"})
    if n_clicks2 > 0:
        print("silmeden once", valeur)
        for i in range(n_clicks2):
            if valeur != []:
                valeur.pop(-1)

    new_checklist = html.Div([dbc.Checklist(
        id='choosenChecklistLeft',
        options=[{'label': i, 'value': i} for i in valeur],
        value=[],
        labelClassName='value_design', labelCheckedStyle={"color": "red"},

    ), ], style={"marginLeft": "30px"})
    print("soncheklist", new_checklist)
    return new_checklist


@app.callback(
    Output("modal", "is_open"),
    [Input("showLeft", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open"),
     State("leftSideDropdownHidden", "children")],
)
def toggle_modal(n1, n2, is_open, children):
    if len(children) > 20:
        return not is_open
    return is_open


#### rightside dropdown-checklist relation


@app.callback(

    Output('rightSideDropdown', "children"),
    [
        Input("showRight", "n_clicks"),
        Input("clearRight", "n_clicks")
    ],
    [
        State("dropdownRight", "value"),
        State('rightSideDropdown', "children"),
    ]
)
def edit_list2(ncr1, ncr2, valeur, children):
    triggered_buttons = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if triggered_buttons == "showRight":
        def mesure1(textRight):
            if textRight == "Mass de Bois":
                return "g"
            elif textRight == 'Volume gaz':
                return 'm3'

            elif textRight == 'Vitesse de rotation':
                return 'tour/mn'

            elif textRight in {'Puissance Thermique', 'Puissance Electrique'}:
                return "W"

            elif textRight in {'CO', 'CO2', 'NO', 'NOX', 'CX'}:
                return "% MOL"


            elif textRight == 'Temperature de Fumée':
                return '°K'

        new_listRight = html.Div([html.Div([
            html.Div([dcc.Markdown('''*{}'''.format(valeur), id="checklistValeur",
                                   style={'height': '1rem', 'fontFamily': 'arial', 'color': 'black',
                                          'fontSize': '1.2rem'}),
                      html.Div(dbc.Input(id='inputRight',
                                         type="text",
                                         min=-10000, max=10000, step=1, bs_size="sm", style={'width': '6rem'},
                                         autoFocus=True, ), id="styled-numeric-input", ),
                      html.P(mesure1(valeur),
                             style={'margin': '0.1rem 0', 'color': 'black', 'height': '2rem', 'fontFamily': 'arial',
                                    'fontSize': '1.2rem', }),
                      dbc.Button("Ok", id="valueSendRight", outline=True, color="primary", className="mr-1"),

                      ], className='design_children2'),
        ], className='design_children', ), html.Hr()])

        children.append(new_listRight)

    if triggered_buttons == "clearRight":
        if len(children) == 0:
            raise PreventUpdate
        else:
            children.pop()

    return children


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')],

              )
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(id='tab1Data')
        ])
    if tab == 'tab-4':
        return html.Div([
            html.Div(id='tab2Data')
        ])
    if tab == 'tab-3':
        return html.Div([
            html.P('zehra')
        ])
    else:
        pass


@app.callback(Output('tab1Data', 'children'),
              [Input("my-toggle-switch", "on"),
               Input("leftSidedroptValue", "children")]
              )
def LoadingDataTab1(on, dropdownhidden):
    if on == 1:
        loadTab1 = html.Div([html.Div([html.Div([html.Div([dcc.Dropdown(id='firstChoosenValue',
                                                                        options=[{'label': i, 'value': i} for i in
                                                                                 dropdownhidden],
                                                                        multi=False,
                                                                        style={"cursor": "pointer", 'width': '180px'},
                                                                        className='',
                                                                        clearable=True,
                                                                        placeholder='First Value...',
                                                                        ),
                                                           dbc.Input(id='leftIntegralFirst',
                                                                     type="text",
                                                                     debounce=True,
                                                                     min=-10000, max=10000, step=1,
                                                                     bs_size="sm",
                                                                     style={'width': '7rem', "marginTop": "1.5rem"},
                                                                     autoFocus=True,
                                                                     placeholder="first point"),
                                                           dbc.Input(id='leftIntegralSecond',
                                                                     type="text",
                                                                     debounce=True,
                                                                     min=-10000, max=10000, step=1,
                                                                     bs_size="sm",
                                                                     style={'width': '7rem', "marginTop": "1.5rem"},
                                                                     autoFocus=True,
                                                                     placeholder="second point"),
                                                           dbc.Input(id='leftIntegral',
                                                                     type="text",
                                                                     min=-10000, max=10000, step=1,
                                                                     bs_size="sm",
                                                                     style={'width': '8rem', "marginTop": "1.5rem"},
                                                                     autoFocus=True,
                                                                     placeholder="total integration"),
                                                           ]), html.Button("Write", id="write_excel", n_clicks=0,
                                                                           style={'fontSize': '1rem'},
                                                                           className="ad")]),
                                       html.Div([dbc.Checklist(
                                           id='operateur',
                                           options=[{'label': i, 'value': i} for i in
                                                    ['Plus', 'Moins', 'Multiplie', 'Division']],
                                           value=[],
                                           labelStyle={"display": "Block"},
                                       ), ]),
                                       html.Div([dcc.Dropdown(id='secondChoosenValue',
                                                              options=[{'label': i, 'value': i} for i in
                                                                       dropdownhidden],
                                                              multi=False,
                                                              style={"cursor": "pointer", 'width': '180px'},
                                                              className='',
                                                              clearable=True,
                                                              placeholder='Second Value...',
                                                              ),
                                                 dbc.Input(id='rightIntegralFirst',
                                                           type="text",
                                                           min=-10000, max=10000, step=1,
                                                           bs_size="sm",
                                                           style={'width': '7rem', "marginTop": "1.5rem"},
                                                           autoFocus=True,
                                                           placeholder="first point"),
                                                 dbc.Input(id='rightIntegralSecond',
                                                           type="text",
                                                           min=-10000, max=10000, step=1,
                                                           bs_size="sm",
                                                           style={'width': '7rem', "marginTop": "1.5rem"},
                                                           autoFocus=True,
                                                           placeholder="second point"),
                                                 dbc.Input(id='rightIntegral',
                                                           type="text",
                                                           min=-10000, max=10000, step=1,
                                                           bs_size="sm",
                                                           style={'width': '8rem', "marginTop": "1.5rem"},
                                                           autoFocus=True,
                                                           placeholder="total integration")]),
                                       html.Div([dbc.Input(id='operation',
                                                           type="text",
                                                           min=-10000, max=10000, step=1,
                                                           bs_size="sm",
                                                           style={'width': '10rem', "marginTop": "2rem",
                                                                  'height': '5rem', 'textAlign': 'center'},
                                                           autoFocus=True,
                                                           placeholder="result"),
                                                 dbc.Input(id='intersection',
                                                           type="text",
                                                           min=-10000, max=10000, step=1,
                                                           bs_size="sm",
                                                           style={'width': '10rem', "marginTop": "2rem",
                                                                  'height': '2rem', 'textAlign': 'center'},
                                                           autoFocus=True,
                                                           placeholder="Intersection")], className='aa')],
                                      className="ab"),
                             html.Div([dcc.RadioItems(id="radiograph",
                                                      options=[
                                                          {'label': 'Point', 'value': 'markers'},
                                                          {'label': 'Line', 'value': 'lines'},
                                                          {'label': 'Line + Point', 'value': 'lines+markers'},

                                                      ],
                                                      value='markers',
                                                      labelClassName='groupgraph',
                                                      labelStyle={'margin': '10px', },
                                                      inputStyle={'margin': '10px', }
                                                      ),
                                       dbc.Input(id='minimumValueGraph',
                                                 type="text",
                                                 min=-10000, max=10000, step=1,
                                                 bs_size="sm",
                                                 style={'width': '7rem', "marginTop": "1rem"},
                                                 autoFocus=True,
                                                 placeholder="Enter Minimum Value of Graph..."),
                                       ], className='abcd'),

                             html.Div([dcc.Graph(id='graph',
                                                 config={'displayModeBar': True,
                                                         'scrollZoom': True,
                                                         'modeBarButtonsToAdd': [
                                                             'drawline',
                                                             'drawrect',
                                                             'drawopenpath',
                                                             'select2d',
                                                             'eraseshape',
                                                         ]},
                                                 style={'marginTop': 20},
                                                 figure={
                                                     'layout': {'legend': {'tracegroupgap': 0},

                                                                }
                                                 }

                                                 ),
                                       dcc.Slider(id="sliderHeightTab1",
                                                  max=2100,
                                                  min=400,
                                                  value=530,
                                                  step=100,
                                                  vertical=True,
                                                  updatemode='drag')], className='abc'),

                             html.Div([dcc.Slider(id="sliderWidthTab1",
                                                  max=2000,
                                                  min=600,
                                                  value=1000,
                                                  step=100,
                                                  updatemode='drag'),
                                       html.Div(id='output-data-upload', children=[])]),

                             ])

        return loadTab1


# bunu bi duzeltmeye calisacam
@app.callback(Output("leftSideChecklistValueHidden", "children"),
              [Input('choosenChecklistLeft', 'value')],
              [State("leftSideChecklistValueHidden", "children")]
              )
def res(val, hiddenval):
    if val == None:
        raise PreventUpdate
    hiddenval = val
    print('valllllllllll', val)
    print('hiddenval', hiddenval)
    return hiddenval


@app.callback(Output("radiographhidden", "children"),
              [Input("radiograph", "value")],

              )
def radio(radiograph):
    return radiograph


@app.callback(Output("sliderHeightTab1hidden", "children"),
              [Input("sliderHeightTab1", "value")],
              )
def tabheight(height):
    return height


@app.callback(Output("sliderWidthTab1hidden", "children"),
              [Input("sliderWidthTab1", "value")],

              )
def tabwidth(width):
    return width


@app.callback(Output("minimumValueGraphhidden", "children"),
              [Input("minimumValueGraph", "value")],
              )
def min(minval):
    return minval


@app.callback(Output("firstchoosenvalhidden", "children"),
              [Input("firstChoosenValue", "value")],
              [State("firstchoosenvalhidden", "children")]
              )
def firstchleft(firstchoosen, hiddenfirstchoosen):
    hiddenfirstchoosen.append(firstchoosen)
    return hiddenfirstchoosen


@app.callback(Output("secondchoosenvalhidden", "children"),
              [Input("secondChoosenValue", "value")],
              )
def secondchleft(secondchoosen):
    print("secondchoosen", secondchoosen)
    return secondchoosen


@app.callback(Output("leftintegralfirsthidden", "children"),
              [Input("leftIntegralFirst", "value")],
              )
def firstchright(leftintfirst):
    return leftintfirst


@app.callback(Output("leftintegralsecondhidden", "children"),
              [Input("leftIntegralSecond", "value")],
              )
def secondchright(leftintsecond):
    return leftintsecond


@app.callback(Output("rightintegralfirsthidden", "children"),
              [Input("rightIntegralFirst", "value")],
              )
def rightfrst(rightintfirst):
    return rightintfirst


@app.callback(Output("rightintegralsecondhidden", "children"),
              [Input("rightIntegralSecond", "value")],
              )
def rightscnd(rightintsecond):
    return rightintsecond


# for show graph and changement

@app.callback([Output('graph', 'figure'),
               Output('hiddenDifferance', 'children'), ],
              [Input("leftSideChecklistValueHidden", "children"),
               Input("radiographhidden", "children"),
               Input('pointLeftFirst', 'children'),
               Input('pointRightFirst', 'children'),
               Input("sliderHeightTab1hidden", "children"),
               Input("sliderWidthTab1hidden", "children"),
               Input('minimumValueGraphhidden', 'children'),
               Input('firstchoosenvalhidden', 'children'),
               Input('secondchoosenvalhidden', 'children'),
               Input('leftintegralfirsthidden', 'children'),
               Input('leftintegralsecondhidden', 'children'),
               Input('rightintegralfirsthidden', 'children'),
               Input('rightintegralsecondhidden', 'children'),
               ],
              [State('hiddenDifferance', 'children'),
               State('retrieve', 'children')]
              )
def res2(val, radiograph, firstshape, secondshape, sliderheight, sliderwidth,
         minVal, firstchoosen, secondchoosen, leftfirstval, leftsecondval,
         rightfirstval, rightsecondval, differance, retrieve):
    if retrieve == None or retrieve == []:
        raise PreventUpdate
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        df['index'] = df.index
        df = df.reindex(columns=sorted(df.columns, reverse=True))
        if 'date' not in df.columns:
            baseval = ''
            for col in df.columns:
                if 'Temps' in col:
                    baseval += col
                    dt = df[baseval]
        else:
            df_shape = pd.read_excel('{}'.format(retrieve[0]))
            df_shape['newindex'] = df_shape.index
            df_shape.index = df_shape['date']
            dt = ["{}-{:02.0f}-{:02.0f} {:02.0f}:{:02.0f}:{:02.0f}".format(d.year, d.month, d.day, d.hour, d.minute,
                                                                           d.second) for d in df_shape.index]
        fig = go.Figure()
        for i_val in range(len(val)):

            y_axis = df[val[i_val]]
            if 'date' not in df.columns:
                x_axis = df[baseval]
            else:
                x_axis = df['date']
            fig.add_trace(go.Scattergl(x=x_axis, y=y_axis, mode=radiograph, name=val[i_val]))
            color = {0: 'blue', 1: 'red', 2: 'green', 3: 'purple', 4: 'orange'}
            if len(firstshape) == 2 and leftfirstval != firstshape[0] and leftfirstval != None:
                print('leffirstval', leftfirstval)
                print(type(leftfirstval))
                if leftfirstval.startswith('T') == 1:
                    del firstshape[0]
                    firstshape.append(float(leftfirstval[2:]))
                    firstshape = sorted(firstshape)
                elif leftfirstval.isnumeric() == 1:
                    del firstshape[0]
                    firstshape.append(float(leftfirstval))
                    firstshape = sorted(firstshape)
                elif leftfirstval != None:
                    del firstshape[0]
            if len(firstshape) == 2 and leftsecondval != firstshape[1] and leftsecondval != None:
                if leftsecondval.startswith('T') == 1:
                    del firstshape[1]
                    firstshape.append(float(leftsecondval[2:]))
                    firstshape = sorted(firstshape)
                elif leftsecondval.isnumeric() == 1:
                    del firstshape[1]
                    firstshape.append(float(leftsecondval))
                    firstshape = sorted(firstshape)
                elif leftsecondval != None:
                    del firstshape[1]

            if len(secondshape) == 2 and rightfirstval != secondshape[0] and rightfirstval != None:
                if rightfirstval.startswith('T') == 1:
                    del secondshape[0]
                    secondshape.append(float(rightfirstval[2:]))
                    secondshape = sorted(secondshape)
                elif rightfirstval.isnumeric() == 1:
                    del secondshape[0]
                    secondshape.append(float(rightfirstval))
                    secondshape = sorted(secondshape)
                elif rightfirstval != None:
                    del secondshape[0]
            if len(secondshape) == 2 and rightsecondval != secondshape[1] and rightsecondval != None:
                if rightsecondval.startswith('T') == 1:
                    del secondshape[1]
                    secondshape.append(float(rightsecondval[2:]))
                    secondshape = sorted(secondshape)
                elif rightsecondval.isnumeric() == 1:
                    del secondshape[1]
                    secondshape.append(float(rightsecondval))
                    secondshape = sorted(secondshape)
                elif rightsecondval != None:
                    del secondshape[1]
            if len(secondshape) == 2 and secondchoosen == None:
                del secondshape[1]
            if len(firstshape) == 2 and firstchoosen == None:
                del firstshape[1]

            # else : return(no_update)
            def controlShape():
                pathline = ''
                pathline2 = ''
                if firstchoosen != [None, None] and secondchoosen != None:
                    if len(firstshape) == 2 and leftfirstval != None and leftsecondval != None and len(
                            secondshape) == 2 and rightsecondval != None and rightfirstval != None:
                        if int(firstshape[1]) > int(firstshape[0]) and int(secondshape[1]) > int(secondshape[0]):
                            rangeshape = range(int(firstshape[0]), int(firstshape[1]))
                            for k in rangeshape:
                                if k == rangeshape[0]:
                                    pathline = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(
                                        df[firstchoosen[-1]][k]) + ' '

                                elif k != rangeshape[0] and k != rangeshape[-1]:
                                    pathline += ' L' + str(int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k])

                            pathline += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline += ' Z'
                            rangeshape2 = range(int(secondshape[0]), int(secondshape[1]))

                            for k in rangeshape2:
                                if k == rangeshape2[0]:
                                    pathline2 = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(
                                        df[secondchoosen][k]) + ' '

                                elif k != rangeshape2[0] and k != rangeshape2[-1]:
                                    pathline2 += ' L' + str(int(dt[k])) + ', ' + str(df[secondchoosen][k])

                            pathline2 += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline2 += ' Z'

                    return [dict(
                        type="path",
                        path=pathline,
                        layer='below',
                        fillcolor="PaleTurquoise",
                        line_color="LightSeaGreen",
                    ), dict(
                        type="path",
                        path=pathline2,
                        layer='below',
                        fillcolor="red",
                        opacity=0.5,
                        line_color="red",
                    )]

                if firstchoosen[-1] != None and secondchoosen == None:
                    if len(firstshape) == 2 and leftfirstval != None and leftsecondval != None:
                        if int(firstshape[1]) > int(firstshape[0]):
                            pathline = ''
                            rangeshape = range(int(firstshape[0]), int(firstshape[1]))
                            for k in rangeshape:
                                if k == rangeshape[0]:
                                    pathline = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k]) + ' '

                                elif k != rangeshape[0] and k != rangeshape[-1]:
                                    pathline += ' L' + str(int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k])

                            pathline += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline += ' Z'

                            return [dict(
                                type="path",
                                path=pathline,
                                layer='below',
                                fillcolor="PaleTurquoise",
                                line_color="LightSeaGreen",
                            )]

                        if int(firstshape[0]) > int(firstshape[1]):
                            rangeshape = range(int(firstshape[1]), int(firstshape[0]))
                            pathline = ''
                            for k in rangeshape:
                                if k == rangeshape[0]:
                                    pathline = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k]) + ' '

                                elif k != rangeshape[0] and k != rangeshape[-1]:
                                    pathline += ' L' + str(int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k])

                            pathline += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline += ' Z'

                            return [dict(
                                type="path",
                                path=pathline,
                                layer='below',
                                fillcolor="PaleTurquoise",
                                line_color="LightSeaGreen",
                            )]

                if secondchoosen != None and firstchoosen[-1] == None:
                    if len(secondshape) == 2 and rightsecondval != None and rightfirstval != None:
                        if int(secondshape[1]) > int(secondshape[0]):

                            rangeshape = range(int(secondshape[0]), int(secondshape[1]))
                            for k in rangeshape:
                                if k == rangeshape[0]:
                                    pathline2 = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(
                                        df[secondchoosen][k]) + ' '

                                elif k != rangeshape[0] and k != rangeshape[-1]:
                                    pathline2 += ' L' + str(int(dt[k])) + ', ' + str(df[secondchoosen][k])

                            pathline2 += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline2 += ' Z'

                            return [dict(
                                type="path",
                                path=pathline2,
                                layer='below',
                                fillcolor="red",
                                opacity=0.5,
                                line_color="LightSeaGreen",
                            )]

                        if int(secondshape[0]) > int(secondshape[1]):
                            rangeshape = range(int(secondshape[1]), int(secondshape[0]))
                            for k in rangeshape:
                                if k == rangeshape[0]:
                                    pathline2 = 'M ' + str(int(dt[k])) + ', ' + str(0) + ' L' + str(
                                        int(dt[k])) + ', ' + str(
                                        df[secondchoosen][k]) + ' '

                                elif k != rangeshape[0] and k != rangeshape[-1]:
                                    pathline2 += ' L' + str(int(dt[k])) + ', ' + str(df[secondchoosen][k])

                            pathline2 += ' L' + str(int(dt[k])) + ', ' + str(0)
                            pathline2 += ' Z'

                            return [dict(
                                type="path",
                                path=pathline2,
                                layer='below',
                                fillcolor="red",
                                opacity=0.5,
                                line_color="LightSeaGreen",
                            )]

            a = controlShape()
            # b = controlShapeSecond()
            # print('aaaaaaaa',a)
            # print('bbbbbbbbbbbbb',b)

            # if a != None and b != None:
            #     g.append(a)
            #     g.append(b)
            # if a == None and b != None:

            # if a != None and b == None:
            #     g.append(a)

            fig.update_layout(
                autosize=False,
                width=sliderwidth,
                height=sliderheight,
                shapes=a,
                margin=dict(
                    l=50,
                    r=50,
                    b=100,
                    t=50,
                    pad=4
                ),
                paper_bgcolor="LightSteelBlue",
            )

            if len(firstshape) == 2 and len(secondshape) == 2:
                a = int(firstshape[0])
                c = int(secondshape[0])
                b = int(firstshape[1])
                d = int(secondshape[1])
                print('aaaa', a)
                print('aaaa', b)
                print('aaaa', c)
                print('aaaa', d)
                if len(set(range(a, b)).intersection(set(range(c, d)))) >= 1 or len(
                        set(range(c, d)).intersection(set(range(a, b)))) >= 1:
                    if a <= c:
                        if len(differance) == 2:
                            differance.pop(0)
                            differance.append(b)
                        differance.append(b)
                    if a >= c:
                        if len(differance) == 2:
                            differance.pop(0)
                            differance.append(a)
                        differance.append(a)
                    if b <= d:
                        if len(differance) == 2:
                            differance.pop(0)
                            differance.append(c)
                        differance.append(c)
                    if b >= d:
                        if len(differance) == 2:
                            differance.pop(0)
                            differance.append(d)
                        differance.append(d)
                    if set(range(a, b)).issuperset(set(range(c, d))) == 1:
                        differance.append(c)
                        differance.append(d)
                    if set(range(c, d)).issuperset(set(range(a, b))) == 1:
                        differance.append(a)
                        differance.append(b)

                else:
                    differance = [0, 0]

            print('diffff', differance[-2:])

        return fig, differance[-2:]

    else:
        return (no_update, no_update)


@app.callback(Output('tab2Data', 'children'),
              [Input("my-toggle-switch", "on")])
def LoadingDataTab2(on):
    if on == 1:
        data_list = ['CoAd', 'ComManCoP2', 'ComManCoP3P4P5', 'ComManPompeSec', 'CompteurEnergie', 'CoP2',
                     'CtempDepChauff',
                     'D1', 'D2', 'D3', 'D4', 'MarcheBruleur', 'Teg', 'SdeBasBouMelange', 'SdeBasHauMelange', 'TambN3',
                     'Tb1',
                     'Tb2', 'Tb3', 'Tb4', 'TdepPLC', 'Teb', 'Tec', 'Teev', 'TempminMaf', 'Text', 'Tsb', 'Tsc', 'Tsev']

        loadlist = html.Div(children=[
            html.Div([html.Div([html.Div([dcc.Dropdown(id='tabDropdownTop',
                                                       options=[{'label': i, 'value': i} for i in data_list],
                                                       multi=True,
                                                       style={"cursor": "pointer"},
                                                       className='stockSelectorClass2',
                                                       clearable=True,
                                                       placeholder='Select your y-axis value...',
                                                       ),
                                          dcc.Dropdown(id='tabDropdownDown',
                                                       options=[{'label': i, 'value': i} for i in data_list],
                                                       multi=True,
                                                       style={"cursor": "pointer"},
                                                       className='stockSelectorClass2',
                                                       clearable=True,
                                                       placeholder='Select your x-axis value...',
                                                       ), ], className="ab"),
                                html.Div(dcc.RadioItems(id="radiograph2",
                                                        options=[
                                                            {'label': 'Point', 'value': 'markers'},
                                                            {'label': 'Line', 'value': 'lines'},
                                                            {'label': 'Line + Point', 'value': 'lines+markers'}],
                                                        value='markers',
                                                        labelClassName='groupgraph',
                                                        labelStyle={'margin': '10px', },
                                                        inputStyle={'margin': '10px', }
                                                        ), ), ], className="ac"),
                      html.Div([dcc.Dropdown(id="dropadd",
                                             options=[
                                                 {'label': 'Note', 'value': 'note'},
                                                 {'label': 'Header', 'value': 'header'},
                                                 {'label': 'x-axis', 'value': 'x_axis'},
                                                 {'label': 'y-axis', 'value': 'y_axis'},

                                             ],
                                             value='header',
                                             ),
                                dcc.Textarea(
                                    id='textarea',
                                    value='',
                                    style={'width': '15rem', 'marginTop': '0.5rem'},
                                    autoFocus='Saisir',
                                ),
                                ], className="aa"),

                      html.Button('addText', id='addText', n_clicks=0, style={'marginTop': '1.5rem'}),

                      ], className="tabDesign", ),

            html.Div([dcc.Graph(id='graph2', config={'displayModeBar': True,
                                                     'scrollZoom': True,
                                                     'modeBarButtonsToAdd': [
                                                         'drawopenpath',
                                                         'drawcircle',
                                                         'eraseshape',
                                                         'select2d',
                                                     ]},
                                figure={
                                    'layout': {'legend': {'tracegroupgap': 0},

                                               }
                                }
                                ),
                      dcc.Slider(id="sliderHeight",
                                 max=2100,
                                 min=400,
                                 value=500,
                                 step=100,
                                 vertical=True,
                                 updatemode='drag')], className='abc'),

            html.Div([dcc.Slider(id="sliderWidth",
                                 max=2000,
                                 min=600,
                                 value=950,
                                 step=100,
                                 updatemode='drag'),
                      html.Div(id="tab2DashTable", children=[])]),
        ])

        return loadlist


# @app2.callback(Output('graph2','figure'),
#               [Input("showTab", "n_clicks"),Input('textarea', 'value')],
#               State('tabDropdownTop', 'value'),
#               State('tabDropdownDown', 'value')
#               )
# def detailedGraph(n_clicks,x, val1, val2):
#     df = pd.read_excel("aa.xlsx")
@app.callback([Output('tab2hiddenValuex_axis', 'children'), Output('tab2hiddenValuey_axis', 'children')],
              [Input('tabDropdownTop', 'value'),
               Input('tabDropdownDown', 'value')],
              )
def contractdropdown(x, y, ):
    if x == [] or y == []:
        raise PreventUpdate

    return x, y


@app.callback([Output("tabDropdownTop", "options"), Output("tabDropdownDown", "options")],
              [Input("retrieve", "children")])
def dropdownlistcontrol(retrieve):
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        dff = [{'label': i, 'value': i} for i in df.columns]
        return (dff, dff)
    else:
        return (no_update, no_update)


@app.callback([Output('hiddenTextxaxis', 'children'), Output('hiddenTextyaxis', 'children'),
               Output('hiddenTextHeader', 'children'), Output('hiddenTextNote', 'children')],
              [Input('addText', 'n_clicks')],
              [State('textarea', 'value'), State('dropadd', 'value'),
               State('hiddenTextxaxis', 'children'), State('hiddenTextyaxis', 'children'),
               State('hiddenTextHeader', 'children'), State('hiddenTextNote', 'children')]

              )
def detailedGraph(addtextclick, textarea, add, g1, g2, head, note):
    if add == None or g1 == None or g2 == None or head == None or note == None:
        raise PreventUpdate

    if addtextclick > 0:
        if add == 'x_axis':
            g1.append(textarea)

        if add == 'y_axis':
            g2.append(textarea)

        if add == 'header':
            head.append(textarea)

        if add == 'note':
            note.append(textarea)
        textarea = ''
        return g1, g2, head, note
    else:
        return (no_update, no_update, no_update, no_update)


@app.callback(Output('graph2', 'figure'),
              [Input('radiograph2', 'value'),
               Input('tab2hiddenValuex_axis', 'children'), Input('tab2hiddenValuey_axis', 'children'),
               Input('sliderHeight', 'value'), Input('sliderWidth', 'value'),
               Input('hiddenTextxaxis', 'children'), Input('hiddenTextyaxis', 'children'),
               Input('hiddenTextHeader', 'children'), Input('hiddenTextNote', 'children')],
              [State('retrieve', 'children')]
              )
def detailedGraph2(radio, valx, valy, slideheight, slidewidth, g1, g2, head, note, retrieve):
    if valx == [] or valy == [] or valx == None or valy == None or g1 == None or g2 == None or head == None or note == None:
        raise PreventUpdate
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        fig = go.Figure()

        for j in range(len(valy)):
            for k in range(len(valx)):
                a = df[valy[j]]
                b = df[valx[k]]
                fig.add_trace(go.Scatter(x=a, y=b, mode=radio, name="{}/{}".format(valy[j], valx[k])))

                fig.update_xaxes(
                    tickangle=90,
                    title_text='' if g1 == [] else g1[-1],
                    title_font={"size": 20},
                    title_standoff=25),

                fig.update_yaxes(
                    title_text='' if g2 == [] else g2[-1],
                    title_standoff=25),
                fig.update_layout(
                    title_text=head[-1] if len(head) > 0 else "{}/{}".format(valy[j], valx[k]),
                    autosize=False,
                    width=slidewidth,
                    height=slideheight,
                    margin=dict(
                        l=50,
                        r=50,
                        b=50,
                        t=50,
                        pad=4
                    ),
                    uirevision=valy[j], ),
                fig.add_annotation(text=note[-1] if len(note) > 0 else '',
                                   xref="paper", yref="paper",
                                   x=0, y=0.7, showarrow=False)

        return fig


@app.callback(
    [Output('pointLeftFirst', 'children'),
     Output('pointLeftSecond', 'children')],
    [Input('graph', 'clickData'),
     Input('firstChoosenValue', 'value'), ],
    [State('leftSideChecklistValueHidden', 'children'),
     State('pointLeftFirst', 'children'),
     State('pointLeftSecond', 'children'),
     State('retrieve', 'children')]
)
def valint(clickData, firstchoosen, value, leftchild, rightchild, retrieve):
    if value is [] or value is None or clickData == None or clickData == [] or firstchoosen == None or retrieve == None or retrieve == []:
        raise PreventUpdate
    print('firstchoosen', firstchoosen)
    spaceList1 = []
    zero = 0
    spaceList2 = []
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        df['index'] = df.index
        for i in range(len(value)):
            spaceList1.append(zero)
            zero += 1
            spaceList2.append(value[i])
        zippedval = [i for i in list(zip(spaceList1, spaceList2))]
        curvenumber = clickData['points'][0]['curveNumber']
        for k in zippedval:
            if k[1] == firstchoosen:
                if k[0] == curvenumber:
                    x_val = clickData['points'][0]['x']
                    if 'date' in df.columns:
                        dff = df[df['date'] == x_val]
                    else:
                        a = ''
                        for v in df.columns:
                            if 'Temps' in v:
                                a += v
                                dff = df[df[v] == x_val]

                    a = []
                    a.append(dff[firstchoosen].index)
                    for i in range(len(a)):
                        for j in a:
                            print('leftchild1', leftchild)
                            leftchild.append(j[i])
                            print('leftchild2', leftchild)
                    if len(leftchild) > 2:
                        leftchild.pop(0)
                        print('leftchild3', leftchild)
                    return (leftchild, leftchild)
                else:
                    return (no_update, no_update)
            else:
                return (no_update, no_update)
    else:
        return (no_update, no_update)


@app.callback([Output('leftIntegralFirst', 'value'), Output('leftIntegralSecond', 'value')],
              [Input('pointLeftFirst', 'children'), Input('pointLeftSecond', 'children')],
              [State('firstChoosenValue', 'value')], )
def display_hover_data(leftchild, rightchild, firstchoosen):
    if leftchild == None or rightchild == None or leftchild == [] or rightchild == [] or firstchoosen == None:
        raise PreventUpdate
    minchild = 0
    maxchild = 0
    if len(leftchild) == 2:
        for i in range(len(leftchild)):
            if leftchild[0] < leftchild[1]:
                minchild = leftchild[0]
                maxchild = leftchild[1]
            else:
                minchild = leftchild[1]
                maxchild = leftchild[0]
        print('minchild', minchild)
        print('maxchild', maxchild)
    else:
        minchild = leftchild[0]
        maxchild = leftchild[0]

    if firstchoosen != '' and len(leftchild) == 2:
        return ('T ' + str(minchild), 'T ' + str(maxchild))
    else:
        return (no_update, no_update)


@app.callback(
    [Output('pointRightFirst', 'children'),
     Output('pointRightSecond', 'children')],
    [Input('graph', 'clickData'),
     Input('secondChoosenValue', 'value')],
    [State('leftSideChecklistValueHidden', 'children'),
     State('pointRightFirst', 'children'),
     State('pointRightSecond', 'children'),
     State('retrieve', 'children')]
)
def valint2(clickData, secondchoosen, value, leftchild, rightchild, retrieve):
    if value is [] or value is None or clickData == None or clickData == [] or secondchoosen == None or retrieve == None or retrieve == []:
        raise PreventUpdate
    spaceList1 = []
    zero = 0
    spaceList2 = []
    if len(retrieve) > 0:
        df = pd.read_excel('{}'.format(retrieve[0]))
        df['index'] = df.index
        for i in range(len(value)):
            spaceList1.append(zero)
            zero += 1
            spaceList2.append(value[i])
        zippedval = [i for i in list(zip(spaceList1, spaceList2))]
        curvenumber = clickData['points'][0]['curveNumber']
        for k in zippedval:
            if k[1] == secondchoosen:
                if k[0] == curvenumber:
                    x_val = clickData['points'][0]['x']
                    if 'date' in df.columns:
                        dff = df[df['date'] == x_val]
                    else:
                        a = ''
                        for v in df.columns:
                            if 'Temps' in v:
                                a += v
                                dff = df[df[v] == x_val]
                    a = []
                    a.append(dff[secondchoosen].index)
                    for i in range(len(a)):
                        for j in a:
                            leftchild.append(j[i])
                    if len(leftchild) > 2:
                        leftchild.pop(0)
                    return (leftchild, leftchild)
                else:
                    return (no_update, no_update)
            else:
                return (no_update, no_update)
    else:
        return (no_update, no_update)


@app.callback(
    [Output('rightIntegralFirst', 'value'), Output('rightIntegralSecond', 'value')],
    [Input('pointRightFirst', 'children'), Input('pointRightSecond', 'children')],
    [State('secondChoosenValue', 'value')], )
def display_hover_data2(leftchild1, rightchild1, secondchoosen):
    if leftchild1 == None or rightchild1 == None or leftchild1 == [] or rightchild1 == [] or secondchoosen == None:
        raise PreventUpdate
    if len(leftchild1) == 2:
        for i in range(len(leftchild1)):
            if leftchild1[0] < leftchild1[1]:
                minchild = leftchild1[0]
                maxchild = leftchild1[1]
            else:
                minchild = leftchild1[1]
                maxchild = leftchild1[0]
    else:
        minchild = leftchild1[0]
        maxchild = leftchild1[0]
    print('secondminchild', minchild)
    print('secondmaxchild', maxchild)
    if secondchoosen != '' and len(leftchild1) == 2:
        return 'T ' + str(minchild), 'T ' + str(maxchild)
    else:
        return (no_update, no_update)


@app.callback(Output('leftIntegral', 'value'),
              [Input('leftIntegralFirst', 'value'),
               Input('leftIntegralSecond', 'value'),
               Input('firstChoosenValue', 'value'),
               ], [State('retrieve', 'children')]

              )
def integralCalculation(st1left, st1right, valuechoosenleft, retrieve):
    if st1left == None or st1right == None or valuechoosenleft == None or valuechoosenleft == [] or retrieve == None or retrieve == []:
        raise PreventUpdate
    if st1left.startswith('T') == 1 and st1right.startswith('T') == 1:
        st1left = st1left[2:]
        st1right = st1right[2:]
    elif st1left.startswith('T') == 1 and st1right.isnumeric() == 1:
        st1left = st1left[2:]
        st1right = st1right
    elif st1left.isnumeric() == 1 and st1right.isnumeric() == 1:
        st1left = st1left
        st1right = st1right
    elif st1left.isnumeric() == 1 and st1right.startswith('T') == 1:
        st1left = st1left
        st1right = st1right[2:]
    if len(retrieve) > 0:
        print('valuechoosenleft', valuechoosenleft)
        print('st1left', type(valuechoosenleft))
        print('st1right', st1right)
        if st1left != '' and st1right != '':
            df = pd.read_excel('{}'.format(retrieve[0]))
            df['index'] = df.index
            df = df.reindex(columns=sorted(df.columns, reverse=True))
            dff1 = df[(df[valuechoosenleft].index >= float(st1left)) & (df[valuechoosenleft].index <= float(st1right)) |
                      (df[valuechoosenleft].index >= float(st1right)) & (df[valuechoosenleft].index <= float(st1left))]
            c = dff1[valuechoosenleft]
            area1 = abs(trapz(c, dx=1))

            return area1
        elif (st1left == '' and st1right != '') or (st1left != '' and st1right == ''):
            return 'total integration'
        elif (st1left == '' and st1right == '') and valuechoosenleft != '':
            return 'total integration'
        elif st1left != '' and st1right != '' and valuechoosenleft == '':
            return 'total integration'
    # return no_update


@app.callback(Output('rightIntegral', 'value'),
              [Input('rightIntegralFirst', 'value'),
               Input('rightIntegralSecond', 'value'),
               Input('secondChoosenValue', 'value'),
               ], [State('retrieve', 'children')]
              )
def integralCalculation2(st2left, st2right, valuechoosenright, retrieve):
    print('retrieve', retrieve)
    if st2left == None or st2right == None or valuechoosenright == None or valuechoosenright == [] or retrieve == None or retrieve == []:
        raise PreventUpdate
    if st2left.startswith('T') == 1 and st2right.startswith('T') == 1:
        st2left = st2left[2:]
        st2right = st2right[2:]
    elif st2left.startswith('T') == 1 and st2right.isnumeric() == 1:
        st2left = st2left[2:]
        st2right = st2right
    elif st2left.isnumeric() == 1 and st2right.isnumeric() == 1:
        st2left = st2left
        st2right = st2right
    elif st2left.isnumeric() == 1 and st2right.startswith('T') == 1:
        st2left = st2left
        st2right = st2right[2:]
    if len(retrieve) > 0:
        if st2left != '' and st2right != '':
            df = pd.read_excel('{}'.format(retrieve[0]))
            df['index'] = df.index
            df = df.reindex(columns=sorted(df.columns, reverse=True))
            dff2 = df[
                (df[valuechoosenright].index >= float(st2left)) & (df[valuechoosenright].index <= float(st2right)) |
                (df[valuechoosenright].index >= float(st2right)) & (df[valuechoosenright].index <= float(st2left))]
            f = dff2[valuechoosenright]
            area2 = abs(trapz(f, dx=1))
            return area2
        elif (st2left == '' and st2right != '') or (st2left != '' and st2right == ''):
            return 'total integration'
        elif (st2left == '' and st2right == '') and valuechoosenright != '':
            return 'total integration'
        elif st2left != '' and st2right != '' and valuechoosenright == '':
            return 'total integration'


@app.callback(Output('operation', 'value'),
              [Input('leftIntegral', 'value'),
               Input('rightIntegral', 'value'),
               Input('operateur', 'value')],
              )
def differanceintegration(value1, value2, ops):
    if value1 == None or value2 == None:
        raise PreventUpdate
    if ops == ['Plus']:
        return float(value1 + value2)
    elif ops == ['Moins']:
        return float(value1 - value2)
    elif ops == ['Multiplie']:
        return float(value1 * value2)
    elif ops == ['Division']:
        return float(value1 / value2)
    elif ops == []:
        return []


@app.callback(Output('intersection', 'value'),
              [Input('hiddenDifferance', 'children'),
               Input('firstChoosenValue', 'value'),
               Input('secondChoosenValue', 'value'),
               Input('leftIntegralFirst', 'value'),
               Input('rightIntegralFirst', 'value'), ],
              [State('intersection', 'value'), State('retrieve', 'children'),

               ]
              )
def differanceCalculation(hiddendif, valuechoosenright, valuechoosenleft, leftfirst, rightfirst, diff, retrieve):
    if hiddendif == None or hiddendif == [] or retrieve == None or retrieve == []:
        raise PreventUpdate
    print('hiddendif', hiddendif)
    print("valuechoosenright", valuechoosenright)
    print("valuechoosenright", type(valuechoosenright))

    # (len(hiddendif)>=2 and len(valuechoosenright)==1) or (len(hiddendif)>=2 and len(valuechoosenleft)==1) or
    if (len(hiddendif) >= 2):
        for i in range(len(hiddendif)):
            if hiddendif[0] < hiddendif[1]:
                a = hiddendif[0]
                b = hiddendif[1]
            else:
                a = hiddendif[1]
                b = hiddendif[0]
        print('a', a)
        print('b', b)
        zz = []
        zz.append(a)
        zz.append(b)
        differance = []
        if len(
                retrieve) > 0 and valuechoosenright != None and valuechoosenleft != None and leftfirst != None and rightfirst != None:

            df = pd.read_excel('{}'.format(retrieve[0]))
            df['index'] = df.index
            df = df.reindex(columns=sorted(df.columns, reverse=True))
            dff = df[(df[valuechoosenright].index >= float(a)) & (df[valuechoosenright].index <= float(b)) |
                     (df[valuechoosenright].index >= float(b)) & (df[valuechoosenright].index <= float(a))]
            l = dff[valuechoosenright]

            dff2 = df[(df[valuechoosenleft].index >= float(a)) & (df[valuechoosenleft].index <= float(b)) |
                      (df[valuechoosenleft].index >= float(b)) & (df[valuechoosenleft].index <= float(a))]
            r = dff2[valuechoosenleft]
            tt = []
            yy = []
            for i in l:
                tt.append(i)
            for i in r:
                yy.append(i)
            for i in range(len(tt)):
                if tt[i] <= yy[i]:
                    differance.append(tt[i])
                if yy[i] < tt[i]:
                    differance.append(yy[i])
            print('differance', differance)
            diff = (abs(trapz(differance, dx=1)))
            return diff
        else:
            return ['intersection']


@app.callback(Output('writeexcelhidden', 'children'),
              [Input('write_excel', 'n_clicks')],
              [State('firstChoosenValue', 'value'),
               State('leftIntegralFirst', 'value'),
               State('leftIntegralSecond', 'value'),
               State('leftIntegral', 'value'),
               State('secondChoosenValue', 'value'),
               State('rightIntegralFirst', 'value'),
               State('rightIntegralSecond', 'value'),
               State('rightIntegral', 'value'),
               State('operation', 'value'),
               State('intersection', 'value'),
               ],
              )
def write_excel(nc, a, b, c, d, e, f, g, h, i, j):
    if nc > 0:
        from datetime import datetime

        # datetime object containing current date and time
        now = datetime.now()
        return (now, a, b, c, d, e, f, g, h, i, j)


# t = []
# @app.callback(Output('bbbb','children'),
#               [Input('writeexcelhidden','children')],
#
#               )
#
# def xxx(s):
#     print('s',s)
#     t.append(s)
#     now = time.strftime("%x")
#     book = Workbook()
#     sheet = book.active
#     for row in t[2:]:
#         sheet.append(row)
#     book.save('appending.xlsx')


# @app.callback(Output,
#               [Input('writeexcelhidden', 'children')],
#               [State('bbbb', 'children')])
#
# def nihai(a,b):
#     if a !=[]:
#         b.append(a[0])
#     print(b)


if __name__ == '__main__':
    app.run_server(debug=True)
