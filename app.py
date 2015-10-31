# -*- coding: utf-8 -*-
"""Flask/bokeh module to generate graphs for the "Dengue" problem.

The module produces graphs of volume and location for Twitter posts given
in a json file

It is meant to run standalone (python app.py) or through heroku

__author__      = "Jacques Sauve"
"""

import flask

import requests
import numpy as np
import pandas as pd
import json
from datetime import date, timedelta, datetime
from calc import read_json, daily_volume, by_location, insert_neighborhood

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.util.string import encode_utf8
from bokeh.palettes import Spectral11
from bokeh.charts import Bar

app = flask.Flask(__name__)

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

DATA_FILE = 'jp-30-days.json'
NEIGHBORHOOD_FILE = 'jp.csv'

def get_data(data_file=DATA_FILE):
    """read_jsons data from the data_file
    Performs a join with the neighborhood info
    Filters posts mentioning 'dengue'
    Produces a dataframe of volume of posts per day
    Produces a dataframe of volume of posts per known (presumed) location of post author
    """
    COLUMNS = ['LocationKey', 'Post', 'PostID', 'TimeStamp', '_id']
    df = read_json(data_file, columns=COLUMNS)
    df = insert_neighborhood(df, NEIGHBORHOOD_FILE, 'osm_id')
    df = df[df['Post'].str.contains('dengue', case=False)]
    df_volume = daily_volume(df)
    df_by_location = by_location(df)
    return (df, df_volume, df_by_location)

TOOLS = "pan,wheel_zoom,box_zoom,reset,resize"
"""Default bokeh tools to show in graph
"""

def volumeGraph(df_volume, tools=TOOLS):
    dates = df_volume.index.map(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    fig = figure(tools=tools, 
            title='Posts Volume',
            x_axis_label='Date',
            y_axis_label='Volume of Posts',
            x_axis_type='datetime')
    fig.line(dates, df_volume.values.tolist(), line_width=3)
    return components(fig, INLINE)

MAX_NEIGHBORHOODS = 20
"""Default maximum number of neighborhoods to show in graph
"""

def locationGraph(df_by_location, max_neighborhoods=MAX_NEIGHBORHOODS):
    data = {"y": df_by_location.values.tolist()[:max_neighborhoods]}
    fig = Bar(data, 
        cat=df_by_location.index.values.tolist()[:max_neighborhoods], 
        title="Post Volume per Neighborhood",
        xlabel='Neighborhood', 
        ylabel='Volume of Posts')

    return components(fig, INLINE)

@app.route("/")
def plot_data():
    """Obtains post data and produces two graphs: 
    volume of posts mentioning 'dengue' versus time; and
    volume of posts versus neighborhood
    """
    (df, df_volume, df_by_location) = get_data()
    script1, div1 = volumeGraph(df_volume)
    script2, div2 = locationGraph(df_by_location)

    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )

    html = flask.render_template(
        'embed.html',
        plot_script1=script1, 
        plot_div1=div1, 
        plot_script2=script2, 
        plot_div2=div2, 
        plot_resources=plot_resources
    )
    return encode_utf8(html)


def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()