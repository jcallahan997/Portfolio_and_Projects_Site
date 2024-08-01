import os
os.system('pip install idendrogram')
# os.system('pip install streamlit==1.33.0')
# from PIL import _imaging
import numpy as np
import idendrogram
import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import random
from random import sample 
import pyarrow
from pyarrow import csv
from scipy.cluster.hierarchy import dendrogram, linkage

st.title('Hierarchical Clustering on Crash Data')
st.write("Data Source: https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents/data")


#def states():
#    return (car_safety.select(["State"]).to_pandas(split_blocks=True, self_destruct=True))['State'].unique()

state_dict = {
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

option = st.selectbox(
   "State",
   (state_dict)
)

st.write("State selected:", state_dict[option])


@st.cache_data()
def load_crash_data():
    car_safety = csv.read_csv("crash_data_prepped.csv")
    return car_safety #.filter(pyarrow.compute.equal(car_safety['State'], option))

car_safety = load_crash_data()

# car_safety = car_safety_full.filter(pyarrow.compute.equal(car_safety_full['State'], option))

#car_safety = load_crash_data()

# car_safety = Dataset.get("car_safety").select(columns_nonculled).limit(10000).read_table(format="arrow")
  # .where(Column.get("column_name").isin(["value1", "value2"])) # See documentation for other available filters

def sample_table(table: pyarrow.Table, n_sample_rows: int = None) -> pyarrow.Table:
    if n_sample_rows is None or n_sample_rows >= table.num_rows:
        return table

    indices = random.sample(range(table.num_rows), k=n_sample_rows)

    return table.take(indices)

car_safety = sample_table(car_safety.filter(pyarrow.compute.equal(car_safety['State'], option)), 10_000)

def rerun(car_safety): 

    columns_heatmap = ["Severity",
                        "Temperature(F)",
                        "Humidity(%)",
                        "Visibility(mi)",
                        "Wind_Speed(mph)",
                        "Precipitation(in)"
                      ]
    heatmap_data = car_safety.select(["ID"] + columns_heatmap)
    heatmap_data_df_unscaled = heatmap_data.to_pandas(split_blocks=True, self_destruct=True)
    st.write("The data (Sample of 100)")
    st.write(heatmap_data_df_unscaled.head(100))
    # perform mean imputation to handle the nulls
    heatmap_data_df = heatmap_data_df_unscaled.fillna(heatmap_data_df_unscaled[columns_heatmap].median())
    st.write("Correlation Heatmap")
    sb.set_style("whitegrid")
    # sb.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})
    fig, ax = plt.subplots()
    # ax.tick_params(colors='white', which='both')
    sb.heatmap(heatmap_data_df[columns_heatmap].corr(), annot=True, vmin=-1, vmax=1, ax=ax)
    st.write(fig)

    scaler = StandardScaler()
    heatmap_data_df[columns_heatmap] = scaler.fit_transform(heatmap_data_df[columns_heatmap])
    heatmap_data_scaled = heatmap_data_df

    latext = r'''
    ##### Note: The heatmap was made with unscaled data. Not scaling the heatmap data does not change the correlation as correlation is not influenced by differences of scale
    ##### Pearson Correlation Coefficient:
    $$ 
    \ r = \frac{{}\sum_{i=1}^{n} (x_i - \overline{x})(y_i - \overline{y})}
    {\sqrt{\sum_{i=1}^{n} (x_i - \overline{x})^2  \sum_{i=1}^{n}(y_i - \overline{y})^2}}
    $$

    ### Scaled Data
    ###### Nulls handled with median imputation
    '''
    st.write(latext)

    # add descriptive column names
    heatmap_data_scaled_imputed = pd.DataFrame(heatmap_data_scaled, columns = (["ID"] + columns_heatmap))


    st.write(heatmap_data_scaled_imputed.head(100))



    # dendrogram time
    st.subheader("Dendrogram")
    st.write("Created using hierarchical clustering")

    X = heatmap_data_scaled_imputed[columns_heatmap]

    # setting distance_threshold=0 ensures we compute the full tree.
    model_a = AgglomerativeClustering(distance_threshold=65, n_clusters=None, compute_distances=True)

    model = model_a.fit(X)
    cl = model_a.fit_predict(X)
    plt.title("Hierarchical Clustering Dendrogram")
    # plot the top three levels of the dendrogram
    plt.xlabel("Number of points in node")
    #st.pyplot(fig)
    #pass it to idendrogram and visualize
    idd = idendrogram.idendrogram()
    idd.set_cluster_info(idendrogram.ScikitLearnClusteringData(model))

    st.write((idd.create_dendrogram().plot(
        backend='plotly',
        height=600, width=629)))

    # interpreting the dendrogram
    st.write("Interpreting the dendrogram:")

    heatmap_data_scaled_imputed['Cluster'] = cl
    heatmap_data_scaled_imputed_id = heatmap_data_scaled_imputed[['ID', 'Cluster']]
    heatmap_data_pred_joined = heatmap_data_df_unscaled.merge(heatmap_data_scaled_imputed_id, on="ID", how='left')
    d1 = dict.fromkeys(columns_heatmap, 'mean')
    d1['ID']='count'
    st.write("Cluster Averages")
    st.write(heatmap_data_pred_joined.groupby(['Cluster'], as_index=False).agg(d1).rename(columns={"ID":"Count"}))
    st.write("Clustered Data (Sample of 100)")
    st.write(heatmap_data_pred_joined.head(100))
    
st.button('rerun')
    
rerun(car_safety)   
    
