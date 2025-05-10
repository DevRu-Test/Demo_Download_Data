

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime


@st.cache_data
def get_data(path):
    data = pd.read_csv(path, index_col=0)
    return data



@st.cache_data
def convert_for_download(data):
    return data.to_csv().encode("utf-8")



def plotly_line(DF, Col, Title):
    scatter = go.Scatter(x=DF.index, y=DF[Col])
    fig = go.Figure(scatter)
    fig.update_layout(
        title=Title,
        hovermode="x unified",
        xaxis=dict(type = "category", title="日期"),
        yaxis=dict(title=Col)
    )
    return fig



def stats_output(DF, Col):
    stats_dict = {
        "近3日平均數" : DF[Col].tail(3).mean(),
        "近5日平均數" : DF[Col].tail(5).mean(),
        "近15日平均數" : DF[Col].tail(15).mean(),
        "近30日平均數" : DF[Col].mean(),
        "近30日標準差" : DF[Col].std(),
        "近30日變異數" : DF[Col].var(),
        "第一四分位數 (Q1)" : DF[Col].quantile(0.25),
        "第三四分位數 (Q3)" : DF[Col].quantile(0.75),
    }
    stats_df = pd.DataFrame([stats_dict], index=[Col]).T
    return stats_df



# Page Config
st.set_page_config(page_title='資料監測',  layout='wide')
col_dict = {
    "SS": "懸浮固體係數 Suspended Solids (SS)",
    "PH": "酸鹼值 Potential of Hydrogen (PH)",
    "ORP": "氧化還原 Oxidation Reduction Potential (ORP)",
}


# Switch Button
on = st.toggle("系統啟動")
if on:
    # Container 1
    container1 = st.container(border=True)
    container2 = st.container(border=True)
    container3 = st.container(border=True)
    input_a1, input_a2, input_a3 = container1.columns((1, 8, 2), vertical_alignment="center")
    input_b1, input_b2, input_b3 = container2.columns((1, 8, 2), vertical_alignment="center")
    input_c1, input_c2, input_c3 = container3.columns((1, 8, 2), vertical_alignment="center")
    


    # Data
    path = "../Data/FinalData/FinalData.csv"
    df = get_data(path)
    df["DATETIME"] = pd.to_datetime(df["DATETIME"])
    df["DATESTR"] = pd.to_datetime(df["DATETIME"]).dt.strftime("%Y-%m-%d")
    temp_df = df.groupby('DATESTR').tail(1).copy()
    temp_df = temp_df.set_index("DATESTR")[["SS", "PH", "ORP"]].tail(30)



    # Plotly
    for i_col, col in enumerate(temp_df.columns):
        col_title = col_dict[col]
        fig = plotly_line(temp_df, col, col_title)
        stats_df = stats_output(temp_df, col)
        
        if i_col == 0:
            input_a2.plotly_chart(fig, theme="streamlit", use_container_width=True)
            input_a3.dataframe(stats_df)
    
        if i_col == 1:
            input_b2.plotly_chart(fig, theme="streamlit", use_container_width=True)
            input_b3.dataframe(stats_df)

        if i_col == 2:
            input_c2.plotly_chart(fig, theme="streamlit", use_container_width=True)
            input_c3.dataframe(stats_df)

    # input_a2.dataframe(temp_df)


    




