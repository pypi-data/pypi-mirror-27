"""Support functions for geographic operations"""


def aspect(df):
    """Return the aspect ratio of a Geopandas dataset"""
    tb = df.total_bounds
    return abs((tb[0] - tb[2]) / (tb[1] - tb[3]))


def scale(df, x):
    """Given an x dimension, return the x and y dimensions to maintain the dataframe aspect ratio"""
    return (x, x / aspect(df))


def aspect_fig_size(df, width, subplots='111', **kwargs):
    """
    Create a matplotlib figure and axis with a given X width and a height
    to keep the boundary box aspect ratio.

    :param df: Geopandas GeoDataFrame, from which to calculate the aspect ratio
    :param width:  X dimension, in inches, of the plot
    :param subplots: A Matplotlib subplots string
    :param kwargs: Other arguments for plt.figure
    :return:
    """
    import matplotlib.pylab as plt


    fig = plt.figure(figsize = scale(df, width), **kwargs)
    ax = fig.add_subplot(subplots)
    return fig, ax

def total_centroid(df):
    return list(reversed(df.geometry.unary_union.centroid.coords[0]))


def folium_map(df, data_column, tiles='Stamen Toner', zoom_start=12, **kwargs):


    import folium
    mapa = folium.Map(location=total_centroid(df),
               tiles=tiles, zoom_start=zoom_start)

    if not df.crs:
        df.crs = {'init' :'epsg:4326'}

    #threshold_scale = np.linspace(_['non_min_r'].min(),
    #                              _['non_min_r'].max(), 6, dtype=float).tolist()

    choro_args = dict(
         fill_color='RdYlGn',
         fill_opacity=.6,
         line_weight=.7
    )

    mapa.choropleth(geo_data=df.reset_index(),
                    data=df.reset_index(),
                    key_on='feature.properties.geoid',
                    columns=['geoid',data_column],
                    **choro_args
                   )

    return mapa

