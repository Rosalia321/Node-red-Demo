import pandas as pd
from dateutil import parser
import datetime
import numpy as np
import plotly.graph_objects as go
from ipywidgets import widgets
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

data = pd.read_csv('Linea Bob_DashboardData_20240701-030000000_20240729-030000000.csv',sep=';')

def parse_datetime(dt_str):
    return parser.parse(dt_str)

data['_time'] = data['_time'].apply(parse_datetime)


data['year'] = data['_time'].dt.year
data['day'] = data['_time'].dt.day
data['hour'] = data['_time'].dt.hour
data['minuto'] = data['_time'].dt.minute

data['day_hour_minute_second'] = data['_time'].dt.strftime('%Y-%m-%d %H:%M')

parameters = ['CantMinutosParadaTotales', 'OEE','Calidad','EstadoTexto']

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='parameter-dropdown',
        options=[{'label': param, 'value': param} for param in parameters],
        value=parameters[0],  # Default value
        clearable=False,
    ),
    dcc.Graph(id='line-plot'),
])

# Callback to update the line plot
@app.callback(
    Output('line-plot', 'figure'),
    Input('parameter-dropdown', 'value')
)
def update_plot(selected_parameter):

    # Fill NaN values using interpolation (or you can use other methods like forward fill)
    Datos_filtrados = data.dropna(subset=[selected_parameter])


    if selected_parameter == 'EstadoTexto':
        # Create a pie chart
        fig = px.pie(Datos_filtrados, names='EstadoTexto', values=selected_parameter, title=f'{selected_parameter} Distribution')

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
    app.run_server(debug=True)