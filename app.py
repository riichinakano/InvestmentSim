import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from io import BytesIO
from database import SimulationDB

# ============================
# 翻訳辞書
# ============================
TRANSLATIONS = {
    "English": {
        # Common
        "app_title": "Investment Portfolio Simulator",
        "language": "Language",

        # Tab names
        "tab_investment": "Investment Simulation",
        "tab_lifeplan": "Life Plan",

        # Investment parameters
        "initial_amount": "Initial Investment (JPY)",
        "nisa_contribution": "Annual NISA Investment (JPY)",
        "expected_return": "Expected Return on Risk Assets (%)",
        "risk_ratio": "Risk Asset Allocation (%)",
        "investment_period": "Investment Period (Years)",

        # Asset types
        "risk_asset": "Risk Assets",
        "safe_asset": "Safe Assets",
        "total_asset": "Total Assets",

        # Chart labels
        "year": "Year",
        "years": "Years",
        "amount_jpy": "Amount (JPY)",
        "amount_billion": "Amount (Billion JPY)",

        # Family members
        "husband": "Husband",
        "wife": "Wife",
        "child1": "Child 1",
        "child2": "Child 2",
        "child3": "Child 3",
        "age": "Age",
        "current_age": "Current Age",

        # Life events
        "event_name": "Event Name",
        "event_amount": "Amount (JPY)",
        "add_event": "Add Event",
        "delete_event": "Delete",
        "event_year": "Year",

        # Simulation results
        "simulation_results": "Simulation Results",
        "nisa_cumulative": "NISA Cumulative Investment",
        "nisa_limit_reached": "NISA limit reached in Year",
        "rebalance_amount": "Rebalance Amount",
        "run_simulation": "Run Simulation",
        "before_withdrawal": "Before Withdrawal",
        "after_withdrawal": "After Withdrawal",
        "after_rebalance": "After Rebalance",

        # Export
        "export_csv": "Download CSV",
        "export_excel": "Download Excel",
        "export_success": "Export successful",

        # Database (Phase 2)
        "save_simulation": "Save Simulation",
        "load_simulation": "Load Simulation",
        "simulation_name": "Simulation Name",
        "saved_simulations": "Saved Simulations",
        "delete": "Delete",
        "overwrite": "Overwrite",
        "confirm_delete": "Are you sure you want to delete this simulation?",
        "save_new": "Save as New",
        "no_simulations": "No saved simulations",
        "select_simulation": "Select a simulation to load",
        "simulation_management": "Simulation Management",
        "current_simulation": "Current Simulation",
        "compare_scenarios": "Compare Scenarios",
        "select_scenarios": "Select scenarios to compare (up to 3)",

        # Messages
        "insufficient_funds": "Insufficient funds to cover event expenses",
        "nisa_limit_notice": "NISA investment limit (18M JPY) has been reached",
        "simulation_saved": "Simulation saved successfully",
        "simulation_loaded": "Simulation loaded successfully",
        "simulation_deleted": "Simulation deleted successfully",
        "enter_simulation_name": "Please enter a simulation name",
        "simulation_name_exists": "A simulation with this name already exists",

        # Table headers
        "family_age_table": "Family Age Progression Table",
        "life_event_table": "Life Event Registration",
        "integrated_results": "Integrated Simulation Results",
        "investment_results": "Investment Results Table",
    },
    "日本語": {
        # Common
        "app_title": "資産運用シミュレーター",
        "language": "言語",

        # Tab names
        "tab_investment": "資産運用シミュレーション",
        "tab_lifeplan": "ライフプラン表",

        # Investment parameters
        "initial_amount": "初期投資額（円）",
        "nisa_contribution": "年間NISA投資額（円）",
        "expected_return": "リスク資産の期待リターン（%）",
        "risk_ratio": "リスク資産配分比率（%）",
        "investment_period": "投資期間（年）",

        # Asset types
        "risk_asset": "リスク資産",
        "safe_asset": "安全資産",
        "total_asset": "総資産",

        # Chart labels
        "year": "年",
        "years": "年",
        "amount_jpy": "金額（円）",
        "amount_billion": "金額（億円）",

        # Family members
        "husband": "夫",
        "wife": "妻",
        "child1": "子1",
        "child2": "子2",
        "child3": "子3",
        "age": "年齢",
        "current_age": "現在年齢",

        # Life events
        "event_name": "イベント名",
        "event_amount": "金額（円）",
        "add_event": "イベント追加",
        "delete_event": "削除",
        "event_year": "年",

        # Simulation results
        "simulation_results": "シミュレーション結果",
        "nisa_cumulative": "NISA累積投資額",
        "nisa_limit_reached": "NISA上限到達年",
        "rebalance_amount": "リバランス必要額",
        "run_simulation": "シミュレーション実行",
        "before_withdrawal": "支出前",
        "after_withdrawal": "支出後",
        "after_rebalance": "リバランス後",

        # Export
        "export_csv": "CSVダウンロード",
        "export_excel": "Excelダウンロード",
        "export_success": "エクスポート成功",

        # Database (Phase 2)
        "save_simulation": "シミュレーションを保存",
        "load_simulation": "シミュレーションを読込",
        "simulation_name": "シミュレーション名",
        "saved_simulations": "保存済みシミュレーション",
        "delete": "削除",
        "overwrite": "上書き保存",
        "confirm_delete": "このシミュレーションを削除してもよろしいですか？",
        "save_new": "新規保存",
        "no_simulations": "保存済みシミュレーションがありません",
        "select_simulation": "読み込むシミュレーションを選択",
        "simulation_management": "シミュレーション管理",
        "current_simulation": "現在のシミュレーション",
        "compare_scenarios": "シナリオ比較",
        "select_scenarios": "比較するシナリオを選択（最大3つ）",

        # Messages
        "insufficient_funds": "イベント支出を賄う資産が不足しています",
        "nisa_limit_notice": "NISA投資枠上限（1800万円）に到達しました",
        "simulation_saved": "シミュレーションを保存しました",
        "simulation_loaded": "シミュレーションを読み込みました",
        "simulation_deleted": "シミュレーションを削除しました",
        "enter_simulation_name": "シミュレーション名を入力してください",
        "simulation_name_exists": "同名のシミュレーションが既に存在します",

        # Table headers
        "family_age_table": "家族年齢推移テーブル",
        "life_event_table": "ライフイベント登録",
        "integrated_results": "統合シミュレーション結果",
        "investment_results": "投資結果テーブル",
    }
}

