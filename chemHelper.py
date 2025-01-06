import pandas as pd
import streamlit as st
import requests

url = "https://datasets-server.huggingface.co/rows?dataset=camel-ai%2Fchemistry&config=default&split=train&offset=0&length=100"

response = requests.get(url)
data = response.json()

df = pd.json_normalize(data['rows']) 
df.to_csv("chemistry_rows.csv", index=False)

def find_focus(df):
    
      topics = ['']
      for topic in df['row.topic;'].unique():
          if topic not in topics:
              topics.append(topic)
      focus = st.selectbox("Select a Chemistry topic to focus: ", (topics))
      if focus != '':
        st.write("Loading questions on " + focus + " . . .")
      df = df[df['row.topic;'] == focus]
      return focus, df

focus, df = find_focus(df)


def aptitude(focus, df):
    
    questions = []
    answers = []
    key = []
    grades = []
    topics = []
    st.header(focus + " Aptitude Test")
    
    
    for topic in df['row.sub_topic'].unique():
        filtered_df = df[df['row.sub_topic'] == topic]

        topics.append(topic)

        question = filtered_df.iloc[0]['row.message_1']
        questions.append(question)       

        right_answer = filtered_df.iloc[0]['row.message_2']
        key.append(right_answer)

        st.write(question)
        answer = st.text_input("Answer:", key=f"{topic}_question_{0}")
        answers.append(answer)
        

    

    if len(topics) == len(questions) == len(answers) == len(key):
      nums = []
      for i in range(1, len(topics) + 1):
          nums.append(i)
      table_data = pd.DataFrame({
      "Question Number": nums,
      "Your Answer": answers,
      "Solution": key,
      
      })

    st.header("Grade your answers")

    st.table(table_data)
    for i in range(len(answers)):
        grade = st.selectbox(f"My answer for Question # {i + 1} was: ", ('', 'Right', 'Wrong'), key=f"selectbox_{i}")
        if grade == "Right":
            grade = 1
        elif grade == "Wrong":
            grade = 0
        grades.append(grade)
     
    return grades, topics

grades, topics = aptitude(focus, df)

def analyze(grades, topics):
    weak_topics = [""]
    st.header("Here are your weak topics: ")
    for i in range(len(grades)):
       if grades[i] == 0:
          weak_topics.append(topics[i])
    st.session_state == "practice"
    

    practice_topic = st.selectbox("Select a topic to practice: ", (weak_topics))


    st.header("Practicing " + practice_topic + " . . .")
    proficiency = 0

    filtered_df = df[df['row.sub_topic'] == practice_topic]
    for i in range(5):
        st.write(filtered_df.iloc[i]['row.message_1'])  
        answer = st.text_input("Answer: ")
        if answer != "":
            right_answer = filtered_df.iloc[i]['row.message_2']
            st.write("Right Answer: ")
            st.write(right_answer)
            grade = st.selectbox("Grade: ", ('Right', 'Wrong'))
            if grade == "Right":
                proficiency += 1

    if proficiency <= 2:
        st.write("Looks like you need some more practice here . . .")
        st.write("Check our these resources for further help: ")
