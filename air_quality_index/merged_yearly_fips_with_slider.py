import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("pivot_df.csv")

df = df.melt(id_vars='fips', value_vars=df.columns, var_name='year')


fig = px.choropleth(df,
                    geojson=counties,
                    locations='fips',
                    color='value',
                    color_continuous_scale="Viridis",
                    animation_frame='year',
                    range_color=(0, 50),
                    scope="usa",
                    labels={'air_quality_index': 'Air Quality Index'})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
if __name__ == '__main__':

    fig.show()