
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
import os

history = db.session.query(History).all()

def get_volumes(user):
    result = []
    for h in history:
        if user.id == 1:
            result.append(h.weights*h.weights*h.set)
    return result


def get_times(user):
    result = []
    for h in history:
        if user.id == 1:
            result.append(datetime.fromtimestamp(h.time/1000))
    return result

def get_dates():
    result = []
    for h in history:
        result.append(datetime.fromtimestamp(h.time/1000).date())
    return result

def get_image(user):
    os.remove('templates/personal.html')
    times = get_times(user)
    volumes = get_volumes(user)
    dates = get_dates()
    fig = go.Figure(data=go.Scatter(
        x=get_dates(),
        y=get_volumes(user),
        mode='lines+markers',
        marker=dict(
            size=16,
            color='#FF4500',
            colorscale='YlOrRd',
            showscale=True
        )
    ))

    fig.write_html('templates/personal.html', auto_open=False)
