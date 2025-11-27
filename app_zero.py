import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

def simulate_investment(initial_amount, nisa_contribution, risk_return, risk_ratio, years):
    """Investment simulation calculation function"""
    
    initial_amount = Decimal(str(initial_amount))
    nisa_contribution = Decimal(str(nisa_contribution))
    risk_return = Decimal(str(risk_return))
    risk_ratio = Decimal(str(risk_ratio))
    
    results = []
    risk_asset = initial_amount * risk_ratio
    safe_asset = initial_amount * (Decimal('1') - risk_ratio)
    
    for year in range(1, years + 1):
        risk_asset += nisa_contribution
        risk_asset *= (Decimal('1') + risk_return)
        risk_asset = risk_asset.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        
        total_amount = risk_asset + safe_asset
        
        results.append({
            'Year': year,
            'Risk Assets (JPY)': int(risk_asset),
            'Safe Assets (JPY)': int(safe_asset),
            'Total (JPY)': int(total_amount)
        })

        total_amount = risk_asset + safe_asset
        risk_asset = total_amount * risk_ratio
        safe_asset = total_amount * (Decimal('1') - risk_ratio)
    
    return pd.DataFrame(results)

def simulate_withdrawal(total_amount, withdrawal_years, withdrawal_rate):
    """Withdrawal simulation function"""
    
    results = []
    remaining_amount = total_amount
    
    for year in range(1, withdrawal_years + 1):
        withdrawal_amount = remaining_amount * (withdrawal_rate / 100)
        remaining_amount = remaining_amount - withdrawal_amount
        
        results.append({
            'Year': year,
            'Withdrawal': int(withdrawal_amount),
            'Remaining': int(remaining_amount)
        })
    
    return pd.DataFrame(results)

def main():
    st.set_page_config(page_title="Investment Portfolio Simulator", layout="wide")
    
    st.title("Investment Portfolio Simulator")
    
    # 資産形成シミュレーションのパラメータ
    with st.sidebar:
        st.header("Investment Parameters")
        initial_amount = st.number_input(
            "Initial Investment (JPY)",
            min_value=1000000,
            max_value=100000000,
            value=20000000,
            step=1000000,
            format="%d"
        )
        
        nisa_contribution = st.number_input(
            "Annual NISA Investment (JPY)",
            min_value=0,
            max_value=2400000,
            value=1200000,
            step=100000,
            format="%d"
        )
        
        risk_return = st.slider(
            "Expected Return on Risk Assets (%)",
            min_value=0.0,
            max_value=10.0,
            value=5.0,
            step=0.1
        ) / 100
        
        risk_ratio = st.slider(
            "Risk Asset Allocation (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=5
        ) / 100
        
        years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=50,
            value=30
        )

    # 資産形成シミュレーション実行
    df = simulate_investment(initial_amount, nisa_contribution, risk_return, risk_ratio, years)
    
    # 資産形成シミュレーショングラフ
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.bar(df['Year'], df['Risk Assets (JPY)'], label='Risk Assets', color='lightblue')
    ax1.bar(df['Year'], df['Safe Assets (JPY)'], bottom=df['Risk Assets (JPY)'],
           label='Safe Assets', color='lightgreen')
    
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/100000000:.1f}B'))
    plt.title(f'Investment Portfolio Simulation\n(Initial: {initial_amount/1000000:.0f}M, NISA: {nisa_contribution/10000:.0f}0K/year\nReturn: {risk_return*100:.1f}%, Risk Ratio: {risk_ratio*100:.0f}%)')
    plt.xlabel('Years')
    plt.ylabel('Amount (JPY)')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig1)
    
    st.header("Investment Results")
    st.dataframe(df.style.format({
        'Risk Assets (JPY)': '{:,.0f}',
        'Safe Assets (JPY)': '{:,.0f}',
        'Total (JPY)': '{:,.0f}'
    }))

    # 取崩しシミュレーション
    st.header("Withdrawal Strategy Simulation")
    
    col1, col2 = st.columns(2)
    with col1:
        withdrawal_years = st.slider(
            "Withdrawal Period (Years)",
            min_value=1,
            max_value=40,
            value=20,
            help="Expected remaining lifespan"
        )
    
    with col2:
        withdrawal_rate = st.slider(
            "Annual Withdrawal Rate (%)",
            min_value=1.0,
            max_value=20.0,
            value=4.0,
            step=0.1,
            help="Percentage of total assets to withdraw each year"
        )

    if st.button("Run Withdrawal Simulation"):
        total_amount = df['Total (JPY)'].iloc[-1]
        withdrawal_df = simulate_withdrawal(total_amount, withdrawal_years, withdrawal_rate)
        
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(withdrawal_df['Year'], withdrawal_df['Remaining'], 
                label='Remaining Assets', color='blue')
        ax2.bar(withdrawal_df['Year'], withdrawal_df['Withdrawal'], 
               alpha=0.3, label='Annual Withdrawal', color='green')
        
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/100000000:.1f}B'))
        plt.title(f'Withdrawal Simulation\n(Initial: {total_amount/100000000:.1f}B, Rate: {withdrawal_rate}%/year)')
        plt.xlabel('Years')
        plt.ylabel('Amount (JPY)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        st.pyplot(fig2)
        
        st.subheader("Withdrawal Details")
        st.dataframe(withdrawal_df.style.format({
            'Withdrawal': '{:,.0f}',
            'Remaining': '{:,.0f}'
        }))
        
        final_balance = withdrawal_df['Remaining'].iloc[-1]
        st.metric("Final Balance", f"¥{final_balance:,.0f}")

if __name__ == "__main__":
    main()
    