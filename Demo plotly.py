import pandas as pd
from dateutil import parser
import datetime
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from flask import request
import io

# Initialize the Dash app
app = Dash(__name__)

# Global variable to store the data
data = pd.DataFrame()

# Endpoint to receive CSV data from Node-RED
@app.server.route('/upload-csv', methods=['POST'])

def upload_csv():

    global data
    # Read the CSV file from the POST request
    csv_file = io.StringIO(request.data.decode('utf-8'))
    # Convert to DataFrame
    data = pd.read_csv(csv_file)

    #def parse_datetime(dt_str):
        #return parser.parse(dt_str)

    #data['_time'] = data['_time'].apply(parse_datetime)

    data['_time'] = pd.to_datetime(data['_time'])

    data['year'] = data['_time'].dt.year
    data['day'] = data['_time'].dt.day
    data['hour'] = data['_time'].dt.hour
    data['minuto'] = data['_time'].dt.minute

    data['day_hour_minute_second'] = data['_time'].dt.strftime('%Y-%m-%d %H:%M')

    return "CSV uploaded successfully!", 200

parameters = ['CantMinutosParadaTotales', 'OEE','Calidad','EstadoTexto']

# Layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='parameter-dropdown',
        options=[{'label': param, 'value': param} for param in parameters],
        value=parameters[0],  # Default value
        clearable=False,
    ),
    dcc.Graph(id='graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    ),
])

# Callback to update the line plot
@app.callback(
    Output('graph', 'figure'),
    Input('parameter-dropdown', 'value')
)
   
def update_plot(selected_parameter):

    if data.empty:
        return go.Figure()
    
    # Fill NaN values using interpolation (or you can use other methods like forward fill)
    Datos_filtrados = data.dropna(subset=[selected_parameter])


    if selected_parameter == 'EstadoTexto':
        # Create a pie chart
        Estado_data = Datos_filtrados[selected_parameter].value_counts().reset_index()
        Estado_data.columns = ['EstadoTexto','cuenta']

        fig = px.pie(Estado_data, names='EstadoTexto', values='cuenta', title=f'{selected_parameter} Distribution')
        

    else:
        # Create the plot with the selected parameter
        fig = px.line(Datos_filtrados, x='day_hour_minute_second', y=selected_parameter, title=f'{selected_parameter} over Time')
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title=selected_parameter,
            xaxis_rangeslider=dict(
                visible=True,
                thickness=0.05,
            ),
            xaxis=dict(
                tickangle=45,
                showgrid=True,
                tickmode='auto',
                nticks=20
            ),
            yaxis=dict(
                showgrid=True
            )
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)