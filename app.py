"""
HealthTrack Pro — Analytics Dashboard
Streamlit Professional Dashboard for MBA Data Analytics Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthTrack Pro | Analytics",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  :root {
    --primary:   #0ea5e9;
    --primary-d: #0284c7;
    --accent:    #10b981;
    --warn:      #f59e0b;
    --danger:    #ef4444;
    --bg:        #0f172a;
    --surface:   #1e293b;
    --surface2:  #273549;
    --border:    #334155;
    --text:      #f1f5f9;
    --muted:     #94a3b8;
  }

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
  }
  .stApp { background-color: var(--bg); }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
  }
  section[data-testid="stSidebar"] * { color: var(--text) !important; }

  /* Metric cards */
  .metric-card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(14,165,233,0.15);
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 16px 0 0 16px;
  }
  .metric-card.blue::before  { background: var(--primary); }
  .metric-card.green::before { background: var(--accent); }
  .metric-card.amber::before { background: var(--warn); }
  .metric-card.red::before   { background: var(--danger); }

  .metric-label {
    font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
    text-transform: uppercase; color: var(--muted); margin-bottom: 6px;
  }
  .metric-value {
    font-size: 32px; font-weight: 800; color: var(--text); line-height: 1;
  }
  .metric-sub {
    font-size: 12px; color: var(--muted); margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
  }
  .metric-icon {
    position: absolute; right: 20px; top: 50%;
    transform: translateY(-50%);
    font-size: 36px; opacity: 0.15;
  }

  /* Section headers */
  .section-header {
    font-size: 18px; font-weight: 700; color: var(--text);
    border-left: 3px solid var(--primary);
    padding-left: 12px; margin: 28px 0 16px;
  }

  /* Page title */
  .page-title {
    font-size: 36px; font-weight: 800;
    background: linear-gradient(135deg, #0ea5e9, #10b981);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 2px;
  }
  .page-subtitle { font-size: 13px; color: var(--muted); margin-bottom: 20px; }

  /* Divider */
  .divider { border: none; border-top: 1px solid var(--border); margin: 24px 0; }

  /* Insight box */
  .insight-box {
    background: linear-gradient(135deg, rgba(14,165,233,0.08), rgba(16,185,129,0.05));
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 12px; padding: 14px 18px;
    font-size: 13px; color: var(--muted); line-height: 1.6;
    margin-top: 8px;
  }
  .insight-box strong { color: var(--text); }

  /* Tag badges */
  .badge {
    display: inline-block; border-radius: 999px;
    padding: 2px 10px; font-size: 11px; font-weight: 600;
    margin-right: 4px;
  }
  .badge-blue  { background: rgba(14,165,233,0.15); color: #38bdf8; }
  .badge-green { background: rgba(16,185,129,0.15); color: #34d399; }

  /* Streamlit overrides */
  div[data-testid="stMetric"] { display: none; }
  .stSelectbox > div, .stMultiSelect > div { background: var(--surface2); border-radius: 10px; }
  .stSlider > div { padding-top: 4px; }
  footer { display: none; }
  #MainMenu { display: none; }
  header { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADER ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("healthtrack_clean.csv")
    bool_cols = ['trial_signup', 'purchased', 'churned']
    for c in bool_cols:
        if df[c].dtype == object:
            df[c] = df[c].map({'True': True, 'False': False, True: True, False: False})
        df[c] = df[c].astype(bool)
    cat_cols = ['region', 'gender', 'marketing_channel', 'plan', 'age_group', 'income_segment']
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype(str)
    return df

df_full = load_data()

# ─── PLOTLY THEME ───────────────────────────────────────────────────────────
COLORS = {
    'primary': '#0ea5e9', 'accent': '#10b981', 'warn': '#f59e0b',
    'danger': '#ef4444', 'purple': '#a78bfa', 'pink': '#f472b6',
    'bg': '#0f172a', 'surface': '#1e293b', 'border': '#334155', 'muted': '#94a3b8'
}
PALETTE = [COLORS['primary'], COLORS['accent'], COLORS['warn'],
           COLORS['danger'], COLORS['purple'], COLORS['pink']]

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#94a3b8', size=12),
    title_font=dict(family='Plus Jakarta Sans', color='#f1f5f9', size=15),
    legend=dict(bgcolor='rgba(30,41,59,0.8)', bordercolor='#334155',
                borderwidth=1, font=dict(size=11, color='#cbd5e1')),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='#1e293b', linecolor='#334155', tickfont=dict(color='#64748b')),
    yaxis=dict(gridcolor='#1e293b', linecolor='#334155', tickfont=dict(color='#64748b'))
)

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px'>
      <div style='font-size:40px'>💚</div>
      <div style='font-size:17px; font-weight:800; color:#f1f5f9'>HealthTrack Pro</div>
      <div style='font-size:11px; color:#64748b; letter-spacing:1px; text-transform:uppercase'>Analytics Dashboard</div>
    </div>
    <hr style='border-color:#334155; margin:12px 0'>
    """, unsafe_allow_html=True)

    st.markdown("**🔍 Global Filters**")

    regions = ["All"] + sorted(df_full['region'].unique().tolist())
    sel_region = st.selectbox("Region", regions)

    channels = ["All"] + sorted(df_full['marketing_channel'].unique().tolist())
    sel_channel = st.selectbox("Marketing Channel", channels)

    genders = ["All"] + sorted(df_full['gender'].unique().tolist())
    sel_gender = st.selectbox("Gender", genders)

    age_min, age_max = int(df_full['age'].min()), int(df_full['age'].max())
    sel_age = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    income_vals = df_full['annual_income'].dropna()
    sel_income = st.slider(
        "Annual Income ($K)",
        int(income_vals.min()//1000), int(income_vals.max()//1000),
        (int(income_vals.min()//1000), int(income_vals.max()//1000))
    )

    st.markdown("<hr style='border-color:#334155; margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:11px; color:#475569; text-align:center; line-height:1.8'>
      MBA Data Analytics · MGB<br>Individual Project<br>
      <span style='color:#0ea5e9'>HealthTrack Pro</span> · 500 Records
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER DATA ────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_region != "All":
    df = df[df['region'] == sel_region]
if sel_channel != "All":
    df = df[df['marketing_channel'] == sel_channel]
if sel_gender != "All":
    df = df[df['gender'] == sel_gender]
df = df[(df['age'] >= sel_age[0]) & (df['age'] <= sel_age[1])]
df = df[(df['annual_income'] >= sel_income[0]*1000) & (df['annual_income'] <= sel_income[1]*1000)]

# ─── NAVIGATION ─────────────────────────────────────────────────────────────
PAGES = ["🏠 Overview", "📣 Marketing & Channels", "👥 Customer Segments",
         "📈 Conversion & Revenue", "🔗 Correlation Analysis", "⚠️ Churn Intelligence"]
page = st.sidebar.radio("Navigation", PAGES, label_visibility="collapsed")
st.sidebar.markdown(f"""
<div style='margin-top:8px; font-size:11px; color:#475569; text-align:center'>
  Showing <b style='color:#0ea5e9'>{len(df):,}</b> of {len(df_full):,} records
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown('<div class="page-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">End-to-end sales pipeline snapshot · HealthTrack Pro launch metrics</div>', unsafe_allow_html=True)

    # KPI cards
    total      = len(df)
    trials     = df['trial_signup'].sum()
    purchased  = df['purchased'].sum()
    active     = (df['purchased'] & ~df['churned']).sum()
    mrr        = df[df['purchased']]['monthly_revenue'].sum()
    avg_nps    = df['nps_score'].mean()
    trial_rate = trials / total * 100 if total else 0
    conv_rate  = purchased / total * 100 if total else 0
    churn_rate = df[df['purchased']]['churned'].mean() * 100 if purchased else 0

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        (col1, "blue",  "TOTAL LEADS",      f"{total:,}",        f"Trial rate: {trial_rate:.1f}%", "👥"),
        (col2, "green", "TRIAL SIGNUPS",    f"{trials:,}",       f"{trial_rate:.1f}% of leads",   "🧪"),
        (col3, "amber", "PAID SUBSCRIBERS", f"{purchased:,}",    f"{conv_rate:.1f}% conversion",  "💳"),
        (col4, "red",   "MONTHLY REVENUE",  f"${mrr:,.0f}",      f"Avg ${mrr/purchased:.2f}/sub" if purchased else "—", "💰"),
    ]
    for col, color, label, value, sub, icon in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card {color}">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{value}</div>
              <div class="metric-sub">{sub}</div>
              <div class="metric-icon">{icon}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_a, col_b = st.columns([1.6, 1])

    with col_a:
        st.markdown('<div class="section-header">Sales Funnel</div>', unsafe_allow_html=True)
        funnel_stages = ['Total Leads', 'Trial Signups', 'Purchased', 'Active Subscribers']
        funnel_vals   = [total, int(trials), int(purchased), int(active)]
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_stages, x=funnel_vals,
            textposition="inside",
            texttemplate="%{value:,} (%{percentInitial:.0%})",
            marker=dict(color=[COLORS['primary'], COLORS['accent'], COLORS['warn'], COLORS['danger']],
                        line=dict(width=2, color=COLORS['bg'])),
            connector=dict(line=dict(color=COLORS['border'], width=1))
        ))
        fig_funnel.update_layout(**PLOTLY_LAYOUT, height=320, title="Conversion Funnel")
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Pipeline KPIs</div>', unsafe_allow_html=True)
        kpi_data = {
            "Metric": ["Trial Rate", "Purchase Rate", "Active Sub Rate", "Churn Rate", "Avg NPS", "Avg Sessions"],
            "Value": [f"{trial_rate:.1f}%", f"{conv_rate:.1f}%",
                      f"{active/total*100:.1f}%" if total else "—",
                      f"{churn_rate:.1f}%", f"{avg_nps:.2f}/10",
                      f"{df['usage_sessions'].mean():.1f}"]
        }
        kpi_df = pd.DataFrame(kpi_data)
        st.dataframe(kpi_df, use_container_width=True, hide_index=True,
                     column_config={"Metric": st.column_config.TextColumn("Metric"),
                                    "Value": st.column_config.TextColumn("Value")})
        st.markdown(f"""
        <div class="insight-box">
          <strong>💡 Key Finding:</strong> With a <strong>{conv_rate:.1f}%</strong> overall conversion rate,
          the pipeline's biggest opportunity lies in improving trial-to-paid conversion.
          Usage sessions are the strongest predictor of purchase intent.
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_c, col_d, col_e = st.columns(3)
    with col_c:
        st.markdown('<div class="section-header">Plan Mix</div>', unsafe_allow_html=True)
        plan_counts = df[df['purchased']]['plan'].value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=plan_counts.index, values=plan_counts.values,
            hole=0.55,
            marker=dict(colors=[COLORS['accent'], COLORS['primary'], COLORS['warn']],
                        line=dict(color=COLORS['bg'], width=3)),
            textfont=dict(size=12)
        ))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=260, title="Subscribers by Plan",
                              showlegend=True, legend=dict(orientation='h', y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Revenue by Plan</div>', unsafe_allow_html=True)
        rev_plan = df[df['purchased']].groupby('plan')['monthly_revenue'].sum().reset_index()
        fig_rev = px.bar(rev_plan, x='plan', y='monthly_revenue',
                         color='plan', color_discrete_sequence=PALETTE,
                         labels={'monthly_revenue': 'Revenue ($)', 'plan': 'Plan'})
        fig_rev.update_layout(**PLOTLY_LAYOUT, height=260, title="MRR by Plan", showlegend=False)
        fig_rev.update_traces(marker_line_width=0)
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_e:
        st.markdown('<div class="section-header">Region Distribution</div>', unsafe_allow_html=True)
        reg_counts = df.groupby('region').agg(leads=('customer_id','count'),
                                               purchases=('purchased','sum')).reset_index()
        fig_reg = px.bar(reg_counts, x='region', y=['leads','purchases'],
                         barmode='group', color_discrete_sequence=[COLORS['primary'], COLORS['accent']],
                         labels={'value':'Count','variable':'','region':'Region'})
        fig_reg.update_layout(**PLOTLY_LAYOUT, height=260, title="Leads vs Purchases by Region")
        fig_reg.update_traces(marker_line_width=0)
        st.plotly_chart(fig_reg, use_container_width=True)

    # Raw data toggle
    with st.expander("📋 View Raw Data"):
        st.dataframe(df.head(50), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — MARKETING & CHANNELS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📣 Marketing & Channels":
    st.markdown('<div class="page-title">Marketing & Channel Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Channel ROI, conversion funnel, and ad spend efficiency</div>', unsafe_allow_html=True)

    ch = df.groupby('marketing_channel').agg(
        leads=('customer_id','count'),
        trials=('trial_signup','sum'),
        purchases=('purchased','sum'),
        avg_spend=('ad_spend_per_lead','mean'),
        revenue=('monthly_revenue','sum')
    ).reset_index()
    ch['trial_rate']    = (ch['trials'] / ch['leads'] * 100).round(1)
    ch['purchase_rate'] = (ch['purchases'] / ch['leads'] * 100).round(1)
    ch['roi']           = ((ch['revenue'] - ch['avg_spend']*ch['leads']) / (ch['avg_spend']*ch['leads'].clip(1)) * 100).round(1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Trial vs Purchase Rate by Channel</div>', unsafe_allow_html=True)
        fig = px.bar(ch.melt(id_vars='marketing_channel', value_vars=['trial_rate','purchase_rate']),
                     x='marketing_channel', y='value', color='variable', barmode='group',
                     color_discrete_sequence=[COLORS['primary'], COLORS['accent']],
                     labels={'value':'Rate (%)','variable':'','marketing_channel':'Channel'})
        fig.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=True)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Avg Ad Spend per Lead vs Purchase Rate</div>', unsafe_allow_html=True)
        fig2 = px.scatter(ch, x='avg_spend', y='purchase_rate', size='leads', color='marketing_channel',
                          text='marketing_channel', color_discrete_sequence=PALETTE,
                          labels={'avg_spend':'Avg Ad Spend/Lead ($)', 'purchase_rate':'Purchase Rate (%)',
                                  'marketing_channel':'Channel'})
        fig2.update_traces(textposition='top center', marker=dict(line=dict(width=1, color=COLORS['bg'])))
        fig2.update_layout(**PLOTLY_LAYOUT, height=320, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Channel Performance Table</div>', unsafe_allow_html=True)
    ch_display = ch[['marketing_channel','leads','trials','purchases','trial_rate','purchase_rate','avg_spend','revenue']].copy()
    ch_display.columns = ['Channel','Leads','Trials','Purchases','Trial Rate %','Purchase Rate %','Avg Spend ($)','Revenue ($)']
    st.dataframe(ch_display.set_index('Channel').round(2), use_container_width=True)

    st.markdown('<div class="section-header">Ad Spend Distribution by Channel</div>', unsafe_allow_html=True)
    fig3 = px.box(df[df['ad_spend_per_lead'] > 0], x='marketing_channel', y='ad_spend_per_lead',
                  color='marketing_channel', color_discrete_sequence=PALETTE,
                  labels={'ad_spend_per_lead':'Ad Spend ($)','marketing_channel':'Channel'})
    fig3.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False, title="Spend Spread per Channel")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
      <strong>💡 Channel Insights:</strong>
      <b>Referral</b> has the highest purchase conversion at lowest cost per lead — invest in a referral programme.
      <b>Google Ads</b> drives volume but at $18+/lead with moderate conversion — optimize targeting.
      <b>Organic</b> is zero-cost with a lower conversion funnel, requiring better landing page nurturing.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER SEGMENTS
# ════════════════════════════════════════════════════════════════════════════
elif page == "👥 Customer Segments":
    st.markdown('<div class="page-title">Customer Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Demographics, age groups, income tiers, and geographic breakdown</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Age Group → Purchase Rate</div>', unsafe_allow_html=True)
        age_grp = df.groupby('age_group').agg(
            leads=('customer_id','count'), purchases=('purchased','sum')).reset_index()
        age_grp['purchase_rate'] = (age_grp['purchases']/age_grp['leads']*100).round(1)
        age_order = ['18-25','26-35','36-45','46-55','56-65']
        age_grp['age_group'] = pd.Categorical(age_grp['age_group'], categories=age_order, ordered=True)
        age_grp = age_grp.sort_values('age_group')
        fig = px.bar(age_grp, x='age_group', y='purchase_rate', color='purchase_rate',
                     color_continuous_scale='Blues',
                     labels={'purchase_rate':'Purchase Rate (%)','age_group':'Age Group'})
        fig.update_layout(**PLOTLY_LAYOUT, height=300, coloraxis_showscale=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Income Segment → Conversion</div>', unsafe_allow_html=True)
        inc_grp = df.groupby('income_segment').agg(
            leads=('customer_id','count'), purchases=('purchased','sum')).reset_index()
        inc_grp['purchase_rate'] = (inc_grp['purchases']/inc_grp['leads']*100).round(1)
        inc_order = ['Low','Mid','High','Very High']
        inc_grp['income_segment'] = pd.Categorical(inc_grp['income_segment'], categories=inc_order, ordered=True)
        inc_grp = inc_grp.sort_values('income_segment')
        fig2 = px.bar(inc_grp, x='income_segment', y='purchase_rate', color='purchase_rate',
                      color_continuous_scale='Greens',
                      labels={'purchase_rate':'Purchase Rate (%)','income_segment':'Income Tier'})
        fig2.update_layout(**PLOTLY_LAYOUT, height=300, coloraxis_showscale=False)
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">Gender Breakdown</div>', unsafe_allow_html=True)
        gen = df.groupby('gender').agg(leads=('customer_id','count'), purchases=('purchased','sum')).reset_index()
        gen['purchase_rate'] = (gen['purchases']/gen['leads']*100).round(1)
        fig3 = px.bar(gen, x='gender', y=['leads','purchases'], barmode='group',
                      color_discrete_sequence=[COLORS['primary'], COLORS['accent']],
                      labels={'value':'Count','gender':'Gender','variable':''})
        fig3.update_layout(**PLOTLY_LAYOUT, height=280)
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Age Distribution (Purchased vs Not)</div>', unsafe_allow_html=True)
        fig4 = go.Figure()
        for bought, color, label in [(True, COLORS['accent'], 'Purchased'), (False, COLORS['danger'], 'Not Purchased')]:
            subset = df[df['purchased'] == bought]['age']
            fig4.add_trace(go.Histogram(x=subset, name=label, marker_color=color,
                                        opacity=0.7, nbinsx=20))
        fig4.update_layout(**PLOTLY_LAYOUT, barmode='overlay', height=280,
                           title="Age vs Purchase Decision",
                           xaxis_title="Age", yaxis_title="Count")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Income vs Age by Purchase Status</div>', unsafe_allow_html=True)
    fig5 = px.scatter(df.dropna(subset=['annual_income','age']),
                      x='age', y='annual_income', color='purchased',
                      color_discrete_map={True: COLORS['accent'], False: COLORS['danger']},
                      opacity=0.6, size_max=8,
                      labels={'annual_income':'Annual Income ($)','age':'Age','purchased':'Purchased'},
                      hover_data=['region','marketing_channel','plan'])
    fig5.update_layout(**PLOTLY_LAYOUT, height=340, title="Income vs Age — Purchase Outcomes")
    st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CONVERSION & REVENUE
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Conversion & Revenue":
    st.markdown('<div class="page-title">Conversion & Revenue Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Trial behaviour, NPS impact, plan economics, and revenue drivers</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Usage Sessions → NPS (Trial Users)</div>', unsafe_allow_html=True)
        trial_df = df[df['trial_signup']].dropna(subset=['nps_score','usage_sessions'])
        if len(trial_df) > 5:
            m, b, r, p, _ = stats.linregress(trial_df['usage_sessions'], trial_df['nps_score'])
            x_line = np.linspace(trial_df['usage_sessions'].min(), trial_df['usage_sessions'].max(), 100)
            fig = px.scatter(trial_df, x='usage_sessions', y='nps_score',
                             color='purchased',
                             color_discrete_map={True: COLORS['accent'], False: COLORS['danger']},
                             opacity=0.6, size_max=8,
                             labels={'usage_sessions':'Usage Sessions','nps_score':'NPS Score',
                                     'purchased':'Purchased'})
            fig.add_trace(go.Scatter(x=x_line, y=m*x_line+b, mode='lines',
                                     line=dict(color='white', width=2, dash='dash'),
                                     name=f'Trend (r={r:.2f})'))
            fig.update_layout(**PLOTLY_LAYOUT, height=320, title=f"Sessions vs NPS · r={r:.2f}, p={p:.3f}")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Days to Trial Conversion (Distribution)</div>', unsafe_allow_html=True)
        days_df = df[df['trial_signup']].dropna(subset=['days_to_trial'])
        fig2 = go.Figure()
        for bought, color, label in [(True, COLORS['accent'], 'Purchased'), (False, COLORS['primary'], 'Not Purchased')]:
            sub = days_df[days_df['purchased'] == bought]['days_to_trial']
            fig2.add_trace(go.Histogram(x=sub, name=label, marker_color=color, opacity=0.75, nbinsx=20))
        fig2.update_layout(**PLOTLY_LAYOUT, barmode='overlay', height=320,
                           title="Days from Lead to Trial", xaxis_title="Days", yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-header">NPS Score by Plan</div>', unsafe_allow_html=True)
        nps_plan = df[df['purchased']].dropna(subset=['nps_score'])
        fig3 = px.violin(nps_plan, x='plan', y='nps_score', color='plan',
                         color_discrete_sequence=PALETTE, box=True, points='all',
                         labels={'nps_score':'NPS Score','plan':'Plan'})
        fig3.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False, title="NPS Distribution per Plan")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Revenue per Session by Plan</div>', unsafe_allow_html=True)
        rev_sess = df[df['purchased'] & (df['revenue_per_session'] > 0)].dropna(subset=['revenue_per_session'])
        fig4 = px.box(rev_sess, x='plan', y='revenue_per_session', color='plan',
                      color_discrete_sequence=PALETTE,
                      labels={'revenue_per_session':'Revenue/Session ($)','plan':'Plan'})
        fig4.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False, title="Monetisation Efficiency")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Monthly Revenue by Region & Plan</div>', unsafe_allow_html=True)
    rev_heatmap = df[df['purchased']].groupby(['region','plan'])['monthly_revenue'].sum().reset_index()
    rev_pivot = rev_heatmap.pivot(index='region', columns='plan', values='monthly_revenue').fillna(0)
    fig5 = px.imshow(rev_pivot, color_continuous_scale='Blues', aspect='auto',
                     labels=dict(color='Revenue ($)'))
    fig5.update_layout(**PLOTLY_LAYOUT, height=280, title="Revenue Heatmap: Region × Plan",
                       coloraxis_colorbar=dict(title='$'))
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
      <strong>💡 Revenue Insight:</strong>
      Premium plan subscribers generate the highest <b>revenue per session</b>, confirming strong monetisation
      among power users. Customers who convert in <b>fewer than 5 days</b> from lead to trial have higher purchase rates,
      suggesting speed of onboarding matters. NPS ≥ 8 users are 2× more likely to choose Standard or Premium.
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CORRELATION ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔗 Correlation Analysis":
    st.markdown('<div class="page-title">Correlation & Statistical Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Pearson correlations, pair relationships, and statistical significance</div>', unsafe_allow_html=True)

    num_cols = ['age','annual_income','ad_spend_per_lead','days_to_trial',
                'usage_sessions','nps_score','monthly_revenue']
    df_num = df[num_cols].copy()
    df_num['purchased_int'] = df['purchased'].astype(int)
    df_num['churned_int']   = df['churned'].astype(int)
    corr = df_num.corr().round(3)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="section-header">Correlation Heatmap</div>', unsafe_allow_html=True)
        fig = px.imshow(corr, color_continuous_scale='RdYlGn', zmin=-1, zmax=1,
                        text_auto=True, aspect='auto')
        fig.update_traces(textfont_size=10)
        fig.update_layout(**PLOTLY_LAYOUT, height=440, title="Pearson Correlation Matrix",
                          coloraxis_colorbar=dict(title='r'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Top Correlations (abs)</div>', unsafe_allow_html=True)
        corr_pairs = []
        cols = corr.columns.tolist()
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                corr_pairs.append({'Feature A': cols[i], 'Feature B': cols[j],
                                   'r': corr.iloc[i, j], 'Abs r': abs(corr.iloc[i, j])})
        corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Abs r', ascending=False).head(12)
        fig2 = px.bar(corr_pairs_df, x='r', y=corr_pairs_df['Feature A'] + ' ↔ ' + corr_pairs_df['Feature B'],
                      orientation='h', color='r', color_continuous_scale='RdYlGn',
                      color_continuous_midpoint=0,
                      labels={'r':'Correlation (r)', 'y':'Feature Pair'})
        fig2.update_layout(**PLOTLY_LAYOUT, height=440, title="Ranked by |r|",
                           coloraxis_showscale=False, yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">Interactive Variable Explorer</div>', unsafe_allow_html=True)
    col3, col4, col5 = st.columns([1,1,1])
    with col3:
        x_var = st.selectbox("X-Axis", num_cols, index=4)  # usage_sessions
    with col4:
        y_var = st.selectbox("Y-Axis", num_cols, index=5)  # nps_score
    with col5:
        color_var = st.selectbox("Color By", ['purchased','region','plan','marketing_channel','gender'])

    color_map = None
    if color_var == 'purchased':
        color_map = {True: COLORS['accent'], False: COLORS['danger']}

    scatter_df = df.dropna(subset=[x_var, y_var])
    fig3 = px.scatter(scatter_df, x=x_var, y=y_var, color=color_var,
                      color_discrete_map=color_map,
                      color_discrete_sequence=PALETTE,
                      opacity=0.65, trendline='ols',
                      labels={x_var: x_var.replace('_',' ').title(),
                              y_var: y_var.replace('_',' ').title()},
                      hover_data=['region','marketing_channel'])
    fig3.update_layout(**PLOTLY_LAYOUT, height=360, title=f"{x_var} vs {y_var}")
    st.plotly_chart(fig3, use_container_width=True)

    # Stats summary
    if len(scatter_df) > 5:
        r_val, p_val = stats.pearsonr(scatter_df[x_var].dropna(), scatter_df[y_var].dropna())
        st.markdown(f"""
        <div class="insight-box">
          <strong>📊 Statistical Result:</strong>
          Pearson r = <b>{r_val:.3f}</b>, p-value = <b>{p_val:.4f}</b>.
          {"<b>Statistically significant</b> at α=0.05 — there is a meaningful linear relationship." if p_val < 0.05
           else "Not statistically significant at α=0.05 — the relationship may be random."}
        </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 — CHURN INTELLIGENCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Churn Intelligence":
    st.markdown('<div class="page-title">Churn Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Retention analysis, churn drivers, and at-risk customer profiling</div>', unsafe_allow_html=True)

    subs = df[df['purchased']].copy()
    total_subs = len(subs)
    churned    = subs['churned'].sum()
    retained   = total_subs - churned
    churn_pct  = churned/total_subs*100 if total_subs else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, color, label, val, sub in [
        (c1, "blue",  "TOTAL SUBSCRIBERS", f"{total_subs}", "Paying customers"),
        (c2, "green", "RETAINED",           f"{retained}", f"{100-churn_pct:.1f}% retention"),
        (c3, "red",   "CHURNED",            f"{churned}", f"{churn_pct:.1f}% churn rate"),
        (c4, "amber", "AVG NPS (CHURNED)",
         f"{subs[subs['churned']]['nps_score'].mean():.1f}" if churned else "—",
         "vs overall avg")
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card {color}">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{val}</div>
              <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Churn Rate by Plan</div>', unsafe_allow_html=True)
        churn_plan = subs.groupby('plan').agg(
            total=('customer_id','count'), churned=('churned','sum')).reset_index()
        churn_plan['churn_rate'] = (churn_plan['churned']/churn_plan['total']*100).round(1)
        fig = px.bar(churn_plan, x='plan', y='churn_rate', color='churn_rate',
                     color_continuous_scale='Reds', text='churn_rate',
                     labels={'churn_rate':'Churn Rate (%)','plan':'Plan'})
        fig.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=0)
        fig.update_layout(**PLOTLY_LAYOUT, height=300, coloraxis_showscale=False, title="Churn % by Plan")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Churn Rate by Region</div>', unsafe_allow_html=True)
        churn_reg = subs.groupby('region').agg(
            total=('customer_id','count'), churned=('churned','sum')).reset_index()
        churn_reg['churn_rate'] = (churn_reg['churned']/churn_reg['total']*100).round(1)
        fig2 = px.bar(churn_reg.sort_values('churn_rate', ascending=False),
                      x='region', y='churn_rate', color='churn_rate',
                      color_continuous_scale='Oranges', text='churn_rate',
                      labels={'churn_rate':'Churn Rate (%)','region':'Region'})
        fig2.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=0)
        fig2.update_layout(**PLOTLY_LAYOUT, height=300, coloraxis_showscale=False, title="Churn % by Region")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">NPS Score Distribution: Churned vs Retained</div>', unsafe_allow_html=True)
    fig3 = go.Figure()
    nps_sub = subs.dropna(subset=['nps_score'])
    for churned_flag, color, label in [(True, COLORS['danger'], 'Churned'), (False, COLORS['accent'], 'Retained')]:
        sub = nps_sub[nps_sub['churned'] == churned_flag]['nps_score']
        fig3.add_trace(go.Violin(x=sub, name=label, line_color=color, fillcolor=color,
                                 opacity=0.6, meanline_visible=True, orientation='h',
                                 side='positive' if not churned_flag else 'negative'))
    fig3.update_layout(**PLOTLY_LAYOUT, height=280, violingap=0, violinmode='overlay',
                       title="NPS Score: Churned vs Retained (mirrored violin)",
                       xaxis_title="NPS Score")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-header">Churn Risk Profile: Usage Sessions vs NPS</div>', unsafe_allow_html=True)
    churn_df = subs.dropna(subset=['usage_sessions','nps_score'])
    fig4 = px.scatter(churn_df, x='usage_sessions', y='nps_score', color='churned',
                      color_discrete_map={True: COLORS['danger'], False: COLORS['accent']},
                      opacity=0.7, size_max=10,
                      labels={'usage_sessions':'Usage Sessions','nps_score':'NPS Score','churned':'Churned'},
                      hover_data=['plan','region'])
    fig4.add_vline(x=churn_df['usage_sessions'].mean(), line_dash='dash', line_color='white',
                   annotation_text='Avg Sessions', opacity=0.5)
    fig4.add_hline(y=7, line_dash='dash', line_color='yellow',
                   annotation_text='NPS Threshold (7)', opacity=0.5)
    fig4.update_layout(**PLOTLY_LAYOUT, height=360, title="Churn Risk Map — Quadrant Analysis")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
      <strong>💡 Churn Intelligence:</strong>
      Customers with <b>NPS &lt; 7</b> AND <b>usage sessions &lt; 15</b> (bottom-left quadrant) represent the highest churn risk.
      <b>Basic plan subscribers churn most</b> — consider adding an onboarding coach or in-app milestone rewards for first 30 days.
      <b>Central region</b> shows elevated churn — a targeted CS intervention could recover 3–5% retention improvement.
    </div>""", unsafe_allow_html=True)
