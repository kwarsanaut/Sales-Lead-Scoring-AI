import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Intelligent Sales AI Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .lead-score-high {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .lead-score-medium {
        background: linear-gradient(90deg, #ff9800, #f57c00);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .lead-score-low {
        background: linear-gradient(90deg, #f44336, #d32f2f);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Generate mock data
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    
    # Lead sources
    lead_sources = ['Website', 'LinkedIn', 'Email Campaign', 'Referral', 'Trade Show', 'Cold Outreach', 'Content Marketing', 'Webinar']
    
    # Industries
    industries = ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education', 'Real Estate', 'Consulting']
    
    # Company sizes
    company_sizes = ['1-10', '11-50', '51-200', '201-1000', '1000+']
    
    # Job titles
    job_titles = ['CEO', 'VP Sales', 'Sales Manager', 'Director', 'VP Marketing', 'IT Manager', 'CFO', 'Operations Manager']
    
    # Generate 500 leads
    leads = []
    for i in range(500):
        # Base scoring factors
        company_size_score = np.random.choice([10, 20, 30, 40, 50], p=[0.2, 0.3, 0.25, 0.15, 0.1])
        industry_score = np.random.randint(10, 40)
        engagement_score = np.random.randint(0, 30)
        title_score = np.random.choice([10, 15, 20, 25, 30], p=[0.15, 0.2, 0.3, 0.2, 0.15])
        
        # Calculate total score with some randomness
        base_score = company_size_score + industry_score + engagement_score + title_score
        final_score = min(100, max(0, base_score + np.random.randint(-15, 15)))
        
        # Determine conversion based on score
        conversion_prob = final_score / 100 * 0.6 + 0.1  # 10-70% based on score
        converted = np.random.random() < conversion_prob
        
        # Lead age
        lead_age = np.random.randint(1, 90)
        
        lead = {
            'lead_id': f'LEAD-{1000 + i}',
            'company_name': f'Company {chr(65 + i % 26)}{i}',
            'contact_name': f'Contact {i}',
            'email': f'contact{i}@company{i}.com',
            'phone': f'+1-555-{random.randint(1000, 9999)}',
            'lead_source': np.random.choice(lead_sources),
            'industry': np.random.choice(industries),
            'company_size': np.random.choice(company_sizes),
            'job_title': np.random.choice(job_titles),
            'lead_score': final_score,
            'conversion_probability': round(conversion_prob * 100, 1),
            'estimated_deal_value': np.random.randint(5000, 150000),
            'lead_age_days': lead_age,
            'last_contact': datetime.now() - timedelta(days=np.random.randint(0, 30)),
            'email_opens': np.random.randint(0, 15),
            'website_visits': np.random.randint(0, 25),
            'content_downloads': np.random.randint(0, 8),
            'converted': converted,
            'time_to_close': np.random.randint(15, 120) if converted else None,
            'actual_deal_value': np.random.randint(3000, 180000) if converted else None
        }
        leads.append(lead)
    
    return pd.DataFrame(leads)

# Load data
df_leads = generate_mock_data()

# Sidebar navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.selectbox("Select Module", [
    "Executive Dashboard", 
    "Lead Scoring Engine", 
    "Conversion Analytics", 
    "Sales Automation",
    "ROI Analysis"
])

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Intelligent Sales AI Platform</h1>
    <p>AI-Powered Lead Scoring & Sales Optimization System</p>
</div>
""", unsafe_allow_html=True)

if page == "Executive Dashboard":
    st.header("📊 Executive Sales Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_leads = len(df_leads)
    high_quality_leads = len(df_leads[df_leads['lead_score'] >= 70])
    avg_conversion_rate = (df_leads['converted'].sum() / total_leads) * 100
    total_pipeline_value = df_leads['estimated_deal_value'].sum()
    
    with col1:
        st.metric(
            label="Total Active Leads",
            value=f"{total_leads:,}",
            delta=f"+{random.randint(15, 45)} this week"
        )
    
    with col2:
        st.metric(
            label="High-Quality Leads",
            value=f"{high_quality_leads}",
            delta=f"+{random.randint(5, 15)} this week"
        )
    
    with col3:
        st.metric(
            label="Conversion Rate",
            value=f"{avg_conversion_rate:.1f}%",
            delta=f"+{random.randint(2, 8)}% vs last month"
        )
    
    with col4:
        st.metric(
            label="Pipeline Value",
            value=f"${total_pipeline_value/1000000:.1f}M",
            delta=f"+${random.randint(100, 500)}K this month"
        )
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Lead Score Distribution")
        
        # Create score categories
        df_leads['score_category'] = pd.cut(df_leads['lead_score'], 
                                          bins=[0, 40, 70, 100], 
                                          labels=['Cold (0-40)', 'Warm (41-70)', 'Hot (71-100)'])
        
        score_dist = df_leads['score_category'].value_counts()
        
        fig_score = px.pie(
            values=score_dist.values,
            names=score_dist.index,
            color_discrete_sequence=['#f44336', '#ff9800', '#4CAF50'],
            title="Lead Quality Distribution"
        )
        fig_score.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_score, use_container_width=True)
    
    with col2:
        st.subheader("Lead Sources Performance")
        
        source_performance = df_leads.groupby('lead_source').agg({
            'lead_score': 'mean',
            'converted': 'mean',
            'lead_id': 'count'
        }).round(2)
        source_performance.columns = ['Avg Score', 'Conversion Rate', 'Lead Count']
        source_performance['Conversion Rate'] *= 100
        
        fig_sources = px.scatter(
            source_performance.reset_index(),
            x='Avg Score',
            y='Conversion Rate',
            size='Lead Count',
            hover_name='lead_source',
            title="Lead Source Quality vs Conversion",
            labels={'Avg Score': 'Average Lead Score', 'Conversion Rate': 'Conversion Rate (%)'}
        )
        st.plotly_chart(fig_sources, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Sales Pipeline")
        
        # Generate monthly data
        months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
        monthly_pipeline = []
        
        for month in months:
            pipeline_value = random.randint(800000, 1500000)
            closed_deals = random.randint(150000, 400000)
            monthly_pipeline.append({
                'Month': month.strftime('%b %Y'),
                'Pipeline Value': pipeline_value,
                'Closed Deals': closed_deals
            })
        
        df_monthly = pd.DataFrame(monthly_pipeline)
        
        fig_pipeline = go.Figure()
        fig_pipeline.add_trace(go.Scatter(
            x=df_monthly['Month'],
            y=df_monthly['Pipeline Value'],
            mode='lines+markers',
            name='Pipeline Value',
            line=dict(color='#667eea', width=3)
        ))
        fig_pipeline.add_trace(go.Scatter(
            x=df_monthly['Month'],
            y=df_monthly['Closed Deals'],
            mode='lines+markers',
            name='Closed Deals',
            line=dict(color='#4CAF50', width=3)
        ))
        
        fig_pipeline.update_layout(
            title="Sales Pipeline Trends",
            xaxis_title="Month",
            yaxis_title="Value ($)",
            hovermode='x'
        )
        st.plotly_chart(fig_pipeline, use_container_width=True)
    
    with col2:
        st.subheader("Conversion Rate by Industry")
        
        industry_conv = df_leads.groupby('industry').agg({
            'converted': 'mean',
            'lead_id': 'count'
        })
        industry_conv['Conversion Rate'] = industry_conv['converted'] * 100
        industry_conv = industry_conv[industry_conv['lead_id'] >= 10]  # Filter industries with at least 10 leads
        
        fig_industry = px.bar(
            industry_conv.reset_index(),
            x='industry',
            y='Conversion Rate',
            title="Industry Conversion Rates",
            color='Conversion Rate',
            color_continuous_scale='Viridis'
        )
        fig_industry.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_industry, use_container_width=True)

elif page == "Lead Scoring Engine":
    st.header("🎯 AI Lead Scoring Engine")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Lead Evaluation System")
        
        # Lead scoring form
        with st.form("lead_scoring_form"):
            st.markdown("### Evaluate New Lead")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                company_name = st.text_input("Company Name", value="ABC Corporation")
                contact_name = st.text_input("Contact Name", value="John Smith")
                industry = st.selectbox("Industry", ['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail', 'Education'])
                company_size = st.selectbox("Company Size", ['1-10', '11-50', '51-200', '201-1000', '1000+'])
            
            with col_b:
                job_title = st.selectbox("Job Title", ['CEO', 'VP Sales', 'Sales Manager', 'Director', 'VP Marketing', 'IT Manager'])
                lead_source = st.selectbox("Lead Source", ['Website', 'LinkedIn', 'Email Campaign', 'Referral', 'Trade Show'])
                email_opens = st.slider("Email Opens (last 30 days)", 0, 20, 5)
                website_visits = st.slider("Website Visits (last 30 days)", 0, 30, 8)
            
            budget_range = st.selectbox("Budget Range", ['<$10K', '$10K-$50K', '$50K-$100K', '$100K-$500K', '$500K+'])
            urgency = st.selectbox("Purchase Urgency", ['Not urgent', 'Within 6 months', 'Within 3 months', 'Within 1 month', 'Immediate'])
            
            submitted = st.form_submit_button("Calculate Lead Score", type="primary")
        
        if submitted:
            # Calculate score based on inputs
            score = 0
            
            # Company size scoring
            size_scores = {'1-10': 10, '11-50': 20, '51-200': 30, '201-1000': 40, '1000+': 50}
            score += size_scores[company_size]
            
            # Title scoring
            title_scores = {'CEO': 30, 'VP Sales': 25, 'VP Marketing': 25, 'Sales Manager': 20, 'Director': 20, 'IT Manager': 15}
            score += title_scores[job_title]
            
            # Engagement scoring
            score += min(email_opens * 2, 20)  # Max 20 points
            score += min(website_visits * 1, 15)  # Max 15 points
            
            # Budget scoring
            budget_scores = {'<$10K': 5, '$10K-$50K': 10, '$50K-$100K': 15, '$100K-$500K': 20, '$500K+': 25}
            score += budget_scores[budget_range]
            
            # Urgency scoring
            urgency_scores = {'Not urgent': 0, 'Within 6 months': 5, 'Within 3 months': 10, 'Within 1 month': 15, 'Immediate': 20}
            score += urgency_scores[urgency]
            
            # Display results
            st.markdown("### 📊 Lead Score Results")
            
            if score >= 70:
                st.markdown(f'<div class="lead-score-high">🔥 HOT LEAD: {score}/100</div>', unsafe_allow_html=True)
                recommendation = "🚨 **IMMEDIATE ACTION REQUIRED** - Assign to senior sales rep within 1 hour"
                conversion_prob = 65 + random.randint(0, 20)
            elif score >= 40:
                st.markdown(f'<div class="lead-score-medium">🟡 WARM LEAD: {score}/100</div>', unsafe_allow_html=True)
                recommendation = "📞 Contact within 24 hours - High potential for conversion"
                conversion_prob = 35 + random.randint(0, 25)
            else:
                st.markdown(f'<div class="lead-score-low">❄️ COLD LEAD: {score}/100</div>', unsafe_allow_html=True)
                recommendation = "📧 Add to nurturing campaign - Educational content focus"
                conversion_prob = 10 + random.randint(0, 20)
            
            st.success(recommendation)
            
            col_x, col_y, col_z = st.columns(3)
            with col_x:
                st.metric("Conversion Probability", f"{conversion_prob}%")
            with col_y:
                estimated_value = random.randint(15000, 120000)
                st.metric("Est. Deal Value", f"${estimated_value:,}")
            with col_z:
                expected_close = random.randint(30, 120)
                st.metric("Expected Close Time", f"{expected_close} days")
    
    with col2:
        st.subheader("Scoring Factors")
        
        st.markdown("""
        ### 🎯 Lead Scoring Criteria
        
        **Company Profile (50 points)**
        - Company Size: 10-50 pts
        - Industry Match: 10-25 pts
        - Budget Range: 5-25 pts
        
        **Contact Profile (30 points)**
        - Job Title/Seniority: 15-30 pts
        - Decision Making Power: 0-15 pts
        
        **Engagement Level (20 points)**
        - Email Opens: 0-20 pts
        - Website Visits: 0-15 pts
        - Content Downloads: 0-10 pts
        - Demo Requests: 15 pts
        
        **Intent Signals (20 points)**
        - Purchase Urgency: 0-20 pts
        - Competitor Research: 10 pts
        - Pricing Inquiries: 15 pts
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 📈 Score Classifications
        
        - **🔥 Hot Leads (70-100)**: Immediate follow-up
        - **🟡 Warm Leads (40-69)**: Contact within 24h
        - **❄️ Cold Leads (0-39)**: Nurturing campaign
        """)
    
    # Recent leads table
    st.subheader("Recent High-Score Leads")
    
    high_score_leads = df_leads[df_leads['lead_score'] >= 60].sort_values('lead_score', ascending=False).head(10)
    
    display_leads = high_score_leads[['company_name', 'contact_name', 'lead_source', 'industry', 'lead_score', 'conversion_probability', 'estimated_deal_value']].copy()
    display_leads['estimated_deal_value'] = display_leads['estimated_deal_value'].apply(lambda x: f"${x:,}")
    display_leads['conversion_probability'] = display_leads['conversion_probability'].apply(lambda x: f"{x}%")
    display_leads.columns = ['Company', 'Contact', 'Source', 'Industry', 'Score', 'Conv. Prob.', 'Est. Value']
    
    st.dataframe(display_leads, use_container_width=True)

elif page == "Conversion Analytics":
    st.header("📈 Conversion Analytics & Insights")
    
    # Conversion funnel
    st.subheader("Sales Conversion Funnel")
    
    # Create funnel data
    funnel_stages = ['Leads Generated', 'Qualified Leads', 'Opportunities', 'Proposals Sent', 'Closed Won']
    funnel_values = [500, 300, 180, 120, 85]
    funnel_colors = ['#E8F4FD', '#B8E6B8', '#87CEEB', '#FFA07A', '#90EE90']
    
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        textinfo="value+percent initial",
        marker=dict(color=funnel_colors)
    ))
    
    fig_funnel.update_layout(
        title="Sales Conversion Funnel Analysis",
        font_size=12,
    )
    
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Conversion metrics by lead score
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conversion Rate by Lead Score Range")
        
        score_ranges = ['0-30', '31-50', '51-70', '71-85', '86-100']
        conversion_rates = [8, 22, 45, 68, 85]
        
        fig_conversion = px.bar(
            x=score_ranges,
            y=conversion_rates,
            title="Lead Score vs Conversion Rate",
            labels={'x': 'Lead Score Range', 'y': 'Conversion Rate (%)'},
            color=conversion_rates,
            color_continuous_scale='RdYlGn'
        )
        
        st.plotly_chart(fig_conversion, use_container_width=True)
    
    with col2:
        st.subheader("Average Deal Size by Score")
        
        avg_deal_sizes = [12000, 28000, 45000, 72000, 95000]
        
        fig_deal_size = px.line(
            x=score_ranges,
            y=avg_deal_sizes,
            title="Lead Score vs Average Deal Size",
            labels={'x': 'Lead Score Range', 'y': 'Average Deal Size ($)'},
            markers=True
        )
        
        fig_deal_size.update_traces(line=dict(color='#667eea', width=4))
        st.plotly_chart(fig_deal_size, use_container_width=True)
    
    # Time to close analysis
    st.subheader("Time to Close Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create sample data for time to close by score
        score_categories = ['Hot (70-100)', 'Warm (40-69)', 'Cold (0-39)']
        avg_time_to_close = [35, 65, 95]
        
        fig_time = px.bar(
            x=score_categories,
            y=avg_time_to_close,
            title="Average Time to Close by Lead Quality",
            labels={'x': 'Lead Category', 'y': 'Days to Close'},
            color=avg_time_to_close,
            color_continuous_scale='RdYlGn_r'
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        # Win rate by lead source
        source_win_rates = df_leads.groupby('lead_source')['converted'].mean() * 100
        
        fig_source_win = px.bar(
            x=source_win_rates.index,
            y=source_win_rates.values,
            title="Win Rate by Lead Source",
            labels={'x': 'Lead Source', 'y': 'Win Rate (%)'},
            color=source_win_rates.values,
            color_continuous_scale='Viridis'
        )
        
        fig_source_win.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig_source_win, use_container_width=True)
    
    # Predictive analytics
    st.subheader("Predictive Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        projected_monthly_conversions = random.randint(75, 95)
        st.metric(
            "Projected Monthly Conversions", 
            f"{projected_monthly_conversions}",
            f"+{random.randint(8, 18)}% vs last month"
        )
    
    with col2:
        projected_revenue = random.randint(380000, 450000)
        st.metric(
            "Projected Monthly Revenue", 
            f"${projected_revenue:,}",
            f"+{random.randint(12, 28)}% vs last month"
        )
    
    with col3:
        forecasted_pipeline = random.randint(1200000, 1800000)
        st.metric(
            "Next Quarter Pipeline", 
            f"${forecasted_pipeline:,}",
            f"+{random.randint(15, 35)}% vs current"
        )

elif page == "Sales Automation":
    st.header("🚀 Sales Automation & Optimization")
    
    # Automation rules
    st.subheader("Intelligent Lead Routing Rules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Automated Lead Assignment
        
        **Hot Leads (Score 70-100)**
        - ⚡ Instant assignment to senior sales reps
        - 📱 SMS & email alerts within 5 minutes
        - 📞 Auto-schedule follow-up calls
        - 🏆 Route to top performers
        
        **Warm Leads (Score 40-69)**
        - 📧 Email assignment within 2 hours
        - 📅 Schedule in CRM follow-up tasks
        - 🎯 Assign based on territory/expertise
        - 📊 Add to sales pipeline
        
        **Cold Leads (Score 0-39)**
        - 📬 Auto-enroll in nurturing campaigns
        - 📚 Send educational content series
        - ⏰ Schedule monthly check-ins
        - 🔄 Re-score after engagement
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 Smart Follow-up Scheduling
        
        **Priority-Based Timing**
        - 🔥 Hot leads: < 1 hour
        - 🟡 Warm leads: < 24 hours
        - ❄️ Cold leads: Weekly nurturing
        
        **Optimal Contact Windows**
        - ☀️ Morning: 9-11 AM (highest response)
        - 🌅 Afternoon: 2-4 PM (secondary)
        - 📅 Tuesday-Thursday (peak days)
        - ⏰ Avoid: Monday mornings, Friday afternoons
        
        **Multi-channel Sequencing**
        - 📧 Email → 📞 Phone → 💼 LinkedIn
        - 📱 SMS for urgent hot leads
        - 🎥 Video messages for key accounts
        """)
    
    # Lead prioritization
    st.subheader("Daily Lead Prioritization")
    
    # Generate priority list
    priority_leads = df_leads.copy()
    priority_leads['priority_score'] = (
        priority_leads['lead_score'] * 0.5 + 
        (100 - priority_leads['lead_age_days']) * 0.3 + 
        priority_leads['email_opens'] * 2
    )
    
    top_priority = priority_leads.nlargest(15, 'priority_score')
    
    display_priority = top_priority[['company_name', 'contact_name', 'lead_score', 'lead_age_days', 'conversion_probability', 'estimated_deal_value']].copy()
    display_priority['Action Required'] = display_priority['lead_score'].apply(
        lambda x: '🔥 Call Now' if x >= 70 else '📧 Email Today' if x >= 40 else '📬 Add to Campaign'
    )
    display_priority['estimated_deal_value'] = display_priority['estimated_deal_value'].apply(lambda x: f"${x:,}")
    display_priority.columns = ['Company', 'Contact', 'Score', 'Age (Days)', 'Conv. Prob.', 'Est. Value', 'Action Required']
    
    st.dataframe(display_priority, use_container_width=True)
    
    # Automation performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Automation Performance Metrics")
        
        automation_metrics = {
            'Response Time Improvement': '78%',
            'Lead Follow-up Rate': '94%',
            'Sales Rep Productivity': '+42%',
            'Conversion Rate Increase': '+35%',
            'Time Saved per Rep/Week': '12 hours'
        }
        
        for metric, value in automation_metrics.items():
            st.metric(metric, value)
    
    with col2:
        st.subheader("Automated Task Distribution")
        
        task_types = ['Lead Assignment', 'Follow-up Scheduling', 'Email Sequences', 'CRM Updates', 'Report Generation']
        task_counts = [45, 38, 28, 22, 15]
        
        fig_tasks = px.pie(
            values=task_counts,
            names=task_types,
            title="Daily Automated Tasks"
        )
        
        st.plotly_chart(fig_tasks, use_container_width=True)
    
    # Workflow optimization
    st.subheader("Workflow Optimization Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Lead Qualification
        - Implement BANT scoring
        - Add progressive profiling
        - Use predictive lead scoring
        - Integrate intent data sources
        """)
    
    with col2:
        st.markdown("""
        ### 📞 Sales Process
        - Standardize call scripts
        - Implement sales stages
        - Add win/loss analysis
        - Create follow-up templates
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Performance Tracking
        - Monitor conversion rates
        - Track response times
        - Measure deal velocity
        - Analyze rep performance
        """)

elif page == "ROI Analysis":
    st.header("💰 ROI Analysis & Business Impact")
    
    # Key ROI metrics
    st.subheader("Platform ROI Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Annual ROI",
            "340%",
            "+85% vs manual process"
        )
    
    with col2:
        st.metric(
            "Revenue Increase",
            "$2.1M",
            "+28% vs last year"
        )
    
    with col3:
        st.metric(
            "Cost Savings",
            "$480K",
            "Time & resource optimization"
        )
    
    with col4:
        st.metric(
            "Payback Period",
            "3.2 months",
            "Faster than projected"
        )
    
    # Before vs After comparison
    st.subheader("Performance Transformation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Before AI Implementation")
        
        before_metrics = {
            'Lead Response Time': '4.2 hours',
            'Conversion Rate': '12.3%',
            'Sales Cycle Length': '89 days',
            'Lead Qualification Rate': '31%',
            'Sales Rep Productivity': '6.2 calls/day',
            'Cost per Lead': '$127',
            'Revenue per Rep/Month': '$42K'
        }
        
        for metric, value in before_metrics.items():
            st.markdown(f"**{metric}:** {value}")
    
    with col2:
        st.markdown("### 🚀 After AI Implementation")
        
        after_metrics = {
            'Lead Response Time': '22 minutes',
            'Conversion Rate': '16.8%',
            'Sales Cycle Length': '64 days',
            'Lead Qualification Rate': '47%',
            'Sales Rep Productivity': '9.1 calls/day',
            'Cost per Lead': '$89',
            'Revenue per Rep/Month': '$58K'
        }
        
        improvements = {
            'Lead Response Time': '91% faster',
            'Conversion Rate': '+37% increase',
            'Sales Cycle Length': '28% shorter',
            'Lead Qualification Rate': '+52% increase',
            'Sales Rep Productivity': '+47% increase',
            'Cost per Lead': '30% reduction',
            'Revenue per Rep/Month': '+38% increase'
        }
        
        for metric, value in after_metrics.items():
            improvement = improvements[metric]
            st.markdown(f"**{metric}:** {value} *({improvement})*")
    
    # ROI calculation breakdown
    st.subheader("ROI Calculation Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💸 Investment Costs (Annual)
        
        **Platform & Technology**
        - AI Platform License: $48,000
        - Integration & Setup: $15,000
        - Training & Onboarding: $8,000
        - Maintenance & Support: $12,000
        
        **Total Investment: $83,000**
        """)
        
        # Investment breakdown chart
        investment_categories = ['Platform License', 'Integration', 'Training', 'Maintenance']
        investment_amounts = [48000, 15000, 8000, 12000]
        
        fig_investment = px.pie(
            values=investment_amounts,
            names=investment_categories,
            title="Investment Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig_investment, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 💰 Revenue Benefits (Annual)
        
        **Direct Revenue Impact**
        - Increased Conversion Rate: $1,240,000
        - Faster Sales Cycles: $430,000
        - Higher Deal Values: $320,000
        - Reduced Lead Acquisition Cost: $180,000
        
        **Operational Savings**
        - Time Savings (Sales Team): $280,000
        - Reduced Manual Tasks: $120,000
        - Improved Productivity: $340,000
        
        **Total Benefits: $2,910,000**
        """)
        
        # Benefits breakdown chart
        benefit_categories = ['Conversion Increase', 'Faster Cycles', 'Higher Values', 'Cost Reduction', 'Time Savings', 'Productivity']
        benefit_amounts = [1240000, 430000, 320000, 180000, 400000, 340000]
        
        fig_benefits = px.bar(
            x=benefit_categories,
            y=benefit_amounts,
            title="Annual Benefits Breakdown",
            color=benefit_amounts,
            color_continuous_scale='Greens'
        )
        fig_benefits.update_layout(xaxis_tickangle=45, showlegend=False)
        
        st.plotly_chart(fig_benefits, use_container_width=True)
    
    # Monthly ROI tracking
    st.subheader("Monthly ROI Progression")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cumulative_roi = [15, 35, 68, 105, 148, 195, 238, 275, 305, 325, 340, 355]
    monthly_revenue_impact = [85000, 125000, 180000, 220000, 245000, 265000, 280000, 295000, 310000, 320000, 330000, 340000]
    
    fig_roi_progression = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_roi_progression.add_trace(
        go.Scatter(x=months, y=cumulative_roi, name="Cumulative ROI (%)", line=dict(color='#667eea', width=3)),
        secondary_y=False,
    )
    
    fig_roi_progression.add_trace(
        go.Bar(x=months, y=monthly_revenue_impact, name="Monthly Revenue Impact", opacity=0.7, marker_color='#4CAF50'),
        secondary_y=True,
    )
    
    fig_roi_progression.update_layout(
        title_text="ROI Growth & Revenue Impact Over Time",
        xaxis_title="Month"
    )
    fig_roi_progression.update_yaxes(title_text="ROI (%)", secondary_y=False)
    fig_roi_progression.update_yaxes(title_text="Revenue Impact ($)", secondary_y=True)
    
    st.plotly_chart(fig_roi_progression, use_container_width=True)
    
    # Industry benchmarks
    st.subheader("Industry Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        benchmarks = {
            'Our Performance': [16.8, 64, 47, 89],
            'Industry Average': [11.2, 95, 28, 127],
            'Top Quartile': [18.5, 58, 52, 78]
        }
        
        metrics = ['Conversion Rate (%)', 'Sales Cycle (Days)', 'Qualification Rate (%)', 'Cost per Lead ($)']
        
        fig_benchmark = go.Figure()
        
        for company, values in benchmarks.items():
            fig_benchmark.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=company
            ))
        
        fig_benchmark.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 150]
                )),
            showlegend=True,
            title="Performance vs Industry Benchmarks"
        )
        
        st.plotly_chart(fig_benchmark, use_container_width=True)
    
    with col2:
        st.markdown("""
        ### 🏆 Competitive Advantages
        
        **Performance Leadership**
        - 49% above industry average conversion
        - 33% faster sales cycles
        - 68% better lead qualification
        - 30% lower cost per lead
        
        **Technology Edge**
        - Real-time AI scoring
        - Predictive analytics
        - Automated workflows
        - Intelligent routing
        
        **Business Impact**
        - $2.9M annual benefit
        - 340% ROI achievement
        - 3.2 month payback
        - Scalable growth platform
        """)
    
    # Future projections
    st.subheader("Future Growth Projections")
    
    years = ['Year 1 (Current)', 'Year 2', 'Year 3', 'Year 5']
    projected_revenue = [2.1, 3.2, 4.8, 8.5]
    projected_savings = [0.48, 0.75, 1.2, 2.1]
    
    fig_projections = go.Figure()
    
    fig_projections.add_trace(go.Bar(
        name='Revenue Increase (M$)',
        x=years,
        y=projected_revenue,
        marker_color='#4CAF50'
    ))
    
    fig_projections.add_trace(go.Bar(
        name='Cost Savings (M$)',
        x=years,
        y=projected_savings,
        marker_color='#2196F3'
    ))
    
    fig_projections.update_layout(
        title='5-Year Revenue & Savings Projection',
        xaxis_title='Year',
        yaxis_title='Value (Million $)',
        barmode='group'
    )
    
    st.plotly_chart(fig_projections, use_container_width=True)
    
    # Success stories
    st.subheader("Success Stories & Use Cases")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Enterprise Client Success
        
        **Challenge:** 
        Manual lead scoring taking 2+ hours per lead
        
        **Solution:** 
        AI-powered instant scoring & prioritization
        
        **Results:**
        - 95% time reduction in qualification
        - 52% increase in sales team productivity
        - $1.2M additional quarterly revenue
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Fast-Growing Startup
        
        **Challenge:** 
        Scaling sales process with limited resources
        
        **Solution:** 
        Automated workflows & intelligent routing
        
        **Results:**
        - 3x lead processing capacity
        - 40% improvement in conversion
        - Maintained quality with 200% growth
        """)
    
    with col3:
        st.markdown("""
        ### 🏢 Manufacturing Company
        
        **Challenge:** 
        Long sales cycles & complex qualification
        
        **Solution:** 
        Predictive analytics & lead nurturing
        
        **Results:**
        - 35% reduction in sales cycle length
        - 60% better lead qualification accuracy
        - $800K increased annual revenue
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <h4>🎯 Intelligent Sales AI Platform</h4>
    <p>Transforming Sales Performance Through Artificial Intelligence</p>
    <p><strong>Contact:</strong> sales@intelligentsalesai.com | <strong>Support:</strong> support@intelligentsalesai.com</p>
</div>
""", unsafe_allow_html=True)
