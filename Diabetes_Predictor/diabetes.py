import numpy as np
import pandas as pd
import streamlit as st
import pickle 
from sklearn.preprocessing import StandardScaler


loaded_model = pickle.load(open('./trained_model.sav', 'rb'))
scaler = StandardScaler()

def Pred_Diabetes(input_data):
    input_data_as_numpy_array = np.asarray(input_data, dtype=float)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Only use this if scaler was fitted or loaded
    # input_data_reshaped = scaler.transform(input_data_reshaped)

    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        return "The person is not diabetic"
    else:
        return "The person is diabetic"
        
def main():
    st.title('Diabetes Prediction Web App')
    
    
    Pregnancies = st.text_input('Number of Pregnancies')
    Glucose = st.text_input('Number of Glucose')
    BloodPressure = st.text_input('Number of BloodPressure')
    SkinThickness = st.text_input('Number of SkinThickness')
    Insulin = st.text_input('Number of Insulin')
    BMI = st.text_input('Number of BMI')
    DiabetesPedigreeFunction = st.text_input('Number of DiabetesPedigreeFunction')
    Age = st.text_input('Number of Age')
    
    diagnosis = ''
    
    if st.button('Diabetes Test Result'):
        diagnosis = Pred_Diabetes([Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age])
        
    st.success(diagnosis)
    
if __name__ == '__main__':
    main()