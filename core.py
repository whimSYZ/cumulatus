import numpy
import matplotlib
import matplotlib.pyplot as plt
import math
import pandas
from io import BytesIO
from app import db, User, History
from datetime import datetime

plt.style.use('ggplot')
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
    plt.clf()
    plt.scatter(times, volumes, alpha=0.5)
    plt.title('Time vs. Volume')
    plt.ylabel('Volume')
    plt.xlabel('Time')
    for i, txt in enumerate(dates):
        plt.annotate(txt, (dates[i], volumes[i]))
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img