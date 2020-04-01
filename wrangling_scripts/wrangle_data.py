import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`
def clean_data(dataset):
    df = pd.read_csv(dataset)
    df=df[:218]
    df = df[['Country Name', '2000 [YR2000]' ,'2014 [YR2014]']]
    countrylist = ['United States', 'China', 'India', 'Pakistan', 'Japan', 'Russian Federation', 'Bangladesh', 'Nigeria', 'Brazil', 'Indonesia']
    df = df[df['Country Name'].isin(countrylist)]
    df.rename(columns={'Country Name': 'Country Name', '2000 [YR2000]': '2000', '2014 [YR2014]': '2014'}, inplace=True)
    df_melt = df.melt(id_vars='Country Name', value_vars = ['2000', '2014'])
    df_melt.columns = ['country', 'year', 'columns']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year
    
    return df_melt


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    graph_one = [] 
    df_melt = clean_data('data/b055f1ad-17cc-43fd-bc5e-8a9572a0e573_Data.csv')
    df_melt.columns = ['country', 'year', 'population']
    df_melt.sort_values('population', ascending=False, inplace=True)
    top10 = df_melt.country.unique().tolist()
    
    for country in top10:
        x_val = df_melt[df_melt['country']==country].year.tolist()
        y_val = df_melt[df_melt['country']==country].population.tolist()    
    
   
        graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
        )

    layout_one = dict(title = 'Most Populous countries growth(2000-2015)',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Population'),
                )
    
# second chart plots ararble land for 2015 as a bar chart    
    
    graph_two = []
    
    df_2 = clean_data("data/co2emissions.csv")
    df_2.columns = ['country', 'years','CO2']
    df_2.sort_values('CO2', ascending=False, inplace=True)
    for country in top10:
        x_val = df_2[df_2['country']==country].years.tolist()
        y_val = df_2[df_2['country']==country].CO2.tolist() 
        graph_two.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines+markers',
        name = country
            )
            )

    layout_two = dict(title = 'CO2 emissions in most populous countries',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'CO2 emissions'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df_3 = clean_data('data/GDP.csv')
    df_3.columns = ['country','year','GDP']
    df_3.sort_values('GDP', ascending=False, inplace=True)
    df_3=df_3[df_3['year'] ==2014]
    graph_three.append(
      go.Bar(
      x = df_3.country.tolist(),
      y = df_3.GDP.tolist(),
      )
    )

    layout_three = dict(title = 'GDP in USD',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'GDP(USD)')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    df_4 = clean_data('data/TotalArea.csv')
    df_4.columns = ['country','year', 'area']
    df_4.sort_values('area', ascending=False, inplace=True)
    df_4=df_4[df_4['year']==2014]
    graph_four.append(
      go.Bar(
      x = df_4.country.tolist(),
      y = df_4.area.tolist(),
      )
    )

    layout_four = dict(title = 'Total Area (Sq. Km)',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'Total Area'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures