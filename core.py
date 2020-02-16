
import math
import pandas
from io import BytesIO
from app import db, User, History
from datetime import datetime
import plotly.express as px
import plotly
import chart_studio.plotly as py
import plotly.graph_objects as go
import numpy as np


history = db.session.query(History).all()

def get_volumes():
    result = []
    for h in history:
        result.append(h.weights*h.weights*h.set)
    return result


def get_times():
    result = []
    for h in history:
        result.append(datetime.fromtimestamp(h.time/1000))
    return result

def get_dates():
    result = []
    for h in history:
        result.append(datetime.fromtimestamp(h.time/1000).date())
    return result

def get_image():
    times = get_times()
    volumes = get_volumes()
    dates = get_dates()

    fig = go.Figure(data=go.Scatter(
        x=get_dates(),
        y=get_volumes(),
        mode='lines+markers',
        marker=dict(
            size=16,
            color='#FF4500',
            colorscale='YlOrRd',
            showscale=True
        )
    ))
    plotly.offline.plot(fig, filename='/templates/personal.html', output_type='div')
