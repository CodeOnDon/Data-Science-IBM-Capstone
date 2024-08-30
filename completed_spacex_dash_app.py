# Import required libraries
import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))
path = "/Users/amiliano/Desktop/Coursera/Data Science/machine_learning/notebooks/CapStone"
os.chdir(path)


import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

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
                                dcc.Dropdown(id = 'site-dropdown',
                                             options = [
                                                 {'label':'All Sites','value':'ALL'},
                                                 {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                 {'label':'VAFB SLC-40','value': 'VAFB SLC-4E'},
                                                 {'label':'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                             ],
                                             value = 'ALL',
                                             placeholder = 'Select a Launch Site',
                                             searchable = True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                # TASK 3: Add a slider to select payload range
                                
                                html.P("Payload range (Kg):"),
                                
                                dcc.RangeSlider(id = 'payload-slider',
                                    min = 0, max = 10000, step = 1000,
                                    marks = {0: '0',
                                    2500: '2500',
                                    5000: '5000',
                                    7500: '7500',
                                    10000: '10000'},
                                    value = [min_payload, max_payload]),
                                
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
                                
@app.callback(Output(component_id = 'success-pie-chart',component_property = 'figure'),
                Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values = 'class',
                        names = spacex_df['Launch Site'],
                        title = 'Total Successful Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df,
                        names = 'class',
                        title = 'Total Successful Launches for Site ' + entered_site)
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property= 'figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id = 'payload-slider', component_property= 'value')])

def get_scatter_chart(entered_site, input_payload):
    # the payload-slider value is a list. first number (index = 0) will be the min, second number (indes = 1) = max
    if entered_site == 'ALL':
        mask = (spacex_df['Payload Mass (kg)'] > input_payload[0]) & (spacex_df['Payload Mass (kg)'] < input_payload[1])
        fig = px.scatter(spacex_df[mask], x = 'Payload Mass (kg)', y = 'class',
                         color = 'Booster Version Category',
                         title = 'Payloadmass vs Success of Launch Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        mask = (filtered_df['Payload Mass (kg)'] > input_payload[0]) & (filtered_df['Payload Mass (kg)'] < input_payload[1])
        fig = px.scatter(filtered_df[mask], x = 'Payload Mass (kg)',
                         y = 'class',
                         color = 'Booster Version Category',
                         title = 'Payload Mass vs Success of Launch Site' + entered_site)
        return fig
        


# Run the app
if __name__ == '__main__':
    app.run_server()
    
    
# 1) Which site has the largest successful launches? - KSC-LC 39A with 10 successful launches
# 2) Which launch has the highest launch success rate? - KSC-LC 39A with 76.9% success rate.
# 3) Which payload range(s) has the highest launch succes rate? - (1952kg to 3696kg) and (4600kg - 5300kg)
# 4) Which payload range(s) has the lowest launch success rate? - (362kg - 2000kg) and (5600kg - 6761kg)
# 5) Which F9 booster version has the highest launch success rate? B5 since it had one launch and that one was successful, but with a larger sample size FT. 
