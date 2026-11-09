"""Hiển thị snapshot đã lưu; không gọi fit khi thay vòng xem."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.metrics import supervision_mask


def render_snapshot(experiment, names, revision):
    name=st.selectbox('Kết quả đang xem',list(experiment.results),format_func=names.get,key='result_algorithm')
    result=experiment.results[name]
    iteration=st.slider('Vòng lặp',0,result.n_iter,value=result.n_iter,key=f'iteration_{revision}_{name}')
    snap=result.history[iteration]
    st.caption(f'Vòng {iteration}/{result.n_iter} • U tính từ đúng tâm đang hiển thị • trạng thái dừng: {result.stop_reason}')
    frame=pd.DataFrame(experiment.X,columns=['x','y'])
    frame['ID điểm']=np.arange(1,len(frame)+1)
    frame['Cụm']=[str(v+1) for v in snap.membership.argmax(axis=1)]
    fig=px.scatter(frame,x='x',y='y',color='Cụm',text='ID điểm',hover_data=['ID điểm'],
                   color_discrete_map={'1':'#2563eb','2':'#ea580c'})
    fig.update_traces(textposition='top center',marker_size=10)
    fig.add_trace(go.Scatter(x=snap.centers[:,0],y=snap.centers[:,1],mode='markers+text',
                            marker=dict(symbol='x',size=18,color='black'),
                            text=[f'Tâm {k+1}' for k in range(len(snap.centers))],textposition='top center',name='Tâm'))
    supervised=supervision_mask(name,len(frame),experiment.B,experiment.targets)
    if supervised.any():
        fig.add_trace(go.Scatter(x=experiment.X[supervised,0],y=experiment.X[supervised,1],mode='markers',
                                marker=dict(symbol='diamond-open',size=22,color='black'),name='Có giám sát'))
    fig.update_layout(height=460,margin=dict(l=10,r=10,t=25,b=10))
    st.plotly_chart(fig,width='stretch',key=f'result_plot_{name}')
    membership=pd.DataFrame(snap.membership,columns=[f'U{k+1}' for k in range(snap.membership.shape[1])])
    membership.insert(0,'ID điểm',np.arange(1,len(frame)+1))
    membership['Cụm cứng']=snap.membership.argmax(axis=1)+1
    st.dataframe(membership,hide_index=True,width='stretch',key='membership_table')
    centers=pd.DataFrame(snap.centers,columns=['x','y'])
    centers.insert(0,'Cụm',range(1,len(centers)+1))
    st.dataframe(centers,hide_index=True,width='stretch',key='centers_table')
    st.metric('J của vòng đang xem',f'{snap.objective:.8g}')
    st.caption('J chỉ theo dõi hội tụ của thuật toán này. Vòng 0 dùng tâm khởi tạo; hòa nhãn cứng chọn cụm ID nhỏ nhất.')
    history=pd.DataFrame([dict(Vòng=s.iteration,J=s.objective,Dịch_chuyển_tâm=s.center_shift) for s in result.history]).set_index('Vòng')
    left,right=st.columns(2)
    with left:
        st.caption('Hàm mục tiêu J')
        st.line_chart(history[['J']])
    with right:
        st.caption('Dịch chuyển tâm lớn nhất (Euclid)')
        st.line_chart(history[['Dịch_chuyển_tâm']])
    return name
