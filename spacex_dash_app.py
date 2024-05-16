# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
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
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                          options=[{'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder='Select a Launch Site here',
                                            searchable=True
                                            ),
                                        ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=1000,
                                            marks= {0: '0 kg', 10000: '10,000 kg'},
                                            value=[0, 10000]
                                        )
                                    ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[['Launch Site','class']]
    if entered_site == 'ALL':
        filtered_df = filtered_df
        successes=filtered_df.groupby(['Launch Site']).sum().reset_index() # sums up all successful launches '1's grouped by LaunchSite
        #print(successes)
        fig = px.pie(successes, values='class', names='Launch Site', title='Number of successful launches by site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        successes=filtered_df.groupby(['Launch Site']).sum().reset_index()
        counts=filtered_df.groupby(['Launch Site']).count().reset_index() # counts all launches
        #print(successes)
        #print(counts)
        n_success=successes.iloc[0]['class']
        n_counts=counts.iloc[0]['class']
        n_failures = n_counts - n_success
        labels = ['Failures', 'Successes']
        values = [n_failures, n_success]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(entered_site, payload_range):
    min_load = payload_range[0]
    max_load = payload_range[1]
    filtered_df = spacex_df[['Launch Site','Payload Mass (kg)', 'Booster Version', 'class']]
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'].between(min_load,max_load))]
    #print(filtered_df)
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version', hover_data=['Launch Site'])
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version')
        return fig
        # return the outcomes scatter plot Payload vs Outcome chart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()

