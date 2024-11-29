import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                         ],
                                    value="ALL",
                                    placeholder="Select launch site",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min=min_payload, max=max_payload, step=1000,
                                        marks={int(i): f'{int(i)}' for i in range(int(min_payload), int(max_payload) + 1000, 1000)},
                                        value=[min_payload, max_payload]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                            ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        data = spacex_df
        
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')

    else:
        data = spacex_df[spacex_df["Launch Site"] == entered_site]
    
        outcome_counts = data['class'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count']

        fig = px.pie(
            outcome_counts, 
            values='Count', 
            names='Outcome', 
            title=f'Landing Outcomes for {"All Sites" if entered_site == "ALL" else entered_site}'
        )
    
    return fig

 

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    
    if entered_site == 'ALL':
        data_s = spacex_df
    else:
        data_s = spacex_df[spacex_df["Launch Site"] == entered_site]

    payload_min, payload_max = payload_range

    data = data_s[
        (data_s['Payload Mass (kg)'] >= payload_min) &
        (data_s['Payload Mass (kg)'] <= payload_max)
    ]
    
    fig = px.scatter(
        data,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category",
        title='Landing Outcomes Payload and Booster')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
