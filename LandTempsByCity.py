"""analyzing and charting the change in temperatures of world cities"""
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
df=pd.read_csv('GlobalLandTempsbyCity.txt')
df = df.rename(columns={'AverageTemperature':'AvgTemp'})
del df['AverageTemperatureUncertainty'],df['Country']
df=df[df['dt'].str.contains('190')|df['dt'].str.contains('200')] #gets years 1900-1909 and 2000-2009
df=df.sort_values(['City','dt'])
df = df.reset_index(drop=True)
df['decAvg']='blank'
i=0
while i<24000:
    decadeAvg=round(sum([float(df['AvgTemp'][i:i+1]) for i in range(i,i+120)])/120,4)
    df['decAvg'][i+119]=decadeAvg
    i+=120   
df=df[df['decAvg']!='blank']
df=df.reset_index(drop=True)
df['centChange']='blank'
i=1
while i<200:
    df['centChange'][i]=round(df['decAvg'][i]-df['decAvg'][i-1],3)
    i+=2
del df['decAvg'],df['dt'],df['AvgTemp']
df=df[df['centChange']!='blank']
df=df.sort_values('centChange',ascending=False)
df=df.reset_index(drop=True)

plt.figure(figsize=(16,16))
plt.title('1905-2005 Change in Average Temperature of 100 Major World Cities',fontsize=18,color='darkblue')
m = Basemap(projection='merc',llcrnrlat=-40,urcrnrlat=65,\
        llcrnrlon=-130,urcrnrlon=160,resolution='c')
m.drawcoastlines()
m.fillcontinents(color='#e0baaa',lake_color='#c2e7e8')
m.drawmapboundary(fill_color='#c2e7e8')
m.drawcountries()
for i in range(100): #change format of lat/lon from 'NESW' to +/-
    if str(df['Latitude'][i])[-1]=='N':
        df['Latitude'][i]=str(df['Latitude'][i])[:-1]
    else:
        df['Latitude'][i]='-'+str(df['Latitude'][i])[:-1]
    if str(df['Longitude'][i])[-1]=='E':
        df['Longitude'][i]=str(df['Longitude'][i])[:-1]
    else:
        df['Longitude'][i]='-'+str(df['Longitude'][i])[:-1]
redshade=plt.get_cmap('OrRd') #create colorshading with red being max
for j in range(100):
    x,y=m(float(df['Longitude'][j]),float(df['Latitude'][j]))
    m.plot(x,y,'o',color=redshade(float(df['centChange'][j])/2),markersize=20,alpha=.85)
    if j<5: plt.annotate(df['City'][j]+':'+str(round(float(df['centChange'][j]),2)),color='black',
            fontsize=12,xy=(x,y),xytext=m(float(df['Longitude'][j])+1,float(df['Latitude'][j])+1))  
light_patch = mpatches.Patch(color=redshade(.25), label='+.5 degC')
med_patch = mpatches.Patch(color=redshade(.5), label='+1 degC')
heavy_patch = mpatches.Patch(color=redshade(.75), label='+1.5 degC')
dark_patch = mpatches.Patch(color=redshade(.999), label='+2 degC')
m.drawparallels(np.arange(-30.,70.,30.),labels=[1,1,1,1])
plt.legend(handles=[light_patch,med_patch,heavy_patch,dark_patch],loc='lower left')
plt.show()