# ============================
# エクスポート関数
# ============================
def export_csv(df, base_filename):
    """Export DataFrame to CSV format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.csv"
    csv = df.to_csv(index=False).encode('utf-8-sig')  # BOM付きUTF-8
    return csv, filename

def export_excel(df, base_filename):
    """Export DataFrame to Excel format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.xlsx"
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Simulation')
        worksheet = writer.sheets['Simulation']
        # 列幅自動調整
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    return buffer.getvalue(), filename

# ============================
# シミュレーション関数
# ============================
def simulate_investment_with_nisa(initial_amount, nisa_contribution, risk_return, risk_ratio, years):
    """
    基本投資シミュレーション（NISA上限管理含む）
    """
    initial_amount = Decimal(str(initial_amount))
    nisa_contribution = Decimal(str(nisa_contribution))
    risk_return = Decimal(str(risk_return))
    risk_ratio = Decimal(str(risk_ratio))
    nisa_limit = Decimal('18000000')  # 1800万円

    results = []
    risk_asset = initial_amount * risk_ratio
    safe_asset = initial_amount * (Decimal('1') - risk_ratio)
    nisa_cumulative = Decimal('0')
    nisa_limit_year = None

    for year in range(1, years + 1):
        # NISA積立（上限チェック）
        remaining_nisa_capacity = nisa_limit - nisa_cumulative

        if remaining_nisa_capacity > 0:
            if nisa_contribution <= remaining_nisa_capacity:
                actual_nisa = nisa_contribution
                nisa_cumulative += nisa_contribution
            else:
                actual_nisa = remaining_nisa_capacity
                nisa_cumulative += remaining_nisa_capacity
                if nisa_limit_year is None:
                    nisa_limit_year = year
        else:
            actual_nisa = Decimal('0')
            if nisa_limit_year is None:
                nisa_limit_year = year

        # リスク資産に積立を追加
        risk_asset += nisa_contribution  # NISA枠使い切った後も通常投資として継続

        # リターン適用
        risk_asset *= (Decimal('1') + risk_return)
        risk_asset = risk_asset.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        total_amount = risk_asset + safe_asset

        results.append({
            'Year': year,
            'Risk Assets (JPY)': int(risk_asset),
            'Safe Assets (JPY)': int(safe_asset),
            'Total (JPY)': int(total_amount),
            'NISA Cumulative (JPY)': int(nisa_cumulative)
        })

        # リバランス
        total_amount = risk_asset + safe_asset
        risk_asset = total_amount * risk_ratio
        safe_asset = total_amount * (Decimal('1') - risk_ratio)

    return pd.DataFrame(results), nisa_limit_year

