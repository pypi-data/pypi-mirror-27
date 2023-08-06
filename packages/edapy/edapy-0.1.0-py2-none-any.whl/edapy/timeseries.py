#!/usr/bin/env python


"""Create and visualize date with timestamps."""

# core modules
from datetime import datetime
import random

# 3rd party module
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def create_data(num_samples, year, month_p=None, day_p=None):
    """
    Create timestamp data.

    Parameters
    ----------
    num_samples : int
    year: int
    month_p : int, optional (default: None)
    day_p : int, optional (default: None)

    Returns
    -------
    data : Pandas.Dataframe object
    """
    data = []
    for _ in range(num_samples):
        if month_p is None:
            month = random.randint(1, 12)
        else:
            month = month_p
        if day_p is None:
            day = random.randint(1, 28)
        else:
            day = day_p
        hour = int(np.random.normal(loc=7) * 3) % 24
        minute = random.randint(0, 59)
        data.append({'date': datetime(year, month, day, hour, minute)})
    data = sorted(data, key=lambda n: n['date'])
    return pd.DataFrame(data)


def visualize_data(df):
    """
    Plot data binned by hour.

    x-axis is the hour, y-axis is the number of datapoints.

    Parameters
    ----------
    df : Pandas.Dataframe object
    """
    df.groupby(df["date"].dt.hour).count().plot(kind="bar")
    plt.show()


df = create_data(2000, 2017)
visualize_data(df)
