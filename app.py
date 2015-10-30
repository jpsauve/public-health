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

# todo
# cleanup, github, README, error

@app.route("/")
def plot_data():
    """Obtains post data and produces two graphs: 
    volume of posts mentioning 'dengue' versus time; and
    volume of posts versus neighborhood
    """
    (df, df_volume, df_by_location) = get_data()
    dates = df_volume.index.map(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    TOOLS = "pan,wheel_zoom,box_zoom,reset,resize"
    fig1 = figure(tools=TOOLS, 
            title='Posts Volume',
            x_axis_label='Date',
            y_axis_label='Volume of Posts',
            x_axis_type='datetime')
    fig1.line(dates, df_volume.values.tolist(), line_width=3)
    script1, div1 = components(fig1, INLINE)

    MAX_NEIGHBORHOODS = 20
    data = {"y": df_by_location.values.tolist()[:MAX_NEIGHBORHOODS]}
    fig2 = Bar(data, 
        cat=df_by_location.index.values.tolist()[:MAX_NEIGHBORHOODS], 
        title="Post Volume per Neighborhood",
        xlabel='Neighborhood', 
        ylabel='Volume of Posts')

    script2, div2 = components(fig2, INLINE)
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