def simulate_integrated_lifeplan(initial_amount, nisa_contribution, risk_return, risk_ratio, years,
                                  family_ages, life_events):
    """
    ライフプラン統合シミュレーション
    """
    initial_amount = Decimal(str(initial_amount))
    nisa_contribution = Decimal(str(nisa_contribution))
    risk_return = Decimal(str(risk_return))
    risk_ratio = Decimal(str(risk_ratio))
    nisa_limit = Decimal('18000000')

    results = []
    risk_asset = initial_amount * risk_ratio
    safe_asset = initial_amount * (Decimal('1') - risk_ratio)
    nisa_cumulative = Decimal('0')

    # イベントを年でマッピング
    event_map = {event['year']: event for event in life_events}

    for year in range(1, years + 1):
        # 家族の年齢を計算
        current_family_ages = {}
        if family_ages['husband_age'] is not None:
            current_family_ages['husband'] = family_ages['husband_age'] + year - 1
        if family_ages['wife_age'] is not None:
            current_family_ages['wife'] = family_ages['wife_age'] + year - 1
        if family_ages['child1_age'] is not None:
            current_family_ages['child1'] = family_ages['child1_age'] + year - 1
        if family_ages['child2_age'] is not None:
            current_family_ages['child2'] = family_ages['child2_age'] + year - 1
        if family_ages['child3_age'] is not None:
            current_family_ages['child3'] = family_ages['child3_age'] + year - 1

        # NISA積立
        remaining_nisa_capacity = nisa_limit - nisa_cumulative
        if remaining_nisa_capacity > 0:
            if nisa_contribution <= remaining_nisa_capacity:
                nisa_cumulative += nisa_contribution
            else:
                nisa_cumulative += remaining_nisa_capacity

        risk_asset += nisa_contribution

        # リターン適用
        risk_asset *= (Decimal('1') + risk_return)
        risk_asset = risk_asset.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        # イベント支出処理
        event_name = None
        event_amount = Decimal('0')
        if year in event_map:
            event = event_map[year]
            event_name = event['event_name']
            event_amount = Decimal(str(event['amount']))

            # 安全資産から支出
            if safe_asset >= event_amount:
                safe_asset -= event_amount
            else:
                shortage = event_amount - safe_asset
                safe_asset = Decimal('0')
                risk_asset -= shortage

        # リバランス
        total_amount = risk_asset + safe_asset
        target_risk = total_amount * risk_ratio
        target_safe = total_amount * (Decimal('1') - risk_ratio)

        risk_asset = target_risk
        safe_asset = target_safe

        # 結果を追加（登録されている家族のみ）
        result_row = {
            'Year': year,
        }

        if family_ages['husband_age'] is not None:
            result_row['Husband Age'] = current_family_ages['husband']
        if family_ages['wife_age'] is not None:
            result_row['Wife Age'] = current_family_ages['wife']
        if family_ages['child1_age'] is not None:
            result_row['Child1 Age'] = current_family_ages['child1']
        if family_ages['child2_age'] is not None:
            result_row['Child2 Age'] = current_family_ages['child2']
        if family_ages['child3_age'] is not None:
            result_row['Child3 Age'] = current_family_ages['child3']

        result_row.update({
            'Event Name': event_name if event_name else '',
            'Event Amount (JPY)': int(event_amount),
            'Risk Asset (JPY)': int(risk_asset),
            'Safe Asset (JPY)': int(safe_asset),
            'Total Asset (JPY)': int(risk_asset + safe_asset),
            'NISA Cumulative (JPY)': int(nisa_cumulative)
        })

        results.append(result_row)

    return pd.DataFrame(results)

