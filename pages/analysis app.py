
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
st.set_page_config(page_title="Viz demo")
st.title('page2')
new_df=pd.read_csv('datasets/data_viz1.csv')
with open('wordcloud_text.txt', 'r', encoding='utf-8') as f:
    feature_text = f.read()
    # --- Description before map plot ---
    st.subheader("📍 Spatial Price Distribution by Sector")
    st.markdown("""
    This interactive map visualizes the **average price per square foot** across different sectors in Gurgaon.
    The size of each circle represents the **average built-up area**, and the color shows **price per sq ft**.
    """)

group_df = new_df.groupby('sector')[[ 'price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

fig=px.scatter_map(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  map_style="open-street-map",text=group_df.index, width=1200,height=700,hover_name=group_df.index)
st.plotly_chart(fig,use_container_width=True)

# --- Description before word cloud ---
st.subheader("☁️ Most Common Features in Listings")
st.markdown("""
The following **word cloud** showcases the most frequent terms or features extracted from the property descriptions. 
It helps understand the common selling points or amenities in demand.
""")

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

fig_wc, ax = plt.subplots(figsize=(8, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)
st.pyplot(fig_wc) # st.pyplot()
st.header('Area vs Price')
property_type=st.selectbox('Select Property type',['flat','house'])
if property_type=='house':
    fig1 = px.scatter(new_df[new_df['property_type']=='house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1,use_container_width=True,key='house_chart')
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True,key='house_chart')

st.header('BHK pie chart')
sector_options=new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
selected_sector=st.selectbox('Select Sector', sector_options)
if selected_sector=='overall':
    fig2=px.pie(new_df,names='bedRoom',title='total bill amount by Day')
    st.plotly_chart(fig2,use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector']==selected_sector], names='bedRoom', title='total bill amount by Day')
    st.plotly_chart(fig2, use_container_width=True)


st.header('side by side BHK price comparision')

fig4, ax = plt.subplots(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], kde=True, label='House', ax=ax)
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], kde=True, label='Flat', ax=ax)
ax.legend()
ax.set_title("Price Distribution: House vs Flat")

st.pyplot(fig4)