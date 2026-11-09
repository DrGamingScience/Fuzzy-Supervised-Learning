"""Demo local tiếng Việt; thuật toán/metrics độc lập trong src."""

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

from src.data import load_paper_data, demo_initial_centers
from src.algorithms import Config
from src.experiments import supervision_from_rows, run_experiment
from src.ui import render_snapshot

st.set_page_config(page_title="Phân cụm mờ bán giám sát", page_icon="🔬")
st.title("Phân cụm mờ bán giám sát")
st.caption('Tái hiện bộ 20 điểm • 2 cụm • tọa độ gốc, không chuẩn hóa')
X, reference = load_paper_data()

NAMES={'fcm':'FCM', 'ssfcm':'sSFCM (m > 1)', 'ssfcm1':'sSFCM (m = 1)',
       'esfcm':'eSFCM', 'ssmc':'sSMC-FCM'}
with st.sidebar:
    st.header('Thiết lập')
    algorithm=st.selectbox('Thuật toán',list(NAMES),format_func=NAMES.get,key='algorithm')
    m=2.0; mp=4.0; lam=1.0
    if algorithm in ('fcm','ssfcm','ssmc'):
        m=st.number_input('m / M',min_value=1.000001,value=2.0,step=0.1,key='m')
    if algorithm=='ssfcm1':
        m=1.0
        st.caption('m = 1: phần dư vào cụm gần nhất; hòa chọn cụm ID nhỏ nhất.')
    if algorithm in ('ssfcm','ssfcm1','esfcm'):
        st.selectbox('Preset B cho ID 9, 10 → cụm 1',[0.0,0.3,0.6],index=1,key='level')
        st.caption('B là cận dưới độ thuộc; B = 0 nghĩa là không có chỉ dẫn ở ô đó.')
    if algorithm=='esfcm':
        lam=st.number_input('lambda',min_value=0.000001,value=1.0,step=0.1,key='lambda')
    if algorithm=='ssmc':
        def apply_mp_preset():
            st.session_state['m_prime']=float(st.session_state['m_prime_preset'])
        st.selectbox('Preset M′',[4.0,8.0],key='m_prime_preset',on_change=apply_mp_preset)
        mp=st.number_input('M′ nhập tay',min_value=1.000001,value=4.0,step=1.0,key='m_prime')
        st.caption('M′ ≥ M; M′ = M thu về FCM. M′ là số mũ ở ô được chỉ dẫn, khác B.')
    epsilon=st.number_input('epsilon (dịch chuyển tâm)',min_value=1e-12,value=1e-7,format='%.8g',key='epsilon')
    max_iter=st.number_input('Giới hạn vòng',min_value=1,max_value=10000,value=500,key='max_iter')
    init_mode=st.selectbox('Khởi tạo',['Tâm demo cố định','Lấy mẫu theo seed'],key='init_mode')
    seed=st.number_input('Seed',min_value=0,max_value=2**32-1,value=42,key='seed')
    st.caption('Tâm demo: (2.7, 5), (9.1, 5), do dự án chọn. Dừng khi max dịch chuyển Euclid của tâm ≤ epsilon.')

config=Config(algorithm=algorithm,m=m,m_prime=mp,lambda_=lam,epsilon=epsilon,max_iter=max_iter,seed=seed)
initial_centers=demo_initial_centers() if init_mode=='Tâm demo cố định' else None
level=st.session_state.get('level',st.session_state.get('prior_level',0.3))

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

st.subheader('Chỉ dẫn giám sát')
st.caption('Mỗi điểm tối đa một dòng bật. ID và cụm đích từ 1. B chỉ áp dụng cho sSFCM/eSFCM; sSMC-FCM dùng cụm đích và M′. FCM bỏ qua bảng này.')
reset=st.button('Khôi phục preset',key='reset_supervision')
if 'supervision_rows' not in st.session_state or st.session_state.get('prior_level')!=level or reset:
    st.session_state['supervision_rows']=pd.DataFrame([
        dict(enabled=True,point_id=i,target_cluster=1,membership=level) for i in (9,10)])
    st.session_state['editor_revision']=st.session_state.get('editor_revision',0)+1
    st.session_state['prior_level']=level
editor_key=f"supervision_editor_{st.session_state['editor_revision']}"
rows=st.data_editor(st.session_state['supervision_rows'],key=editor_key,num_rows='dynamic',
    hide_index=True,width='stretch',disabled=['membership'] if algorithm=='ssmc' else [],
    column_config={
        'enabled':st.column_config.CheckboxColumn('Bật',default=False),
        'point_id':st.column_config.NumberColumn('ID điểm',min_value=1,max_value=20,step=1,required=True),
        'target_cluster':st.column_config.NumberColumn('Cụm đích',min_value=1,max_value=2,step=1,required=True),
        'membership':st.column_config.NumberColumn('B (độ thuộc)',min_value=0.0,max_value=1.0,step=0.1,required=True),
    })
supervision_error=None
B=np.zeros((20,2)); targets=np.full(20,-1,dtype=int)
if algorithm!='fcm':
    try:
        B,targets=supervision_from_rows(rows,20,2,use_membership=algorithm!='ssmc')
    except ValueError as exc:
        supervision_error=str(exc)
        st.error(supervision_error)

if st.button('Chạy thuật toán',type='primary',key='run',disabled=supervision_error is not None):
    try:
        with st.spinner('Đang phân cụm…'):
            experiment=run_experiment(X,[config],initial_centers,B,targets,reference)
        st.session_state['experiment']=experiment
        st.session_state['run_revision']=st.session_state.get('run_revision',0)+1
    except (ValueError,ArithmeticError) as exc:
        st.error(f'Không thể chạy: {exc}')

if 'experiment' in st.session_state:
    st.subheader('Kết quả và diễn biến')
    render_snapshot(st.session_state['experiment'],NAMES,st.session_state['run_revision'])
