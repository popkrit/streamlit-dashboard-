import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Page Config
st.set_page_config(page_title="RMUTP Student Information Dashboard", layout="wide")

# --- ข้อ 2. คำนวณและบันทึกลง sciRMUTP_output.csv ---
if os.path.exists('sciRMUTP.csv'):
    df = pd.read_csv('sciRMUTP.csv')
    
    # คำนวณคอลัมน์ใหม่
    df['total'] = df['male'] + df['female']
    total_all = df['total'].sum()
    df['malePer'] = (df['male'] / total_all) * 100
    df['femalePer'] = (df['female'] / total_all) * 100
    
    # บันทึกลง sciRMUTP_output.csv
    df.to_csv('sciRMUTP_output.csv', index=False, encoding='utf-8-sig')
else:
    st.error("ไม่พบไฟล์ sciRMUTP.csv กรุณารันข้อ 1 เพื่อบันทึกข้อมูลก่อน")
    st.stop()

# --- ข้อมูลสถิติรวม ---
total_male = df['male'].sum()
total_female = df['female'].sum()
total_students = df['total'].sum()
male_percent = (total_male / total_students) * 100
female_percent = (total_female / total_students) * 100
num_curriculum = len(df)

# --- ข้อ 3. สร้าง Streamlit Dashboard ---
st.title("🎓 RMUTP Student Information Dashboard")
st.subheader("ข้อมูลนักศึกษาคณะวิทยาศาสตร์และเทคโนโลยี")

st.markdown("---")

# 1. การ์ดตัวเลขสรุป
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="นักศึกษาทั้งหมด", value=f"{total_students:,} คน")

with col2:
    st.metric(label="นักศึกษาชาย", value=f"{total_male:,} คน", delta=f"{male_percent:.2f}%")

with col3:
    st.metric(label="นักศึกษาหญิง", value=f"{total_female:,} คน", delta=f"{female_percent:.2f}%")

with col4:
    st.metric(label="จำนวนหลักสูตร", value=f"{num_curriculum} หลักสูตร")

st.markdown("---")

# 2. ส่วนแสดงสัดส่วนเพศ (Donut Chart)
st.subheader("⭕ สัดส่วนเพศของนักศึกษา")

col_chart, col_summary = st.columns([1.5, 1])

with col_chart:
    st.caption("สัดส่วนเพศนักศึกษาทั้งหมด")
    gender_df = pd.DataFrame({
        'Gender': ['ชาย', 'หญิง'],
        'Count': [total_male, total_female]
    })
    
    # สร้าง Donut Chart ด้วย Plotly
    fig = px.pie(
        gender_df, 
        values='Count', 
        names='Gender', 
        hole=0.6,
        color='Gender',
        color_discrete_map={'ชาย': '#1f77b4', 'หญิง': '#e377c2'}
    )
    fig.update_traces(textposition='inside', textinfo='percent')
    fig.update_layout(showlegend=True, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)

with col_summary:
    st.markdown("### *สรุปสัดส่วนเพศ*")
    st.caption("สัดส่วนนักศึกษาชาย")
    st.markdown(f"## *{male_percent:.2f}%*")
    st.caption("สัดส่วนนักศึกษาหญิง")
    st.markdown(f"## *{female_percent:.2f}%*")

st.markdown("---")

# 3. สรุปหลักสูตรสูงสุด/ต่ำสุด
st.subheader("🏆 หลักสูตรที่มีจำนวนนักศึกษาสูงสุดและต่ำสุด")

max_total_row = df.loc[df['total'].idxmax()]
min_total_row = df.loc[df['total'].idxmin()]

c1, c2 = st.columns(2)
with c1:
    st.warning(f"**นักศึกษามากที่สุด**\n\n### {max_total_row['curriculum']}\n{max_total_row['total']} คน")

with c2:
    st.warning(f"**นักศึกษาน้อยที่สุด**\n\n### {min_total_row['curriculum']}\n{min_total_row['total']} คน")

# 4. สรุปชาย/หญิงมากที่สุด
st.subheader("🧢 หลักสูตรที่มีนักศึกษาชายและหญิงมากที่สุด")

max_male_row = df.loc[df['male'].idxmax()]
max_female_row = df.loc[df['female'].idxmax()]

c3, c4 = st.columns(2)
with c3:
    st.info(f"**นักศึกษาชายมากที่สุด**\n\n### {max_male_row['curriculum']}\n{max_male_row['male']} คน")

with c4:
    st.info(f"**นักศึกษาหญิงมากที่สุด**\n\n### {max_female_row['curriculum']}\n{max_female_row['female']} คน")

st.caption("*ส่วนแสดงผลรายงานและสรุปผลเกิดจากการคำนวณด้วยโปรแกรม หรือใช้คำสั่งทางสถิติพื้นฐานเท่านั้น*")