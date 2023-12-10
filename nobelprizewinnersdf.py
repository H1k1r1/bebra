import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import streamlit as st

st.title('## **Start**')
"""

So, let's start, I chose a dataset to analyze from kaggle.com, it's called 'Nobel Prize Winners'.

This is a dataset containing information about the laureates from 1901 to the present.

There are 1000 rows and 16 columns in the dataset.

It contains the following data:
1. Year
2. Category
3. Motivation
4. prizeShare
5. laurateID
6. fullName
7. gender
8. born
9. bornCountry
10. bornCity
11. died
12. diedCountry
13. diedCity
14. organizationName
15. organizationCountry
16. organizationCity

## **1.Importing and opening a dataset**

The first step is to import the necessary libraries to work with:
"""

import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from matplotlib import pyplot as plt

"""Let's open the dataset itself and look at the data that is in it:

"""

NobelPrizeWinnersdf = pd.read_csv('/content/nobel_laureates_data.csv')
NobelPrizeWinnersdf

"""Note that there are empty lines and dates of death with all zeros (the person is alive):"""

NobelPrizeWinnersdf.info()

"""As you can see, NaN is present in the dataset, let's look at their number in each column in more detail:"""

NobelPrizeWinnersdf.isna().sum()

"""## **2.Cleaning and converting the dataset**

First of all, let's look at the number of genders:
"""

NobelPrizeWinnersdf['gender'].unique()

"""Lucky, there are only 3 of them. For myself, I will replace the org-organization for greater clarity, as well as rewrite all genders with a capital letter:"""

NobelPrizeWinnersdf['gender'] = NobelPrizeWinnersdf['gender'].replace('org','Organizations').replace('male','Male').replace('female','Female')
NobelPrizeWinnersdf['gender'].unique()

"""I'll do the same with the 'category' column:"""

NobelPrizeWinnersdf['category'].unique()

"""There are only 6 different values in it, so it's not difficult:"""

NobelPrizeWinnersdf['category'] = NobelPrizeWinnersdf['category'].replace('medicine','Medicine').replace('economics','Economics').replace('peace','Peace').replace('peace','Peace').replace('literature','Literature').replace('chemistry','Chemistry').replace('physics','Physics')
NobelPrizeWinnersdf['category'].unique()

"""Now replace the empty lines with the standard value - 'Not Stated':"""

NobelPrizeWinnersdf.fillna('Not Stated',inplace = True)
NobelPrizeWinnersdf

"""Now let's start processing the dates of birth and death:

Let's look at the option of recording these dates:
"""

NobelPrizeWinnersdf['born'].unique()

NobelPrizeWinnersdf['died'].unique()

"""We see that they are written either through '/' or through '-'.

We will remove them, as well as days and months, so they will not be needed for analysis:
"""

def changetoYearorDel(a):
    s = a.replace('-',' ').replace('/',' ').split()
    for i in s:
        i = str(i)
        if len(i) == 4 and i.isdigit():
            i = int(i)
            if i <= 2023:
                return i


NobelPrizeWinnersdf['born'] = [changetoYearorDel(i) for i in NobelPrizeWinnersdf['born']]
NobelPrizeWinnersdf['died'] = [changetoYearorDel(i) for i in NobelPrizeWinnersdf['died']]
NobelPrizeWinnersdf

"""Note that the column with the dates of death remained in float format:

Let's look at the values of both columns again:
"""

NobelPrizeWinnersdf['born'].unique()

NobelPrizeWinnersdf['died'].unique()

"""As you can see, empty values('nan') appeared in the column with deaths:

For now, I'll just replace them with any numeric value to convert the column to int format:
"""

NobelPrizeWinnersdf.fillna(11,inplace = True)
NobelPrizeWinnersdf

"""We check the column again:"""

NobelPrizeWinnersdf['died'].unique()

"""Now it can be converted to int format, but before that, let's look at the strings with this value:"""

find = NobelPrizeWinnersdf[NobelPrizeWinnersdf['died'] == 11].index
find

"""You are probably out of order with arbitrary values from this list:"""

NobelPrizeWinnersdf.loc[[16, 78, 602]]

"""As you can see, these are the values where the organization received the award.Then it is logical that there can be no date of death.

For now, let's leave this value in this form, because organizations will be useful for plotting.

Let's convert both columns to int format (the birth rate column is already in this format, but just in case, let's do it again):
"""

NobelPrizeWinnersdf['born'] = NobelPrizeWinnersdf['born'].astype(int)
NobelPrizeWinnersdf['died'] = NobelPrizeWinnersdf['died'].astype(int)
NobelPrizeWinnersdf

"""It remains to get rid of the dates of death with the value '0'.They can be replaced either by 'alive' or for the current year, that is, by '2023'.Since I'm going to count the age of people, I'll set the value to '2023':"""

