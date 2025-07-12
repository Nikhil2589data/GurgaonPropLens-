import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(page_title="Recommand Appartments")
from joblib import load

location_df = load('location_distance.joblib')
cosine_sim1 = load('cosine_sim1.joblib')
cosine_sim2 = load('cosine_sim2.joblib')
cosine_sim3 = load('cosine_sim3.joblib')


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df
st.title('Select location and radius')
selected_location=st.selectbox('Location',sorted(location_df.columns.to_list()))
radius=st.number_input('Radius in kms')
if st.button('Search'):
    result_ser=location_df[location_df[selected_location]<radius*1000][selected_location].sort_values()
    if result_ser.empty:
        st.warning("⚠️ No property found within the selected radius.")
    else:
        st.success(f"🏡 Found {len(result_ser)} properties within {radius} km of {selected_location}:")
        for key, value in result_ser.items():
            st.text(str(key)+" "+str(round(value/1000))+'kms')
st.title("recommand appartments")
selected_appartment=st.selectbox('Select an appartment',sorted(location_df.index.to_list()))
if st.button('reccomand'):
    recommendation_df=recommend_properties_with_scores(selected_appartment)
    st.dataframe(recommendation_df)
