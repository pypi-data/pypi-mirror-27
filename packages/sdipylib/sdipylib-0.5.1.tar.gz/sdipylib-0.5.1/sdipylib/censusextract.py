""" Functions for working with census extracts, from 
https://github.com/CivicKnowledge/census-extract"""

def make_col_map(schema_df):
    
    """Returns a column map, from census colum ids to column titles, given a pandas Dataframe
    created from the schema csv file for a table. ie: 
    
    schema_df = pandas.read_csv('http://extracts.census.civicknowledge.com/2014/5/140_tract/b01001-schema.csv')
    colmap = make_col_map(schema_df)
    """
    
    col_map = {}

    new_titles = []
    last_heading = ''

    for col_id, col_title in schema_df.loc[8:][['name','description']].values.tolist():
        if col_id.endswith('m90'):
            continue

        if col_title.endswith(':'):
            col_title = col_title.strip(':')
            col_map[col_id] = col_title
            last_heading = col_title
        else:
            col_map[col_id] = last_heading+' '+col_title
    
    # Now, add back in entries for the margins
    for k, v in col_map.items():
        col_map[k+'_m90'] = 'Margin for '+v
        
    return col_map
    
def load_table(table, summary_level, year=2014, release=5):
    url_params = {
        'base_url': 'http://extracts.census.civicknowledge.com',
        'year': 2014,
        'release': 5, 
        'summary_level': '140_tract',
        'table': 'b01001'
    }
    
    template = '{base_url}/{year}/{release}/{summary_level}/{table}'
    data_template = template+".csv"
    schema_template = template+'-schema.csv'

    df = pd.read_csv(data_template.format(**url_params))
    schema_df = pd.read_csv(schema_template.format(**url_params))
    
    col_map = make_col_map(schema_df)
    
    return df, schema_df, col_map