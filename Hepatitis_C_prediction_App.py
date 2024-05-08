import numpy as np
import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

from pandas import DataFrame



st.markdown("""
<style>
.css-q16mip.e3g6aar0
{
  visibility:hidden;
}
</style>
""", unsafe_allow_html=True)

#st.write(spread.url)
#@st.cache_data(ttl=600)



def change_label_style(label, font_size='20px', font_color='black', font_family='sans-serif'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)




# Load our mnodel
model_load = pickle.load(open('my_model_XGBoost_hepatitisC_new.sav', 'rb'))
X_train = pd.read_csv('X_train.csv')

scaler = StandardScaler()
# Identify numeric columns
numeric_cols = X_train.select_dtypes(include=np.number).columns
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])

# Define a prediction function

def prediction_model(input_data):
    
    input_data_as_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_array.reshape(1,-1)

    prediction = model_load.predict(input_data_reshaped)

    if prediction[0] == 0:
        return "0=Blood Donor", "The patient is a 0=Blood Donor"
    elif prediction[0] == 1:
        return "0s=Suspect Blood Donor" ,"The patient is a 0s=Suspect Blood Donor"
    elif prediction[0] == 2:
        return "1=Hepatitis", "The patient has 1=Hepatitis"
    elif prediction[0] == 3:
        return "2=Fibrosis" ,"The patient has 2=Fibrosis"
    elif prediction[0] == 4:
        return "3=Cirrhosis" ,"The patient has 3=Cirrhosis"


def main():

    # Give a title to the App
    st.title('Hepatitis C prediction App')

    # label = "My text here"
    #      st.text_input(label)
    #      change_label_style(label, '20px')     
    # Getting the Input from the user
    Age = st.text_input(r"$\textsf{\Large Age of the patient(in years)}$")
    #change_label_style('Age of the patient(in years)', '20px') 
    Sex = st.text_input(r"$\textsf{\Large Sex of the patient( either f(for female)/m(for male))}$" )
    ALB = st.text_input(r"$\textsf{\Large ALB(Albumin) value}$")
    ALP = st.text_input(r"$\textsf{\Large ALP(Alkaline Phosphatase) value}$")
    ALT = st.text_input(r"$\textsf{\Large ALT(ALamine aminotransferase) value}$")
    AST = st.text_input(r"$\textsf{\Large AST(ASparate aminotransferase) value}$")
    BIL = st.text_input(r"$\textsf{\Large BIL(Bilirubin) value}$")
    CHE = st.text_input(r"$\textsf{\Large CHE Value}$")
    CHOL = st.text_input(r"$\textsf{\Large CHOL(CHOlesterol) Value}$")
    CREA = st.text_input(r"$\textsf{\Large CREA(CREAtinine) Value}$")
    GGT = st.text_input(r"$\textsf{\Large GGT(Gamma-Glutamyl Transferase) Value}$")
    PROT = st.text_input(r"$\textsf{\Large PROT Value}$")
    
    

    data = {
    'Age': [Age],
    'Sex': [Sex],
    'ALB': [ALB],
    'ALP': [ALP],
    'ALT': [ALT],
    'AST': [AST],
    'BIL': [BIL],
    'CHE': [CHE],
    'CHOL': [CHOL],
    'CREA': [CREA],
    'GGT': [GGT],
    'PROT': [PROT]
     }

    df_ = pd.DataFrame(data)
    df_.loc[df_["Sex"] == "m", "Sex"] = "1"
    df_.loc[df_["Sex"] == "f", "Sex"] = "0"

    col_names = df_.columns
    
    df_ = df_.apply(pd.to_numeric, errors='coerce')

    df_[numeric_cols] = scaler.transform(df_[numeric_cols])
    df_s = pd.DataFrame(df_, columns=col_names)

    opt_df = pd.DataFrame(data)
    opt_df['target'] = " "
    
 
    

    # variable of prediction

    result = ''

    if st.button('Hepatitis C test result'):
        label, result = prediction_model(df_)
        

    # Display the result
    st.success(result)

if __name__ == '__main__':
    main()
