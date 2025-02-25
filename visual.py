import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# @st.cache_data
def load_data():
    return pd.read_csv('thai_air_data_cleaned.csv')

data = load_data()

st.title('Thai Air Data Visualization')

st.subheader('DataFrame')
st.write(data)

st.subheader('Summary Statistics')
st.write(data.describe())
columns = data.columns.tolist()

st.subheader('Correlation Heatmap')
correlation_matrix = data.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(10, 8))
for (i, j), val in np.ndenumerate(correlation_matrix):
    ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')
cax = ax.matshow(correlation_matrix, cmap='coolwarm')
fig.colorbar(cax)
ax.set_xticks(range(len(correlation_matrix.columns)))
ax.set_yticks(range(len(correlation_matrix.columns)))
ax.set_xticklabels(correlation_matrix.columns, rotation=90)
ax.set_yticklabels(correlation_matrix.columns)
st.pyplot(fig)


st.subheader('Scatter Matrix')
selected_columns = st.multiselect('Select Columns for Scatter Matrix', columns, default=columns[3:])
hue_scatter_matrix = st.selectbox('Select Hue for Scatter Matrix', columns, key='scatter_matrix_hue', index=columns.index('pm25'))
if len(selected_columns) > 1:
    scatter_matrix_fig = pd.plotting.scatter_matrix(data[selected_columns].fillna(-1), figsize=(10, 10), diagonal='kde', c=data[hue_scatter_matrix], cmap='viridis')
    st.pyplot(scatter_matrix_fig[0][0].figure)
else:
    st.write("Please select at least two columns for the scatter matrix.")

st.subheader('Box Plot')
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
selected_box_columns = st.multiselect('Select Columns for Box Plot', numeric_columns, default=numeric_columns)
if selected_box_columns:
    fig, ax = plt.subplots()
    data[selected_box_columns].plot(kind='box', ax=ax)
    st.pyplot(fig)
else:
    st.write("Please select at least one column for the box plot.")



st.subheader('Scatter Plot')
x_axis_scatter = st.selectbox('Select X-axis for Scatter Plot', columns, key='scatter_x', index=columns.index('lat'))
y_axis_scatter = st.selectbox('Select Y-axis for Scatter Plot', columns, key='scatter_y', index=columns.index('pm25'))
hue_scatter = st.selectbox('Select Hue for Scatter Plot', columns, key='scatter_hue', index=columns.index('pm25'))
fig, ax = plt.subplots()
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
data[hue_scatter] = label_encoder.fit_transform(data[hue_scatter])
scatter = ax.scatter(data[x_axis_scatter], data[y_axis_scatter], c=data[hue_scatter], cmap='viridis')
ax.set_xlabel(x_axis_scatter)
ax.set_ylabel(y_axis_scatter)
fig.colorbar(scatter, ax=ax, label=hue_scatter)
st.pyplot(fig)

# st.subheader('Line Plot')
# x_axis_line = st.selectbox('Select X-axis for Line Plot', columns, key='line_x', index=columns.index('lat'))
# y_axis_line = st.selectbox('Select Y-axis for Line Plot', columns, key='line_y', index=columns.index('pm25'))
# hue_line = st.selectbox('Select Hue for Line Plot', columns, key='line_hue', index=columns.index('pm25'))
# fig, ax = plt.subplots()
# for hue_value in data[hue_line].unique():
#     subset = data[data[hue_line] == hue_value]
#     ax.plot(subset[x_axis_line], subset[y_axis_line], label=hue_value)
# ax.set_xlabel(x_axis_line)
# ax.set_ylabel(y_axis_line)
# show_legend_line = st.radio('Show Legend for Line Plot?', ('No', 'Yes'), index=0)
# if show_legend_line == 'Yes':
#     ax.legend(title=hue_line)
# st.pyplot(fig)

st.subheader('Bar Plot')
x_axis_bar = st.selectbox('Select X-axis for Bar Plot', columns, key='bar_x', index=columns.index('lat'))
y_axis_bar = st.selectbox('Select Y-axis for Bar Plot', columns, key='bar_y', index=columns.index('pm25'))
hue_bar = st.selectbox('Select Hue for Bar Plot', columns, key='bar_hue', index=columns.index('pm25'))
fig, ax = plt.subplots()
for hue_value in data[hue_bar].unique():
    subset = data[data[hue_bar] == hue_value]
    ax.bar(subset[x_axis_bar], subset[y_axis_bar], label=hue_value)
ax.set_xlabel(x_axis_bar)
ax.set_ylabel(y_axis_bar)
show_legend_line_bar = st.radio('Show Legend for Bar Plot?', ('No', 'Yes'), index=0)
if show_legend_line_bar == 'Yes':
    ax.legend(title=hue_bar)
st.pyplot(fig)


# Time Series Trend Line
st.subheader('Time Series Trend Line')
time_column = 'time'
y_axis_trend = st.selectbox('Select Y-axis for Trend Line', numeric_columns, key='trend_y', index=numeric_columns.index('pm25'))
city_filter = st.selectbox('Select City for Trend Line', data['City'].unique(), key='city_filter')

# Convert the time column to datetime
data[time_column] = pd.to_datetime(data[time_column])

# Filter data by selected city
filtered_data = data[data['City'] == city_filter]

fig, ax = plt.subplots()
ax.plot(filtered_data[time_column], filtered_data[y_axis_trend], label=city_filter)
ax.set_xlabel(time_column)
ax.set_ylabel(y_axis_trend)
ax.set_title(f'Trend Line for {city_filter}')
st.pyplot(fig)