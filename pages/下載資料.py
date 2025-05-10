

import pandas as pd
import streamlit as st
from datetime import datetime


@st.cache_data
def get_data(path):
    data = pd.read_csv(path, index_col=0)
    return data



@st.cache_data
def convert_for_download(data):
    return data.to_csv().encode("utf-8")



# Page Config
st.set_page_config(page_title='下載資料',  layout='wide')
container1 = st.container(border=True)
input_a1, input_a2 = container1.columns((1, 1))


# Data
path = "./Data/FinalData.csv"
df = get_data(path)
df["DATETIME"] = pd.to_datetime(df["DATETIME"])
df["DATESTR"] = pd.to_datetime(df["DATETIME"]).dt.strftime("%Y-%m-%d")
df = df.groupby('DATESTR').tail(1)



# Download Button
datestr_tuple = tuple(df["DATESTR"].unique())
Start_Date_str = datestr_tuple[0]
End_Date_str = datestr_tuple[-1]
option_start_date = input_a1.selectbox(
    "起始日期：",
    datestr_tuple,
)
option_end_date = input_a2.selectbox(
    "結束日期：",
    datestr_tuple,
)

Start_Date_val = datetime.strptime(option_start_date, "%Y-%m-%d")
End_Date_val = datetime.strptime(option_end_date, "%Y-%m-%d")
with st.spinner("讀取中..."):
    try:
        if End_Date_val >= Start_Date_val:
            container2 = st.container(border=True)
            input_b1, input_b2, input_b3 = container2.columns((1, 10, 1), vertical_alignment="center")

            temp_df = df.set_index("DATETIME").loc[option_start_date:option_end_date].copy()
            temp_df = temp_df.set_index("DATESTR")[["SS", "PH", "ORP"]].copy()
            input_b2.dataframe(temp_df)

            container3 = st.container(border=True)
            input_c1, input_c2, input_c3 = container3.columns((1, 10, 1), vertical_alignment="center")
            csv = convert_for_download(temp_df)
            input_c2.download_button(
                label="下載資料",
                data=csv,
                file_name="data.csv",
                mime="text/csv",
            )

        else:
            st.text("日期設定錯誤")

    except:
        st.text("日期設定錯誤")


