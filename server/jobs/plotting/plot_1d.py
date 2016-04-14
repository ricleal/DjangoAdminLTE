
from plotly.offline import plot
import plotly.graph_objs as go

def plot1d(list_plot_data):
    '''
    @param list_plot_data: See data.iq_string_to_plot_format for the format
    '''
    traces = []
    for dataset in list_plot_data:
        trace = go.Scatter(
            x=dataset['X'],
            y=dataset['Y'],
            error_y=dict(
                type='data',
                array=dataset['E'],
                visible=True
            ),
            name=dataset['name']
        )
        traces.append(trace)

    layout = go.Layout(
        showlegend=True,
        autosize=False,
        width=900,
        height=600,
        xaxis=dict(
            type='log',
            autorange=True
        ),
        yaxis=dict(
            type='log',
            autorange=True
        )
    )
    fig = go.Figure(data=traces, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
