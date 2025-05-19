import streamlit as st
import pandas as pd

# Load the dataset (assumes netflix_titles.csv is in the same directory)
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    df.columns = df.columns.str.strip().str.lower()
    # Ensure release_year is numeric
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    return df

df = load_data()

st.title('Netflix Movie Search (Streamlit)')

# Year filter
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.slider('Filter by release year', min_year, max_year, (min_year, max_year))

movie_title = st.text_input('Enter movie title:')

# Filter dataframe by year range
filtered_df = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]

if movie_title:
    match = filtered_df[filtered_df['title'].str.strip().str.lower() == movie_title.strip().lower()]
    if not match.empty:
        record = match.iloc[0]
        st.markdown(f"""
        **Title:** {record['title']}  
        **Genre:** {record['genre']}  
        **Year:** {record['release_year']}  
        **Duration:** {record['duration']}  
        **Description:** {record['description']}
        """)
    else:
        st.error('Movie not found in database.')
else:
    # If no title is entered, show all books/movies in the selected year range
    st.subheader('All Movies/Books in Selected Year Range')
    st.dataframe(filtered_df[['title', 'genre', 'release_year', 'duration', 'description']].reset_index(drop=True))