NobelPrizeWinnersdf['died'] = NobelPrizeWinnersdf['died'].replace(0,2023)
NobelPrizeWinnersdf['died'].unique()

"""As you can see, everything worked.

I will also convert the remaining columns with numeric values to int format in advance, if I use them:
"""

NobelPrizeWinnersdf['year'] = NobelPrizeWinnersdf['year'].astype(int)
NobelPrizeWinnersdf['prizeShare'] = NobelPrizeWinnersdf['prizeShare'].astype(int)
NobelPrizeWinnersdf['laureateID'] = NobelPrizeWinnersdf['laureateID'].astype(int)
NobelPrizeWinnersdf

"""I'm rechecking the columns with the dates of birth and death again:"""

NobelPrizeWinnersdf['born'].unique()

NobelPrizeWinnersdf['died'].unique()

"""Also, let's check the number of Nan in the columns again."""

NobelPrizeWinnersdf.isna().sum()

"""Excellent, the dataset is cleaned and presented in a normal form.Now you can start plotting and analyzing the dataset using them.

## **3.Overview.Plotting and hypothesizing**

Now let's think about what actual statistics do we have in our dataset, let's firstly create mean, median and standard deviation of some numerical fields:
"""

mean1 = NobelPrizeWinnersdf['year'].mean()
median1 = NobelPrizeWinnersdf['year'].median()
standard1 = NobelPrizeWinnersdf['year'].std()
print(mean1)
print(median1)
print(standard1)

mean2 = NobelPrizeWinnersdf['prizeShare'].mean()
median2 = NobelPrizeWinnersdf['prizeShare'].median()
standard2 = NobelPrizeWinnersdf['prizeShare'].std()
print(mean2)
print(median2)
print(standard2)

"""As you can see, the data is quite normal.

Let's look at the values for another column after it is created.

The first schedule I will look at the awards received by year by each gender.I think that men have always received a prize, but women have not, because previously women did not receive higher education and rarely delved into science.
"""

scatter = px.scatter(NobelPrizeWinnersdf, x='year', y='gender',color = 'gender', symbol = 'gender',color_discrete_sequence=['red', 'blue', 'lime'])
scatter.update_layout(title_text='The rate of awarding prizes to different genders by year')
scatter.show()

"""As you can see, every year a man received the award.Women began to receive a contract only in 2018. Organizations have rarely been awarded this award at all.
The longest streak was only 3 years (2005-2007 inclusive). It is also clear that no one received the prize in 1940-1942, so there was the Second World War.

Therefore, my hypothesis has been confirmed.

Let's display the same data as a percentage on another graph.
"""

pie1 = px.pie(NobelPrizeWinnersdf,'gender',color_discrete_sequence=px.colors.sequential.Sunsetdark)
pie1.update_traces(textposition='inside', textinfo='percent+label')
pie1.update_layout(title_text='Percentage of genders')
pie1.show()

"""Here you can clearly see the superiority of men in receiving the award.

Now we will remove the values of 'Organizations', since we will no longer need them, but they may interfere with calculating the ages of the laureates:
"""

NobelPrizeWinnersdf.drop(find,inplace = True)
NobelPrizeWinnersdf['died'].unique()

"""Now let's calculate the age:"""

spisok = NobelPrizeWinnersdf[['born','died']].values.tolist()
NobelPrizeWinnersdf['age'] = [int(i[1] - i[0]) for i in spisok]
NobelPrizeWinnersdf

"""Now let's create an average value, median and standard deviation of some numeric fields for 3 columns:"""

mean3 = NobelPrizeWinnersdf['age'].mean()
median3 = NobelPrizeWinnersdf['age'].median()
standard3 = NobelPrizeWinnersdf['age'].std()
print(mean3)
print(median3)
print(standard3)

"""Also, all numbers are normal.

Let's make a graph of the birth rate density by the death of the laureates. It shows that the densest relationship begins from 1900 to our time. I think that the density will be more and more dense.
"""

