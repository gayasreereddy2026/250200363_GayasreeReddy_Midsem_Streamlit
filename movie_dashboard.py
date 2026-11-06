import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("IMDb Top 250 Movies Dashboard")

df = pd.read_csv("imdb_top_250.csv")

st.success("Dataset loaded successfully!")

#Q1
st.subheader("First 10 Records")
st.dataframe(df.head(10))

st.subheader("Dataset Information")

st.write("Total Rows:", df.shape[0])
st.write("Total Columns:", df.shape[1])

st.write("Column Names:")
st.write(df.columns)

st.write("Data Types:")
st.write(df.dtypes)

st.subheader("Missing Values")
st.write(df.isnull().sum())

#Q2
st.divider()

st.header("Movie Analytics Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Movies", len(df))

with col2:
    st.metric("Average Rating", round(df['averageRating'].mean(), 2))

with col3:
    st.metric("Highest Rating", df['averageRating'].max())

with col4:
    st.metric("Total Votes", df['numVotes'].sum())


#Q3(a)
st.divider()
st.header("Data Visualizations")

st.subheader("Movies by Genre")

genre_df = df['genres'].str.split(',').explode()

genre_count = genre_df.value_counts()

st.bar_chart(genre_count)

#Q3(b)
st.subheader("IMDb Rating Distribution")

fig, ax = plt.subplots()

ax.hist(df['averageRating'], bins=10)

ax.set_xlabel("IMDb Rating")
ax.set_ylabel("Number of Movies")
ax.set_title("Distribution of IMDb Ratings")

st.pyplot(fig)

#Q3(C)
st.subheader("IMDb Rating vs Number of Votes")

fig, ax = plt.subplots()

ax.scatter(df['averageRating'], df['numVotes'])

ax.set_xlabel("IMDb Rating")
ax.set_ylabel("Number of Votes")
ax.set_title("Rating vs Votes")

st.pyplot(fig)

#Q3(d)
st.subheader("Top 10 Movies by Worldwide Gross")

top_movies = df.sort_values(
    by='grossWorldwide',
    ascending=False
).head(10)

st.bar_chart(top_movies, x='primaryTitle', y='grossWorldwide')
#Q4
tab1, tab2, tab3 = st.tabs([
    "Genre Analysis",
    "Rating Analysis",
    "Gross Collection"
])

with tab1:
    st.subheader("Movies by Genre")

    genre_df = df['genres'].str.split(',').explode()
    genre_count = genre_df.value_counts()

    st.bar_chart(genre_count)

with tab2:
    st.subheader("IMDb Rating Distribution")

    fig, ax = plt.subplots()
    ax.hist(df['averageRating'], bins=10)
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Movies")
    st.pyplot(fig)

    st.subheader("Rating vs Votes")

    fig, ax = plt.subplots()
    ax.scatter(df['averageRating'], df['numVotes'])
    ax.set_xlabel("IMDb Rating")
    ax.set_ylabel("Number of Votes")
    st.pyplot(fig)

with tab3:
    st.subheader("Top 10 Movies by Worldwide Gross")

    top_movies = df.sort_values(
        by='grossWorldwide',
        ascending=False
    ).head(10)

    st.bar_chart(top_movies, x='primaryTitle', y='grossWorldwide')

with st.expander("Dataset Information"):
    st.write("Total Records:", df.shape[0])
    st.write("Total Columns:", df.shape[1])
    st.write("Available Columns:", list(df.columns))

st.divider()

st.info("Explore the IMDb Top 250 Movies dataset using the dashboard.")
st.success("Dashboard loaded successfully!")

#5(a)
st.divider()
st.header("Interactive Movie Explorer")

filtered_df = df.copy()

genre_list = df['genres'].dropna().str.split(',').explode().unique()

selected_genre = st.selectbox(
    "Select Movie Genre",
    ["All"] + sorted(genre_list.tolist())
)

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df['genres'].str.contains(
            selected_genre, na=False
        )
    ]

st.dataframe(filtered_df)

#5(b)
country_list = df['countriesOfOrigin'].dropna().str.split(',').explode().unique()

selected_countries = st.multiselect(
    "Select Countries",
    sorted(country_list.tolist())
)

if selected_countries:
    filtered_df = filtered_df[
        filtered_df['countriesOfOrigin'].apply(
            lambda x: any(
                country in str(x) for country in selected_countries
            )
        )
    ]

#5(c)
min_rating, max_rating = st.slider(
    "Select IMDb Rating Range",
    min_value=0.0,
    max_value=10.0,
    value=(7.0, 10.0),
    step=0.1
)

filtered_df = filtered_df[
    (filtered_df['averageRating'] >= min_rating) &
    (filtered_df['averageRating'] <= max_rating)
]
#5(d)
min_votes = st.number_input(
    "Minimum Number of Votes",
    min_value=0,
    value=1000
)

filtered_df = filtered_df[
    filtered_df['numVotes'] >= min_votes
]
#5(e)
search_movie = st.text_input("Search Movie by Title")

if search_movie:
    filtered_df = filtered_df[
        filtered_df['primaryTitle'].str.contains(
            search_movie, case=False, na=False
        )
    ]

#5(f)
sort_order = st.radio(
    "Sort IMDb Ratings",
    ["Ascending", "Descending"]
)

if sort_order == "Ascending":
    filtered_df = filtered_df.sort_values(
        by='averageRating', ascending=True
    )
else:
    filtered_df = filtered_df.sort_values(
        by='averageRating', ascending=False
    )
#5(g)
st.subheader("Filtered Movie Results")
st.write("Total Movies Found:", len(filtered_df))
#5(h)
st.dataframe(filtered_df)

if st.button("Reset Filters"):
    st.rerun()

#6(a)
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
#6(b)
st.divider()

st.header("Movie Search Form")

with st.form("movie_search_form"):

    movie_name = st.text_input("Enter Movie Title")

    preferred_genre = st.selectbox(
        "Select Preferred Genre",
        sorted(df['genres'].dropna().str.split(',').explode().unique())
    )

    preferred_rating = st.slider(
        "Minimum IMDb Rating",
        0.0, 10.0, 7.0, 0.1
    )

    submitted = st.form_submit_button("Search Movie")
#6(c)
if submitted:

    result = df[
        (df['primaryTitle'].str.contains(
            movie_name, case=False, na=False
        )) &
        (df['genres'].str.contains(
            preferred_genre, case=False, na=False
        )) &
        (df['averageRating'] >= preferred_rating)
    ]

    if not result.empty:
        st.session_state.selected_movie = result.iloc[0]
    else:
        st.session_state.selected_movie = None
#6(d)
if st.session_state.selected_movie is not None:

    movie = st.session_state.selected_movie

    st.success("Movie Found!")

    st.write("Movie Title:", movie['primaryTitle'])
    st.write("Genre:", movie['genres'])
    st.write("IMDb Rating:", movie['averageRating'])
    st.write("Number of Votes:", movie['numVotes'])

else:
    if submitted:
        st.info("No matching movie found. Try different preferences.")