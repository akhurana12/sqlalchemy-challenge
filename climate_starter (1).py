#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd
import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[3]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[4]:


database_path=(r"C:\Users\USER\Desktop\sql alchemy\Surf's up!\Resources\hawaii.sqlite")


# In[5]:


# create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{database_path}")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# View all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[20]:


from sqlalchemy import inspect

inspector=inspect(engine)


# In[21]:


inspector.get_table_names()


# In[22]:


inspector.get_columns('measurement')


# # Exploratory Precipitation Analysis

# In[32]:


# Find the most recent date in the data set.
most_recent_date = session.query(func.max(Measurement.date)).scalar()
session.close()
print("Most recent date:", most_recent_date)


# In[45]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 

last_twelve_months = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
last_twelve_months
# Calculate the date one year from the last date in data set.


# Perform a query to retrieve the data and precipitation scores
p_results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                    filter(Measurement.date >= last_twelve_months).\
                    group_by(Measurement.date).all()
p_results

# Save the query results as a Pandas DataFrame. Explicitly set the column names
precipitation_df = pd.DataFrame(p_results, columns=['Date', 'Precipitation'])
precipitation_df.set_index('Date', inplace=True)
precipitation_df.head()


# Use Pandas Plotting with Matplotlib to plot the data
ax = precipitation_df.plot(kind='bar', width=3, figsize=(12,8))
plt.locator_params(axis='x', nbins=6)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.tick_params(axis='y', labelsize=16)
ax.grid(True)
plt.legend(bbox_to_anchor=(.3,1), fontsize="14")
plt.title("Precipitation Last 12 Months", size=20)
plt.ylabel("Precipitation (Inches)", size=18)
plt.xlabel("Date", size=18)
plt.show


# In[46]:


# Use Pandas to calculate the summary statistics for the precipitation data
precipitation_df.describe()


# # Exploratory Station Analysis

# In[50]:


# Design a query to calculate the total number of stations in the dataset
total_stations = session.query(Station).count()
session.close()
print("Total number of stations:", total_stations)


# In[53]:


# Design a query to find the most active stations (i.e. which stations have the most rows?)
# List the stations and their counts in descending order.
active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()
active_stations


# In[ ]:


# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram


# # Close Session

# In[54]:


# Close Session
session.close()


# In[ ]:




