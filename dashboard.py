import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_profiling import ProfileReport
import streamlit.components.v1 as components

st.set_page_config(
    page_title='DS Program Dashboard',
    layout="wide"
    )

@st.cache
def load_clean():
    df = pd.read_csv('ds_program_data - Sheet1.csv')

    df_full = df.fillna(df.mean(numeric_only=True))
    df_rmt = df_full[df_full.type=='RMT']
    df_hck = df_full[df_full.type=='HCK']

    return df_full, df_rmt, df_hck

df_full, df_rmt, df_hck = load_clean()

df_rmt_latest = df_full[
    (df_full.batch == df_full.batch.max()) &
    (df_full.phase == 0) &
    (df_full.type == 'RMT')
]['passing_rate']

df_rmt_before = df_full[
    (df_full.batch == df_full.batch.max()-1) &
    (df_full.phase == 0) &
    (df_full.type == 'RMT')
]['passing_rate']

df_hck_latest = df_full[
    (df_full.batch == df_hck.batch.max()) &
    (df_full.phase == 0) &
    (df_full.type == 'HCK')
]['passing_rate']

df_hck_before = df_full[
    (df_full.batch == df_hck.batch.max()-1) &
    (df_full.phase == 0) &
    (df_full.type == 'HCK')
]['passing_rate']

st.markdown("<h1 style='text-align: center;'>FTDS Program Data</h1>", unsafe_allow_html=True)

with st.expander("Show DS Data"):
    data_option = st.selectbox(
        'Which data do you like to see?',
        ['Full Data', 'HCK', 'RMT'])

    if data_option=='Full Data':
        st.dataframe(df_full, use_container_width=True)
    elif data_option=='HCK':
        st.dataframe(df_hck, use_container_width=True)
    else:
        st.dataframe(df_rmt, use_container_width=True)

col1, col2, col3 = st.columns(3)

col1.metric("All Programs Passing Rate All Time", round(df_full['passing_rate'].mean(), 2))
col2.metric("HCK Passing Rate All Time", round(df_hck['passing_rate'].mean(), 2))
col3.metric("RMT Passing Rate All Time", round(df_rmt['passing_rate'].mean(), 2))

col1, col2, col3 = st.columns(3)
col1.metric("Latest All Programs Passing Rate Prep", (int(df_hck_latest)+int(df_rmt_latest))/2, ((int(df_hck_latest)+int(df_rmt_latest))/2)-((int(df_hck_before)+int(df_rmt_before))/2))
col2.metric("Latest HCK Passing Rate Prep", df_hck_latest, int(df_hck_latest)-int(df_hck_before))
col3.metric("Latest RMT Passing Rate Prep", df_rmt_latest, int(df_rmt_latest)-int(df_rmt_before))

st.markdown('''
<style>
[data-testid="metric-container"] {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] > div {
    width: fit-content;
    margin: auto;
}

[data-testid="metric-container"] label {
    width: fit-content;
    margin: auto;
}

</style>
''', unsafe_allow_html=True)

fig_rmt = px.line(df_rmt, y='passing_rate', x='batch', color='phase', markers=True, symbol='phase', labels={'passing_rate': 'Passing Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='RMT Passing Rate All Time')
fig_rmt.update_layout(yaxis_range=[0, 100])
fig_hck = px.line(df_hck, y='passing_rate', x='batch', color='phase', markers=True, symbol='phase', labels={'passing_rate': 'Passing Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='HCK Passing Rate All Time')
fig_hck.update_layout(yaxis_range=[0, 100])

col1, col2 = st.columns(2)
col1.plotly_chart(fig_rmt, use_container_width=True)
col2.plotly_chart(fig_hck, use_container_width=True)

tab1, tab2, tab3 = st.tabs(["Buddy Evaluation", "Material Evaluation", "Instructor Evaluation"])

fig_rmt_buddy = px.line(df_rmt, y='avg_buddy', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_buddy': 'Buddy Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='RMT Buddy Rate All Time')
fig_rmt_buddy.update_layout(yaxis_range=[0, 10])

fig_hck_buddy = px.line(df_hck, y='avg_buddy', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_buddy': 'Buddy Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='HCK Buddy Rate All Time')
fig_hck_buddy.update_layout(yaxis_range=[0, 10])

with tab1:
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_rmt_buddy, use_container_width=True)
    col2.plotly_chart(fig_hck_buddy, use_container_width=True)

fig_rmt_materials = px.line(df_rmt, y='avg_materials', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_materials': 'Materials Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='RMT Materials Rate All Time')
fig_rmt_materials.update_layout(yaxis_range=[0, 5])

fig_hck_materials = px.line(df_hck, y='avg_materials', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_materials': 'Materials Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='HCK Materials Rate All Time')
fig_hck_materials.update_layout(yaxis_range=[0, 5])

with tab2:
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_rmt_materials, use_container_width=True)
    col2.plotly_chart(fig_hck_materials, use_container_width=True)

fig_rmt_instructor = px.line(df_rmt, y='avg_instructor', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_instructor': 'Instructor Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='RMT Instructor Rate All Time')
fig_rmt_instructor.update_layout(yaxis_range=[0, 5])

fig_hck_instructor = px.line(df_hck, y='avg_instructor', x='batch', color='phase', markers=True, symbol='phase', labels={'avg_instructor': 'Instructor Rate', 'batch': 'Batch', 'phase': 'Phase'}, title='HCK Instructor Rate All Time')
fig_hck_instructor.update_layout(yaxis_range=[0, 5])

with tab3:
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_rmt_instructor, use_container_width=True)
    col2.plotly_chart(fig_hck_instructor, use_container_width=True)

@st.cache
def profiling_data():
    profile = ProfileReport(df_full,
        title="DS Data Profiling Report",
        missing_diagrams={
            "bar": False, 
            "matrix": False
        },
        correlations={
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False}
        },
        interactions={
            "target":['passing_rate', 'avg_buddy', 'avg_materials', 'avg_instructor']
        }
        ).to_html()
    return profile

components.html(profiling_data(), height=1000, scrolling=True)