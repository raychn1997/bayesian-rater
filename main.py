import streamlit as st
import pandas as pd
import numpy as np


# Helper function to calculate the adjusted rating
def rate(n, rating_avg):
    # Convert the rating from a scale of 1-5 to 0.2-1
    s = 1/5 * rating_avg * n

    # Apply the approximation formula
    a = 1 + s
    b = 1 + n - s
    mu = a/(a+b)
    std_err = 1.65 * np.sqrt((a * b) / ((a + b) ** 2 * (a + b + 1)))

    # Convert the rating back to a scale of 1-5
    mu = mu * 5
    std_err = std_err * 5
    rating_adjusted = mu - std_err

    return rating_adjusted


# Load and pre-compute adjusted ratings
if 'df' not in st.session_state:
    st.session_state['df'] = pd.read_json('data/yelp.json', lines=True)
    st.session_state['df']['adjusted_rating'] = st.session_state['df'][['review_count', 'stars']].apply(lambda x: rate(*x), axis=1)
    st.session_state['df'] = st.session_state['df'][['adjusted_rating', 'stars', 'name', 'address', 'city', 'state',
                                                     'postal_code', 'latitude', 'longitude', 'review_count', 'is_open',
                                                     'categories', 'hours']]
    st.session_state['states'] = st.session_state['df']['state'].unique()


# A box to select the state
state = st.sidebar.selectbox('Choose a state and I will rank their restaurants for you',
                             st.session_state['states'])

# Filter by state
df_state = st.session_state['df'].query('state == "{}"'.format(state))
df_state = df_state.sort_values('adjusted_rating', ascending=False)
st.write(df_state)
