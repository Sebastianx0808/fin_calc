import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(page_title="Financial Calculators", layout="wide")

def create_pie_chart(invested_amount, total_interest, title):
    total = invested_amount + total_interest
    invested_percent = (invested_amount/total) * 100
    interest_percent = (total_interest/total) * 100

    fig = go.Figure(data = [go.Pie(
        labels = ['Invested Amount', 'Total Interest'],
        values = [invested_amount, total_interest],
        hole = .6,
        marker_colors = ['#3366cc', '#708090'],
        marker=dict(
            line=dict(color='#ffffff', width=3)
        ),
        textfont = dict(size=14, color='white'),
        hovertemplate= "<b>%{label}</b><br>" +
                     "Amount: ₹%{value:,.2f}<br>" +
                     "Percentage: %{percent:.1f}%<br>" +
                     "<extra></extra>",
        rotation=90,
    )])

    fig.update_layout(
        title=dict(
            text=title,
            y=0.95,  # Title positiondir
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(
                size=24,
                color='#FFFFFF',
                family='Arial Black'
            )
        ),
        # Adding subtle shadow effect using shapes
        shapes=[dict(
            type='circle',
            xref='paper',
            yref='paper',
            x0=0.1,
            y0=0.1,
            x1=0.9,
            y1=0.9,
            fillcolor='rgba(0,0,0,0.1)',
            line_width=0,
            layer='below'
        )],
        height=500,  # Increased height
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        paper_bgcolor='rgba(255,255,255,0)',  # Transparent background
        plot_bgcolor='rgba(255,255,255,0)',
        # Adding annotations for total value
        annotations=[
            dict(
                text=f'Total Value<br>₹{invested_amount + total_interest:,.0f}',
                x=0.5,
                y=0.5,
                font=dict(size=16, color='#FFFFFF'),
                showarrow=False
            )
        ]
    )
    
    # Add gradient and shadow effects
    fig.update_traces(
        marker=dict(
            colors=['#3366cc', '#708090'],
            pattern=dict(
                shape="",
                solidity=0.1
            )
        ),
        
    )
    
    return fig

# Lambda functions for calculations
calculate_ppf = lambda p, n, i: {
    'invested_amount': p * n,
    'maturity_value': p * ((pow(1 + i/100, n) - 1) / (i/100)),
    'total_interest': (p * ((pow(1 + i/100, n) - 1) / (i/100))) - (p * n)
}

calculate_fd_compound = lambda p, r, t: {
    'invested_amount': p,
    'maturity_value': p * pow(1 + r/100, t),
    'total_interest': (p * pow(1 + r/100, t)) - p
}

calculate_fd_simple = lambda p, r, t: {
    'invested_amount': p,
    'maturity_value': p * (1 + (r * t)/100),
    'total_interest': (p * (r * t)/100)
}

calculate_sip = lambda p, r, t: {
    'invested_amount': p * t * 12,
    'maturity_value': p * ((pow(1 + (r/(12*100)), t*12) - 1) / (r/(12*100))) * (1 + r/(12*100)),
    'total_interest': (p * ((pow(1 + (r/(12*100)), t*12) - 1) / (r/(12*100))) * (1 + r/(12*100))) - (p * t * 12)
}

calculate_rd = lambda p, r, t: {
    'invested_amount': p * t * 12,
    'maturity_value': sum(p * (1 + r/(4*100))**(4 * (t - i/12)) for i in range(t*12)),
    'total_interest': sum(p * (1 + r/(4*100))**(4 * (t - i/12)) for i in range(t*12)) - (p * t * 12)
}

# Main app
st.title("Financial Calculators")

# Create tabs for different calculators
calculator_type = st.sidebar.radio(
    "Select Calculator",
    ["PPF Calculator", "Fixed Deposit Calculator", "SIP Calculator", "RD Calculator"]
)