ratio = NobelPrizeWinnersdf.plot(kind='scatter', x='born', y='died',title = 'The ratio of birth to death of Nobel laureates', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

"""After ~1900, the grouping became denser and denser, as I assumed.

Let's also look at the number of laureates by the years they have lived. I think most of them have lived for about 60-80 years.
"""

histogram = px.histogram(NobelPrizeWinnersdf, x='age', title='Age Proportion',color_discrete_sequence=['#6A5ACD'],barmode='overlay')
histogram.update_yaxes(range=[0, 81])

histogram.show()

"""As you can see, there are those who lived 26-31 years and even 102-103, and my guess turned out to be practically correct, but most lived 70-90 years.

Now let's see which country most of the award winners are from.I can't say which country, but I think it's from Western Europe.
"""

pie2 = px.pie(NobelPrizeWinnersdf,'bornCountry')
pie2.update_traces(textposition='inside', textinfo='percent+label')
pie2.update_layout(title_text='Percentage of countries by the number of Nobel Prize winners')
pie2.show()

"""For greater clarity, we will display only the top 10:"""

d = {}
for i in NobelPrizeWinnersdf['bornCountry']:
        if i in d.keys():
            d[i] += 1
        else:
            d[i] = 1

SupDf = pd.DataFrame({'bornCountry': d.keys(),'count': d.values()})
SupDf['count'] = SupDf['count'].astype(int)
find1 = SupDf[SupDf['count'] <= 19].index
SupDf.drop(find1,inplace = True)
SupDf

pie3 = px.pie(SupDf,values = 'count',names = 'bornCountry')
pie3.update_traces(textposition='inside', textinfo='percent+label')
pie3.update_layout(title_text='Percentage of countries by the number of Nobel Prize winners')
pie3.show()

"""My guess was not confirmed, most were born in the United States of America. Although this is not surprising, due to the absence of wars on the territory of this country throughout the years of the award, a good standard of living, the development of science, industry and education.
Also the entire top 10 countries:

1.   USA
2.   UK
3.   Germany
4.   France
5.   Sweden
6.   Russia
7.   Poland
8.   Japan
9.   Canada
10.  Italy

Let's display the same values on another graph in the form of a world map:
"""

countries_count = NobelPrizeWinnersdf['bornCountry'].value_counts()
countries_percent = ((countries_count / countries_count.sum()) * 100).round(2)
countries_keys = countries_percent.index
countries_values = countries_percent.values

world_map = go.Figure(data=go.Choropleth(
    locations=countries_keys,
    z=countries_values,
    locationmode='country names',
    colorscale='Reds',
    colorbar_title='Proportion (%)',
    marker_line_color='DarkRed',
    marker_line_width=1,
    hovertemplate='%{location}<br>Nobel Prize Winners: %{z}%<extra></extra>'))

world_map.update_traces(zmin=0, zmax=countries_percent.max())

world_map.update_layout(title_text='Nobel Prizes per country Proportion')

world_map.show()

"""And in the form of a line graph.

Let's also see which country is the leader in the organizations of the laureates. Most likely it will be the United States again.
"""

countries_count1 = NobelPrizeWinnersdf['organizationCountry'].value_counts()
countries_percent1 = ((countries_count1 / countries_count1.sum()) * 100).round(2)
countries_keys1 = countries_percent1.index
countries_values1 = countries_percent1.values

world_map1= go.Figure(data=go.Choropleth(
    locations=countries_keys1,
    z=countries_values1,
    locationmode='country names',
    colorscale='Blues',
    colorbar_title='Proportion (%)',
    marker_line_color='DarkBlue',
    marker_line_width=1,
    hovertemplate='%{location}<br>Nobel Prize Winners: %{z}%<extra></extra>'))

world_map1.update_traces(zmin=0, zmax=countries_percent1.max())

world_map1.update_layout(title_text='Nobel Prizes per organizationcountry Proportion')

world_map1.show()

"""As I suggested, the USA is also in the first place here.

We also display this through the pie chart.
"""

pie4 = px.pie(NobelPrizeWinnersdf,'organizationCountry')
pie4.update_traces(textposition='inside', textinfo='percent+label')
pie4.update_layout(title_text='Percentage of countries by the number of Nobel Prize winners')
pie4.show()

"""As we can also see, many people receive a bonus without being in any organization.

Now let's look at the graph of the number of awards received in different categories and the average life expectancy of the holders of these awards. I think that medicine, chemistry and physics will be the leaders.
"""

bar = NobelPrizeWinnersdf.groupby('category').size()
bar2 = NobelPrizeWinnersdf.groupby('category')['age'].mean()
print(bar2)
df = pd.DataFrame({'name':['chemistry','economics','literature','medicine','peace','physics'],'count':bar,'age':bar2})
df

"""Let's leave the age in float format for more accurate values."""

fig = px.bar(df, x='count', y='name',color='age', height=400)
fig.update_layout(title_text='Nobel Prizes per country Proportion')
fig.show()

"""As you can see, the prize in medicine was awarded 227 times, and the average life expectancy of the laureates is ~ 81 years, physics is almost at the same level: 225 times and the average duration is ~ 81 years. But the literature is quite far away: 120 awards and an average duration of ~ 79 years.

## **Results of the analysis**

Such an analysis of the data showed that the majority of the award winners are men, most of whom are from the United States and the age of the majority: 60-90 years old. Also, most of the awards were in the field of medicine, and the average life expectancy of the laureates was 81 years
"""