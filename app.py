"""Demo local tiếng Việt; thuật toán/metrics độc lập trong src."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data import load_paper_data

st.set_page_config(page_title="Phân cụm mờ bán giám sát", page_icon="🔬")
st.title("Phân cụm mờ bán giám sát")
st.caption('Tái hiện bộ 20 điểm • 2 cụm • tọa độ gốc, không chuẩn hóa')
X, reference = load_paper_data()
with st.expander('Dữ liệu và nhóm tham chiếu',expanded=True):
    data=pd.DataFrame(X,columns=['x','y'])
    data.insert(0,'ID điểm',range(1,len(X)+1))
    data['Nhóm tham chiếu']=[f'Nhóm {v+1}' for v in reference]
    data['Điểm chú ý']=['ID 9/10' if i in (9,10) else 'Điểm khác' for i in range(1,21)]
    fig=px.scatter(data,x='x',y='y',color='Nhóm tham chiếu',symbol='Điểm chú ý',
                   hover_data=['ID điểm'],text='ID điểm')
    fig.update_traces(textposition='top center',marker_size=10)
    fig.update_layout(height=430,margin=dict(l=10,r=10,t=25,b=10))
    st.plotly_chart(fig,width='stretch')
    st.dataframe(data.drop(columns='Điểm chú ý'),hide_index=True,width='stretch')
    st.caption('Nhóm tham chiếu chỉ dùng đánh giá; dữ liệu fit chỉ gồm hai tọa độ x, y. ID điểm/cụm hiển thị từ 1.')