if calculator_type == "PPF Calculator":
    st.header("PPF Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        yearly_investment = st.slider("Yearly Investment (₹)", 500, 1000000, 150000, 500)
        time_period = st.slider("Time Period (Years)", 1, 30, 15, 1)
        st.write("Rate of Interest: 7.1%")
        
        result = calculate_ppf(yearly_investment, time_period, 7.1)
        
        st.subheader("Results")
        st.write(f"Invested Amount: ₹{result['invested_amount']:,.2f}")
        st.write(f"Total Interest: ₹{result['total_interest']:,.2f}")
        st.write(f"Maturity Value: ₹{result['maturity_value']:,.2f}")
    
    with col2:
        st.plotly_chart(create_pie_chart(
            result['invested_amount'],
            result['total_interest'],
            "PPF Investment Breakdown"
        ))

elif calculator_type == "Fixed Deposit Calculator":
    st.header("Fixed Deposit Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        total_investment = st.slider("Total Investment (₹)", 1000, 1000000, 100000, 1000)
        rate_of_interest = st.slider("Rate of Interest (%)", 1.0, 15.0, 10.0, 0.1)
        time_period = st.slider("Time Period (Years)", 1, 10, 5, 1)
        interest_type = st.radio("Interest Type", ["Simple", "Compound"])
        
        result = (calculate_fd_compound if interest_type == "Compound" else calculate_fd_simple)(
            total_investment, rate_of_interest, time_period
        )
        
        st.subheader("Results")
        st.write(f"Invested Amount: ₹{result['invested_amount']:,.2f}")
        st.write(f"Total Interest: ₹{result['total_interest']:,.2f}")
        st.write(f"Maturity Value: ₹{result['maturity_value']:,.2f}")
    
    with col2:
        st.plotly_chart(create_pie_chart(
            result['invested_amount'],
            result['total_interest'],
            "FD Investment Breakdown"
        ))

elif calculator_type == "SIP Calculator":
    st.header("SIP Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Modified SIP calculator with new requirements
        monthly_investment = st.slider(
            "Monthly Investment (₹)", 
            min_value=1000,          # Changed minimum to 1000
            max_value=500000,        # Reasonable maximum value
            value=5000,              # Default value
            step=1000                # Step value of 1000
        )
        return_rate = st.slider("Expected Return Rate (% p.a)", 8.0, 20.0, 12.0, 0.1)
        time_period = st.slider("Time Period (Years)", 1, 30, 5, 1)
        
        result = calculate_sip(monthly_investment, return_rate, time_period)
        
        st.subheader("Results")
        st.write(f"Invested Amount: ₹{result['invested_amount']:,.2f}")
        st.write(f"Total Interest: ₹{result['total_interest']:,.2f}")
        st.write(f"Maturity Value: ₹{result['maturity_value']:,.2f}")
        
        # Additional monthly breakdown
        st.subheader("Monthly Breakdown")
        st.write(f"Monthly Investment: ₹{monthly_investment:,.2f}")
        st.write(f"Average Monthly Interest: ₹{(result['total_interest']/(time_period*12)):,.2f}")
    
    with col2:
        st.plotly_chart(create_pie_chart(
            result['invested_amount'],
            result['total_interest'],
            "SIP Investment Breakdown"
        ))

else:  # RD Calculator
    st.header("RD Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_investment = st.slider("Monthly Investment (₹)", 100, 100000, 5000, 100)
        rate_of_interest = st.slider("Rate of Interest (% p.a)", 1.0, 15.0, 8.0, 0.1)
        time_period = st.slider("Time Period (Years)", 1, 10, 1, 1)
        
        result = calculate_rd(monthly_investment, rate_of_interest, time_period)
        
        st.subheader("Results")
        st.write(f"Invested Amount: ₹{result['invested_amount']:,.2f}")
        st.write(f"Total Interest: ₹{result['total_interest']:,.2f}")
        st.write(f"Maturity Value: ₹{result['maturity_value']:,.2f}")
    
    with col2:
        st.plotly_chart(create_pie_chart(
            result['invested_amount'],
            result['total_interest'],
            "RD Investment Breakdown"
        ))