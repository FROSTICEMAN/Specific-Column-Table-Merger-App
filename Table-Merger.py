import streamlit as st
import pandas as pd
import regex as re
import io
import openpyxl as op
import numpy as np


# Hide burger menu, maximize width
st.markdown(
    """<style>
    #MainMenu {visibility: hidden;}
    .reportview-container .main .block-container {max-width: 100%}
    </style>""",
    unsafe_allow_html=True,
)

st.title("Table - Merger")
st.subheader("App for Merging Data of Files having similar columns (Specific)")
st.write("Built by Mr.FROSTICEMAN")


upload_file1 = st.file_uploader("Upload Excel File1 for Merging eg.(X1) ")
upload_file2 = st.file_uploader("Upload Excel File2 for Merging with File1 eg.(X2) ")

if upload_file1:
    df1 = pd.read_excel(upload_file1)
    df1 = df1.astype(str)
    column_names1 = df1.columns.tolist()
    listA = [a for a in column_names1 if not re.search('(?:Invention |invention |INVENTION )', a)] ## Incase Specific column merging X1
    df3 = df1.set_index(listA).apply(lambda x: x.str.split(';').explode()).reset_index()
    listD = [a for a in column_names1 if  re.search('(?:Invention |invention |INVENTION )', a)] ## Incase Specific column merging X1
    result1 = listD[:len(listD)//2]
    df3[result1] = df3[result1].astype(str).astype(int)
    #st.text(df3.dtypes)
    #st.dataframe(df3)
    column_names1 = df1.columns.tolist()
    #st.text(column_names1)

if upload_file2:
    df2 = pd.read_excel(upload_file2)
    df2 = df2.astype(str)
    column_names2 = df2.columns.tolist()
    #st.text(column_names2)
    listB = [a for a in column_names2 if not re.search('(?:Invention |invention |INVENTION )', a)]## Incase Specific column merging X2
    df4 = df2.set_index(listB).apply(lambda x: x.str.split(';').explode()).reset_index()
    listE = [a for a in column_names2 if  re.search('(?:Invention |invention |INVENTION )', a)]## Incase Specific column merging X2
    #st.text(listE)
    result1 = listE[:len(listE)//2]
    result2 = listE[len(listE)//2:]
    df4[result1] = df4[result1].astype(str).astype(int)
    #st.text(df4.dtypes)
    #st.dataframe(df4)
    common_list = set(column_names1).intersection(column_names2)   
    merging_parameter = st.selectbox("Select the Merging Column",common_list)
    #st.text(merging_parameter)
    df_combine = df3[column_names1].concat(df4[column_names2], 
                                     on = merging_parameter,how = "left")
    column_names3 = df_combine.columns.tolist()
    res = list(set(column_names3)^set(column_names1))
    res2 = list(set(res)^set(column_names2))
    drop_x = [a for a in res2 if  re.search('_y', a)]
    df_comb = df_combine.drop(drop_x,axis=1)


    #st.text(column_names3)                                 
    st.dataframe(df_comb)      

    #write Excel with all parameters:
    buffer = io.BytesIO()
    df_xlsx = df_comb
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
     df_xlsx.to_excel(writer, sheet_name='Sheet1')
    
    # Close the Pandas Excel writer and output the Excel file to the buffer
     writer.save()

    st.download_button(
        label=" 📥 Download Excel worksheet",
        data=buffer,
        file_name="Table - Merger App Output.xlsx",
        mime="application/vnd.ms-excel"
    )                          
