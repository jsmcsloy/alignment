import pandas as pd
from pandas import DataFrame, read_csv
import streamlit as st
import altair as  alt
from altair import Chart, X, Y
import matplotlib.pyplot as plt
from datetime import date
import base64

#get stored limits
#changed to hard coded limits except 25°

# create side bar
st.sidebar.subheader("Variables")
location = st.sidebar.selectbox("Location", ['Stowmarket', 'Milan', 'Cleveland', 'KL', 'Shouzo'])
week = st.sidebar.number_input("Enter week: ",min_value = 1, max_value = 52, step = 1)

#low = st.sidebar.slider("Low limit:",0.01,100.00)         #sliders not used moved to hardcoded
#high = st.sidebar.slider("High limit: ",0.00, 100.00)     #sliders not used moved to hardcoded

col1 , col2 = st.sidebar.beta_columns(2)
with col1:
        angle = st.selectbox("Select angle", ['25°','45°','75°'])
with col2:
        gun = st.selectbox("Gun: ", [1,2,3,4,5,'Automation'])

#text area currently not in use
#data_in = st.sidebar.text_area("Paste in Data")
#st.sidebar.text_area("Paste in Data")
l_value = st.sidebar.number_input("Enter the L Value: ")
insert = st.sidebar.button("Insert")



# MAIN APP SCREEN

st.title("Alignment")
st.text("Mouse over the point for more information. High/Low limits can be set in the menu.")


#df = pd.DataFrame(columns =["week", "gun", "angle", "lab", "L_value", "location", "date"])  # used to setup initial df
df = pd.read_pickle("lab_df.pk1") #load the saved DataFrame in

today = date.today()


# shortern pasted in  data - currently fails on different length strings
try:
        pass
        if insert == True:
            d = data_in
            grid_list = d.replace(" ", "")
            grid_list = grid_list[-37:]
            print(grid_list)
            mlist = ['0','1','2','3','4','5','6','7','8','9','.'] #remove all non numerical string data
            lv = ''.join(c for c in grid_list if c in mlist)
            lv = lv[:5]
            

except:
        pass


# pretty graph
# Every thing displayed
#st.subheader("All angles displayed")
#chart = alt.Chart(df).mark_point().encode(x='week', y='L_value',tooltip = ['week', 'location', 'gun', 'L_value', 'angle']
# )
#line = alt.Chart(pd.DataFrame({'L_value': [low]})).mark_rule().encode(y='L_value')
#line2 = alt.Chart(pd.DataFrame({'L_value': [high]})).mark_rule().encode(y='L_value')

#st.write(chart +line +line2)



# Define the logic for the button. Inserts row to DataFrame using this until shortern string is working. Remove once happy

if insert == True:
        d ={"week":week, "gun":gun, "angle":angle, "lab":"", "L_value": l_value, "location": location, "date": today}
        df = df.append(d, ignore_index = True)
        df.to_pickle("lab_df.pk1") # save dataframe
        

#draw control charts

st.subheader("25° Angle")
a_25 = pd.DataFrame(df.loc[df['angle'] == "25°"])

chartb = alt.Chart(a_25).mark_point().encode(x='week' , y='L_value',tooltip = ['week', 'location', 'gun', 'L_value', 'angle'], color='location') #main chart
lineb = alt.Chart(pd.DataFrame({'L_value': [54.67]})).mark_rule().encode(y='L_value') # sets lower control line
line2b = alt.Chart(pd.DataFrame({'L_value': [59.7]})).mark_rule().encode(y='L_value') # sets upper control line

st.write(chartb +lineb +line2b)

st.subheader("45° Angle")
a_45 = pd.DataFrame(df.loc[df['angle'] == "45°"])

chartc = alt.Chart(a_45).mark_point().encode(x='week', y='L_value',tooltip = ['week', 'location', 'gun', 'L_value', 'angle'], color='location')  #main chart
linec = alt.Chart(pd.DataFrame({'L_value': [13.89]})).mark_rule().encode(y='L_value') # sets lower control line
line2c = alt.Chart(pd.DataFrame({'L_value': [21.5]})).mark_rule().encode(y='L_value') # sets upper control line

st.write(chartc +linec +line2c)

st.subheader("75° Angle")
a_75 = pd.DataFrame(df.loc[df['angle'] == "75°"])

chartd = alt.Chart(a_75).mark_point().encode(x='week', y='L_value',tooltip = ['week', 'location', 'gun', 'L_value', 'angle'], color='location')  #main chart
lined = alt.Chart(pd.DataFrame({'L_value': [22.3]})).mark_rule().encode(y='L_value')   # sets lower control line
line2d = alt.Chart(pd.DataFrame({'L_value': [25.6]})).mark_rule().encode(y='L_value') # sets upper control line

st.write(chartd +lined +line2d)


def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


# Examples
#df = pd.DataFrame({'x': list(range(10)), 'y': list(range(10))})
#st.write(df)

if st.button('Download Dataframe as CSV'):
    tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)






#s = st.text_input('Enter text here')
#st.write(s)

#if st.button('Download input as a text file'):
 #   tmp_download_link = download_link(s, 'YOUR_INPUT.txt', 'Click here to download your text!')
#    st.markdown(tmp_download_link, unsafe_allow_html=True)
            

