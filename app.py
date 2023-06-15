import streamlit as st
import pickle
import pandas as pd

teams = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Kolkata Knight Riders',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad',
]
cities = [
    'Ahmedabad', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai', 'Sharjah',
       'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad', 'Visakhapatnam',
       'Chandigarh', 'Bengaluru', 'Kolkata', 'Jaipur', 'Indore',
       'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
       'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
       'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town'
]
choices = [
    '1st Innings',
    '2nd Innings'
]

st.title('IPL Match Predictor')
choice = st.selectbox('Select Current Innings', choices)

def score_prediction():
    st.title('Score Predictor')
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select Batting Team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select Bowling Team', sorted(teams), index=3)
    selected_cities = st.selectbox('Select Host City', sorted(cities), index=21)
    col3, col4, col5 = st.columns(3)
    with col3:
        current_score_1 = st.number_input('Current Score',min_value=0.0,max_value=300.0,value=0.0,step=1.0)
    with col4:
        overs_1 = st.number_input('Overs Completed (Over > 5)',min_value=5.0,max_value=19.0,value=5.0,step=1.0)
    with col5:
        wickets_1 = st.number_input('Wickets Down',min_value=0.0,max_value=9.0,value=0.0,step=1.0)
    col6, col7= st.columns(2)
    with col6:
        last_five_runs = st.number_input('Run Scored in Last 5 Overs',min_value=0.0,max_value=120.0,value=0.0,step=1.0)
    with col7:
        last_five_wickets = st.number_input('Wickets Down in Last 5 Overs',min_value=0.0,max_value=9.0,value=0.0,step=1.0)

    if st.button('Predict Score'):
        balls_left = 120 - (overs_1 * 6)
        wickets_left = 10 - wickets_1
        crr = current_score_1 / overs_1
        input_df = pd.DataFrame({'BattingTeam':[batting_team], 'BowlingTeam':[bowling_team], 'City':[selected_cities], 'current_score':[current_score_1], 'balls_left':[balls_left], 'wickets_left':[wickets_left], 'crr':[crr], 'last_five_runs':[last_five_runs], 'last_five_wickets':[last_five_wickets]})
        pipe = pickle.load(open('score_pred.pkl','rb'))
        result = pipe.predict(input_df)
        st.header('Projected Score' + ' - ' + str(int(result[0])))

def win_prediction():
    st.title('Win Predictor')
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select Batting Team', sorted(teams), index=3)
    with col2:
        bowling_team = st.selectbox('Select Bowling Team', sorted(teams))
    selected_cities = st.selectbox('Select Host City', sorted(cities), index=21)
    target = st.number_input('Target',min_value=1.0,max_value=300.0,value=1.0,step=1.0)
    col3, col4, col5 = st.columns(3)
    with col3:
        current_score_2 = st.number_input('Current Score',min_value=0.0,max_value=300.0,value=0.0,step=1.0)
    with col4:
        overs_2 = st.number_input('Overs Completed',min_value=1.0,max_value=300.0,value=1.0,step=1.0)
    with col5:
        wickets_2 = st.number_input('Wickets Down',min_value=0.0,max_value=9.0,value=0.0,step=1.0)

    if st.button('Predict Score'):
        runs_left = target - current_score_2
        balls_left = 120 - (overs_2 * 6)
        wickets_left = 10 - wickets_2
        crr = current_score_2 / overs_2
        rrr = (runs_left / balls_left) * 6
        input_df = pd.DataFrame({'BattingTeam':[batting_team], 'BowlingTeam':[bowling_team], 'City':[selected_cities], 'runs_left':[runs_left], 'balls_left':[balls_left], 'wickets_left':[wickets_left], 'target':[target], 'crr':[crr], 'rrr':[rrr]})
        pipe = pickle.load(open('win_pred.pkl','rb'))
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + ' - ' + str(round(win * 100)) + '%')
        st.header(bowling_team + ' - ' + str(round(loss * 100)) + '%')

if choice == choices[0]:
    score_prediction()

elif choice == choices[1]:
    win_prediction()