# ============================
# メイン関数
# ============================
def main():
    st.set_page_config(page_title="Investment Portfolio Simulator", layout="wide")

    # データベース初期化
    db = SimulationDB()

    # セッション状態の初期化
    if 'language' not in st.session_state:
        st.session_state.language = "日本語"
    if 'life_events' not in st.session_state:
        st.session_state.life_events = []
    if 'current_simulation_id' not in st.session_state:
        st.session_state.current_simulation_id = None
    if 'current_simulation_name' not in st.session_state:
        st.session_state.current_simulation_name = None

    # 翻訳テキスト
    t = TRANSLATIONS[st.session_state.language]

    # タイトル
    st.title(t["app_title"])

    # サイドバー: 言語選択
    with st.sidebar:
        language = st.selectbox(
            t["language"],
            ["日本語", "English"],
            index=0 if st.session_state.language == "日本語" else 1
        )
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

        st.divider()

        # シミュレーション管理セクション
        st.subheader(t["simulation_management"])

        # 現在のシミュレーション表示
        if st.session_state.current_simulation_name:
            st.info(f"{t['current_simulation']}: {st.session_state.current_simulation_name}")

        # 保存済みシミュレーション一覧
        saved_sims = db.list_simulations()

        if saved_sims:
            sim_options = {f"{sim['name']} ({sim['updated_at'][:16]})": sim['id'] for sim in saved_sims}
            sim_options_list = ["---"] + list(sim_options.keys())

            selected_sim = st.selectbox(
                t["select_simulation"],
                sim_options_list,
                index=0
            )

            col1, col2 = st.columns(2)

            # 読込ボタン
            with col1:
                if st.button(t["load_simulation"], disabled=(selected_sim == "---"), use_container_width=True):
                    sim_id = sim_options[selected_sim]
                    loaded_sim = db.load_simulation(sim_id)

                    if loaded_sim:
                        # パラメータを復元
                        st.session_state.current_simulation_id = sim_id
                        st.session_state.current_simulation_name = loaded_sim['name']
                        st.session_state.life_events = loaded_sim['events']

                        # セッション状態に保存（入力フィールドに反映させるため）
                        for key, value in loaded_sim['params'].items():
                            st.session_state[f'loaded_{key}'] = value

                        st.success(t["simulation_loaded"])
                        st.rerun()

            # 削除ボタン
            with col2:
                if st.button(t["delete"], disabled=(selected_sim == "---"), use_container_width=True):
                    sim_id = sim_options[selected_sim]
                    if db.delete_simulation(sim_id):
                        if st.session_state.current_simulation_id == sim_id:
                            st.session_state.current_simulation_id = None
                            st.session_state.current_simulation_name = None
                        st.success(t["simulation_deleted"])
                        st.rerun()
        else:
            st.info(t["no_simulations"])

        # 保存フォーム
        with st.expander(t["save_simulation"], expanded=False):
            save_name = st.text_input(
                t["simulation_name"],
                value=st.session_state.current_simulation_name or "",
                key="save_name_input"
            )

            col1, col2 = st.columns(2)

            # 新規保存
            with col1:
                save_new_clicked = st.button(t["save_new"], use_container_width=True, key="save_new_btn")

            # 上書き保存
            with col2:
                save_overwrite_clicked = st.button(t["overwrite"], disabled=(st.session_state.current_simulation_id is None), use_container_width=True, key="save_overwrite_btn")

        st.divider()

        # 投資パラメータ
        st.header(t["tab_investment"])

        initial_amount = st.number_input(
            t["initial_amount"],
            min_value=1000000,
            max_value=100000000,
            value=st.session_state.get('loaded_initial_amount', 20000000),
            step=1000000,
            format="%d",
            key="initial_amount_input"
        )

        nisa_contribution = st.number_input(
            t["nisa_contribution"],
            min_value=0,
            max_value=2400000,
            value=st.session_state.get('loaded_nisa_contribution', 1200000),
            step=100000,
            format="%d",
            key="nisa_contribution_input"
        )

        risk_return = st.slider(
            t["expected_return"],
            min_value=0.0,
            max_value=10.0,
            value=st.session_state.get('loaded_risk_return', 0.05) * 100,
            step=0.1,
            key="risk_return_input"
        ) / 100

        risk_ratio = st.slider(
            t["risk_ratio"],
            min_value=0,
            max_value=100,
            value=int(st.session_state.get('loaded_risk_ratio', 0.8) * 100),
            step=5,
            key="risk_ratio_input"
        ) / 100

        years = st.slider(
            t["investment_period"],
            min_value=1,
            max_value=50,
            value=st.session_state.get('loaded_investment_years', 30),
            key="years_input"
        )

    # タブ構成
    tab1, tab2, tab3 = st.tabs([t["tab_investment"], t["tab_lifeplan"], t["compare_scenarios"]])

    # ============================
    # タブ1: 資産運用シミュレーション
    # ============================
    with tab1:
        st.header(t["simulation_results"])

        # シミュレーション実行
        df, nisa_limit_year = simulate_investment_with_nisa(
            initial_amount, nisa_contribution, risk_return, risk_ratio, years
        )

        # NISA情報表示
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t["nisa_cumulative"], f"¥{df['NISA Cumulative (JPY)'].iloc[-1]:,.0f}")
        with col2:
            if nisa_limit_year:
                st.metric(t["nisa_limit_reached"], f"{nisa_limit_year} {t['years']}")
            else:
                st.metric(t["nisa_limit_reached"], "N/A")

        # Plotlyグラフ
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name=t["safe_asset"],
            x=df['Year'],
            y=df['Safe Assets (JPY)'],
            marker_color='lightgreen'
        ))
        fig.add_trace(go.Bar(
            name=t["risk_asset"],
            x=df['Year'],
            y=df['Risk Assets (JPY)'],
            marker_color='lightblue'
        ))

        fig.update_layout(
            barmode='stack',
            xaxis_title=t["years"],
            yaxis_title=t["amount_billion"],
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=500
        )

        # Y軸を億円単位で表示
        fig.update_yaxes(tickformat=".2s")

        st.plotly_chart(fig, use_container_width=True)

        # データテーブル
        st.subheader(t["investment_results"])
        display_df = df.copy()
        display_df.columns = [
            t["year"],
            t["risk_asset"] + " (JPY)",
            t["safe_asset"] + " (JPY)",
            t["total_asset"] + " (JPY)",
            t["nisa_cumulative"] + " (JPY)"
        ]
        st.dataframe(display_df.style.format({
            t["risk_asset"] + " (JPY)": '{:,.0f}',
            t["safe_asset"] + " (JPY)": '{:,.0f}',
            t["total_asset"] + " (JPY)": '{:,.0f}',
            t["nisa_cumulative"] + " (JPY)": '{:,.0f}'
        }), use_container_width=True)

        # エクスポートボタン
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            csv_data, csv_filename = export_csv(df, "investment_simulation")
            st.download_button(
                label=t["export_csv"],
                data=csv_data,
                file_name=csv_filename,
                mime="text/csv"
            )
        with col2:
            excel_data, excel_filename = export_excel(df, "investment_simulation")
            st.download_button(
                label=t["export_excel"],
                data=excel_data,
                file_name=excel_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # ============================
    # タブ2: ライフプラン表
    # ============================
    with tab2:
        st.header(t["tab_lifeplan"])

        # 家族構成入力
        st.subheader(t["family_age_table"])
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            husband_age = st.number_input(
                f"{t['husband']} - {t['current_age']}",
                min_value=0,
                max_value=120,
                value=35,
                step=1
            )
        with col2:
            wife_age = st.number_input(
                f"{t['wife']} - {t['current_age']}",
                min_value=0,
                max_value=120,
                value=33,
                step=1
            )
        with col3:
            child1_age = st.number_input(
                f"{t['child1']} - {t['current_age']}",
                min_value=0,
                max_value=120,
                value=5,
                step=1
            )
        with col4:
            child2_age = st.number_input(
                f"{t['child2']} - {t['current_age']}",
                min_value=0,
                max_value=120,
                value=0,
                step=1
            )
        with col5:
            child3_age = st.number_input(
                f"{t['child3']} - {t['current_age']}",
                min_value=0,
                max_value=120,
                value=0,
                step=1
            )

        family_ages = {
            'husband_age': husband_age if husband_age > 0 else None,
            'wife_age': wife_age if wife_age > 0 else None,
            'child1_age': child1_age if child1_age > 0 else None,
            'child2_age': child2_age if child2_age > 0 else None,
            'child3_age': child3_age if child3_age > 0 else None
        }

        # 家族年齢推移テーブル
        family_age_data = []
        for year in range(1, min(years + 1, 31)):  # 最大30年表示
            row = {'Year': year}
            if family_ages['husband_age']:
                row[t['husband']] = family_ages['husband_age'] + year - 1
            if family_ages['wife_age']:
                row[t['wife']] = family_ages['wife_age'] + year - 1
            if family_ages['child1_age']:
                row[t['child1']] = family_ages['child1_age'] + year - 1
            if family_ages['child2_age']:
                row[t['child2']] = family_ages['child2_age'] + year - 1
            if family_ages['child3_age']:
                row[t['child3']] = family_ages['child3_age'] + year - 1
            family_age_data.append(row)

        family_age_df = pd.DataFrame(family_age_data)
        family_age_df.insert(0, t['year'], family_age_df.pop('Year'))
        st.dataframe(family_age_df, use_container_width=True, height=300)

        st.divider()

        # ライフイベント登録
        st.subheader(t["life_event_table"])

        # イベント追加フォーム
        with st.form("add_event_form"):
            col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
            with col1:
                event_year = st.number_input(t["event_year"], min_value=1, max_value=years, value=1, step=1)
            with col2:
                event_name = st.text_input(t["event_name"], value="")
            with col3:
                event_amount = st.number_input(t["event_amount"], min_value=0, value=0, step=100000, format="%d")
            with col4:
                submitted = st.form_submit_button(t["add_event"])
                if submitted and event_name and event_amount > 0:
                    st.session_state.life_events.append({
                        'year': event_year,
                        'event_name': event_name,
                        'amount': event_amount
                    })
                    st.rerun()

        # 登録済みイベント表示
        if st.session_state.life_events:
            events_df = pd.DataFrame(st.session_state.life_events)
            events_df = events_df.sort_values('year')

            # 子の年齢を追加
            events_display = []
            for idx, event in events_df.iterrows():
                row = {
                    t['event_year']: event['year'],
                    t['event_name']: event['event_name'],
                    t['event_amount']: f"¥{event['amount']:,.0f}"
                }
                events_display.append(row)

            events_display_df = pd.DataFrame(events_display)
            st.dataframe(events_display_df, use_container_width=True)

            # イベント削除ボタン
            if st.button(t["delete_event"] + " (All)"):
                st.session_state.life_events = []
                st.rerun()

        st.divider()

        # 統合シミュレーション実行
        if st.button(t["run_simulation"], type="primary"):
            if st.session_state.life_events:
                result_df = simulate_integrated_lifeplan(
                    initial_amount, nisa_contribution, risk_return, risk_ratio, years,
                    family_ages, st.session_state.life_events
                )

                st.subheader(t["integrated_results"])

                # グラフ表示
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    name=t["safe_asset"],
                    x=result_df['Year'],
                    y=result_df['Safe Asset (JPY)'],
                    marker_color='lightgreen'
                ))
                fig2.add_trace(go.Bar(
                    name=t["risk_asset"],
                    x=result_df['Year'],
                    y=result_df['Risk Asset (JPY)'],
                    marker_color='lightblue'
                ))

                fig2.update_layout(
                    barmode='stack',
                    xaxis_title=t["years"],
                    yaxis_title=t["amount_billion"],
                    hovermode='x unified',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    height=500
                )

                fig2.update_yaxes(tickformat=".2s")
                st.plotly_chart(fig2, use_container_width=True)

                # 詳細データテーブル（日本語表示）
                st.subheader(t["investment_results"])

                # 列名を翻訳
                display_result_df = result_df.copy()
                column_mapping = {
                    'Year': t['year'],
                    'Husband Age': t['husband'] + ' ' + t['age'],
                    'Wife Age': t['wife'] + ' ' + t['age'],
                    'Child1 Age': t['child1'] + ' ' + t['age'],
                    'Child2 Age': t['child2'] + ' ' + t['age'],
                    'Child3 Age': t['child3'] + ' ' + t['age'],
                    'Event Name': t['event_name'],
                    'Event Amount (JPY)': t['event_amount'],
                    'Risk Asset (JPY)': t['risk_asset'] + ' (JPY)',
                    'Safe Asset (JPY)': t['safe_asset'] + ' (JPY)',
                    'Total Asset (JPY)': t['total_asset'] + ' (JPY)',
                    'NISA Cumulative (JPY)': t['nisa_cumulative'] + ' (JPY)'
                }

                # 存在する列のみリネーム
                rename_dict = {k: v for k, v in column_mapping.items() if k in display_result_df.columns}
                display_result_df.rename(columns=rename_dict, inplace=True)

                # 数値フォーマット
                format_dict = {}
                for col in display_result_df.columns:
                    if '(JPY)' in col:
                        format_dict[col] = '{:,.0f}'

                st.dataframe(display_result_df.style.format(format_dict), use_container_width=True, height=400)

                # エクスポートボタン
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    csv_data, csv_filename = export_csv(result_df, "lifeplan_simulation")
                    st.download_button(
                        label=t["export_csv"],
                        data=csv_data,
                        file_name=csv_filename,
                        mime="text/csv"
                    )
                with col2:
                    excel_data, excel_filename = export_excel(result_df, "lifeplan_simulation")
                    st.download_button(
                        label=t["export_excel"],
                        data=excel_data,
                        file_name=excel_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning(t["add_event"])

    # ============================
    # タブ3: シナリオ比較
    # ============================
    with tab3:
        st.header(t["compare_scenarios"])

        # 保存済みシミュレーション取得
        saved_sims = db.list_simulations()

        if len(saved_sims) < 2:
            st.info(t["select_scenarios"])
            st.warning("比較するには少なくとも2つのシミュレーションが必要です。" if st.session_state.language == "日本語" else "At least 2 simulations are required for comparison.")
        else:
            # シミュレーション選択
            st.subheader(t["select_scenarios"])

            col1, col2, col3 = st.columns(3)

            sim_names = [f"{sim['name']}" for sim in saved_sims]
            sim_ids = [sim['id'] for sim in saved_sims]

            with col1:
                scenario1_idx = st.selectbox(
                    "シナリオ 1" if st.session_state.language == "日本語" else "Scenario 1",
                    range(len(sim_names)),
                    format_func=lambda x: sim_names[x],
                    key="scenario1"
                )

            with col2:
                scenario2_idx = st.selectbox(
                    "シナリオ 2" if st.session_state.language == "日本語" else "Scenario 2",
                    range(len(sim_names)),
                    format_func=lambda x: sim_names[x],
                    index=min(1, len(sim_names) - 1),
                    key="scenario2"
                )

            with col3:
                scenario3_idx = st.selectbox(
                    "シナリオ 3 (オプション)" if st.session_state.language == "日本語" else "Scenario 3 (Optional)",
                    [-1] + list(range(len(sim_names))),
                    format_func=lambda x: "---" if x == -1 else sim_names[x],
                    key="scenario3"
                )

            # 比較実行ボタン
            if st.button("比較実行" if st.session_state.language == "日本語" else "Run Comparison", type="primary"):
                # シナリオを読み込み
                scenarios = []

                for idx in [scenario1_idx, scenario2_idx, scenario3_idx]:
                    if idx >= 0:
                        sim_data = db.load_simulation(sim_ids[idx])
                        if sim_data:
                            scenarios.append(sim_data)

                if len(scenarios) >= 2:
                    # 各シナリオのシミュレーション実行
                    results = []

                    for scenario in scenarios:
                        params = scenario['params']
                        events = scenario['events']

                        # シミュレーション実行
                        if events:
                            family_ages = {
                                'husband_age': params.get('husband_age'),
                                'wife_age': params.get('wife_age'),
                                'child1_age': params.get('child1_age'),
                                'child2_age': params.get('child2_age'),
                                'child3_age': params.get('child3_age')
                            }

                            df = simulate_integrated_lifeplan(
                                params['initial_amount'],
                                params['nisa_contribution'],
                                params['risk_return'],
                                params['risk_ratio'],
                                params['investment_years'],
                                family_ages,
                                events
                            )
                        else:
                            df, _ = simulate_investment_with_nisa(
                                params['initial_amount'],
                                params['nisa_contribution'],
                                params['risk_return'],
                                params['risk_ratio'],
                                params['investment_years']
                            )

                        results.append({
                            'name': scenario['name'],
                            'df': df
                        })

                    # 比較グラフ作成
                    st.subheader("総資産推移の比較" if st.session_state.language == "日本語" else "Total Asset Comparison")

                    fig_compare = go.Figure()

                    colors = ['blue', 'red', 'green']

                    for i, result in enumerate(results):
                        df = result['df']
                        name = result['name']

                        # 総資産列を取得
                        if 'Total Asset (JPY)' in df.columns:
                            total_col = 'Total Asset (JPY)'
                        else:
                            total_col = 'Total (JPY)'

                        fig_compare.add_trace(go.Scatter(
                            x=df['Year'],
                            y=df[total_col],
                            mode='lines+markers',
                            name=name,
                            line=dict(color=colors[i], width=2),
                            marker=dict(size=6)
                        ))

                    fig_compare.update_layout(
                        xaxis_title=t["years"],
                        yaxis_title=t["amount_billion"],
                        hovermode='x unified',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=500
                    )

                    fig_compare.update_yaxes(tickformat=".2s")
                    st.plotly_chart(fig_compare, use_container_width=True)

                    # 最終年の比較テーブル
                    st.subheader("最終年度の資産比較" if st.session_state.language == "日本語" else "Final Year Asset Comparison")

                    comparison_data = []
                    for result in results:
                        df = result['df']
                        last_row = df.iloc[-1]

                        if 'Total Asset (JPY)' in df.columns:
                            total_col = 'Total Asset (JPY)'
                            risk_col = 'Risk Asset (JPY)'
                            safe_col = 'Safe Asset (JPY)'
                        else:
                            total_col = 'Total (JPY)'
                            risk_col = 'Risk Assets (JPY)'
                            safe_col = 'Safe Assets (JPY)'

                        comparison_data.append({
                            t['simulation_name']: result['name'],
                            t['total_asset']: f"¥{last_row[total_col]:,.0f}",
                            t['risk_asset']: f"¥{last_row[risk_col]:,.0f}",
                            t['safe_asset']: f"¥{last_row[safe_col]:,.0f}"
                        })

                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True)

    # 保存処理（サイドバーのボタンが押された場合）
    if 'save_new_clicked' in locals() and save_new_clicked:
        if not save_name:
            st.error(t["enter_simulation_name"])
        elif db.simulation_exists(save_name):
            st.error(t["simulation_name_exists"])
        else:
            # パラメータを収集
            params = {
                'initial_amount': initial_amount,
                'nisa_contribution': nisa_contribution,
                'risk_return': risk_return,
                'risk_ratio': risk_ratio,
                'investment_years': years,
                'husband_age': None,
                'wife_age': None,
                'child1_age': None,
                'child2_age': None,
                'child3_age': None,
                'language': st.session_state.language
            }

            # 保存
            sim_id = db.save_simulation(save_name, params, st.session_state.life_events)
            st.session_state.current_simulation_id = sim_id
            st.session_state.current_simulation_name = save_name
            st.success(t["simulation_saved"])
            st.rerun()

    if 'save_overwrite_clicked' in locals() and save_overwrite_clicked:
        if not save_name:
            st.error(t["enter_simulation_name"])
        else:
            # パラメータを収集
            params = {
                'initial_amount': initial_amount,
                'nisa_contribution': nisa_contribution,
                'risk_return': risk_return,
                'risk_ratio': risk_ratio,
                'investment_years': years,
                'husband_age': None,
                'wife_age': None,
                'child1_age': None,
                'child2_age': None,
                'child3_age': None,
                'language': st.session_state.language
            }

            # 上書き保存
            db.save_simulation(save_name, params, st.session_state.life_events, st.session_state.current_simulation_id)
            st.session_state.current_simulation_name = save_name
            st.success(t["simulation_saved"])
            st.rerun()

if __name__ == "__main__":
    main()
