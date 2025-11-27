# 要件定義書：ライフプラン統合型資産運用シミュレーター

## 1. プロジェクト概要

### 1.1 目的
既存の資産運用シミュレーターに家族のライフイベントを統合し、実際の支出計画を考慮した長期資産形成シミュレーションを実現する。

### 1.2 対象ユーザー
- 長期資産形成を計画している個人・家族
- 子どもの教育資金や住宅購入など、大型支出を伴うライフイベントを控えている世帯
- NISA制度を活用した投資を検討している人

### 1.3 主要な改善点
- 家族構成の入力と年齢自動計算機能
- ライフイベントと支出の登録・管理機能
- イベント支出を考慮した資産シミュレーション
- リバランス必要額の可視化
- NISA枠上限（1800万円）の管理
- **多言語対応（日本語・英語切替）機能**
- **データエクスポート機能（CSV/XLSX）**
- **データベース保存・読込機能（Phase 2）**

---

## 2. 機能要件

### 2.1 画面構成

#### 2.1.1 タブ構成
```
共通UI要素: 言語選択（サイドバー最上部）
  - 選択肢: "English" / "日本語"
  - デフォルト: "日本語"

タブ1: 資産運用シミュレーション
タブ2: ライフプラン表
```

#### 2.1.2 タブ1: 資産運用シミュレーション
**目的**: 基本的な投資パラメータを設定し、資産形成の基礎シミュレーションを実行

**サイドバー（入力項目）**:
- 初期投資額（JPY）: 1,000,000 ～ 100,000,000、デフォルト 20,000,000
- 年間NISA投資額（JPY）: 0 ～ 2,400,000、デフォルト 1,200,000
- リスク資産の期待リターン（%）: 0.0 ～ 10.0、デフォルト 5.0
- リスク資産配分比率（%）: 0 ～ 100、デフォルト 80
- 投資期間（年）: 1 ～ 50、デフォルト 30

**メインエリア（表示内容）**:
- 積上げ棒グラフ（リスク資産・安全資産の推移）
- 年次データテーブル（年、リスク資産額、安全資産額、総資産額）
- NISA累積投資額の表示
- NISA上限到達年の表示（該当する場合）
- **エクスポートボタン**:
  - 「CSV形式でダウンロード」ボタン
  - 「Excel形式でダウンロード」ボタン

#### 2.1.3 タブ2: ライフプラン表
**目的**: 家族構成とライフイベントを入力し、支出を反映した統合シミュレーションを実行

**サイドバー（入力項目）**:
- 家族構成入力
  - 夫: 現在年齢（入力フィールド）
  - 妻: 現在年齢（入力フィールド）
  - 子1: 現在年齢（入力フィールド、オプション）
  - 子2: 現在年齢（入力フィールド、オプション）
  - 子3: 現在年齢（入力フィールド、オプション）

**メインエリア（表示内容）**:
1. **家族年齢推移テーブル**
   - 列: シミュレーション年、夫年齢、妻年齢、子1年齢、子2年齢、子3年齢

2. **ライフイベント登録テーブル**
   - 列: 年（ドロップダウン）、子の年齢（該当年の自動表示）、イベント名（自由入力）、金額（JPY）
   - 編集可能なテーブル形式
   - 行の追加・削除機能

3. **統合シミュレーション実行ボタン**

4. **統合シミュレーション結果**
   - 調整後資産推移グラフ（積上げ棒グラフ）
   - 詳細データテーブル（日本語・英語対応）:
     - 年
     - 家族の年齢（登録されている家族メンバーのみ表示）
     - イベント名
     - イベント支出額
     - リスク資産額
     - 安全資産額
     - 総資産額
     - NISA累積投資額
   - **エクスポートボタン**:
     - 「CSV形式でダウンロード」ボタン
     - 「Excel形式でダウンロード」ボタン

---

## 3. データ構造

### 3.1 多言語対応

#### 3.1.1 言語選択
```python
AVAILABLE_LANGUAGES = ["English", "日本語"]
```

#### 3.1.2 翻訳辞書構造
```python
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
        
        # Simulation results
        "simulation_results": "Simulation Results",
        "nisa_cumulative": "NISA Cumulative Investment",
        "nisa_limit_reached": "NISA limit reached in Year",
        "rebalance_amount": "Rebalance Amount",
        "run_simulation": "Run Simulation",
        
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
        
        # Messages
        "insufficient_funds": "Insufficient funds to cover event expenses",
        "nisa_limit_notice": "NISA investment limit (18M JPY) has been reached",
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
        
        # Simulation results
        "simulation_results": "シミュレーション結果",
        "nisa_cumulative": "NISA累積投資額",
        "nisa_limit_reached": "NISA上限到達年",
        "rebalance_amount": "リバランス必要額",
        "run_simulation": "シミュレーション実行",
        
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
        
        # Messages
        "insufficient_funds": "イベント支出を賄う資産が不足しています",
        "nisa_limit_notice": "NISA投資枠上限（1800万円）に到達しました",
    }
}
```

### 3.2 家族構成データ
```python
{
    "husband_age": int,
    "wife_age": int,
    "child1_age": int | None,
    "child2_age": int | None,
    "child3_age": int | None
}
```

### 3.2 家族構成データ
```python
{
    "husband_age": int,
    "wife_age": int,
    "child1_age": int | None,
    "child2_age": int | None,
    "child3_age": int | None
}
```

### 3.3 ライフイベントデータ
```python
[
    {
        "year": int,              # シミュレーション開始からの経過年数
        "event_name": str,        # イベント名（自由入力）
        "amount": int             # 支出金額（JPY）
    },
    ...
]
```

### 3.4 年次シミュレーションデータ（簡略化）
```python
{
    "year": int,
    "family_ages": {
        "husband": int | None,        # 登録されている場合のみ
        "wife": int | None,           # 登録されている場合のみ
        "child1": int | None,         # 登録されている場合のみ
        "child2": int | None,         # 登録されている場合のみ
        "child3": int | None,         # 登録されている場合のみ
    },
    "event": {
        "name": str | None,
        "amount": int
    },
    "risk_asset": Decimal,            # イベント支出・リバランス後のリスク資産
    "safe_asset": Decimal,            # イベント支出・リバランス後の安全資産
    "total_asset": Decimal,           # 総資産
    "nisa_cumulative": Decimal        # NISA累積投資額
}
```

**変更理由**: 支出前/後、リバランス前/後の詳細表示は複雑すぎるため、最終的な資産状態のみを表示するようシンプル化しました。

---

## 4. エクスポート・データ管理機能

### 4.1 データエクスポート機能（Phase 1）

#### 4.1.1 エクスポート対象
- タブ1: 資産運用シミュレーション結果テーブル
- タブ2: ライフプラン統合シミュレーション結果テーブル

#### 4.1.2 エクスポート形式
**CSV形式**:
- 文字エンコーディング: UTF-8 with BOM（Excelで文字化け防止）
- ファイル名形式: `investment_simulation_YYYYMMDD_HHMMSS.csv`

**Excel形式**:
- フォーマット: .xlsx (Excel 2007以降)
- ファイル名形式: `investment_simulation_YYYYMMDD_HHMMSS.xlsx`
- 列幅: 自動調整
- 数値フォーマット: カンマ区切り

#### 4.1.3 実装方法
```python
import pandas as pd
from io import BytesIO
from datetime import datetime

# CSV エクスポート
def export_csv(df, base_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.csv"
    csv = df.to_csv(index=False).encode('utf-8-sig')  # BOM付きUTF-8
    return csv, filename

# Excel エクスポート
def export_excel(df, base_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_filename}_{timestamp}.xlsx"
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Simulation')
        worksheet = writer.sheets['Simulation']
        # 列幅自動調整
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            worksheet.column_dimensions[column[0].column_letter].width = max_length + 2
    return buffer.getvalue(), filename

# Streamlit実装
st.download_button(
    label="📥 Download CSV",
    data=csv_data,
    file_name=csv_filename,
    mime="text/csv"
)
```

### 4.2 データベース機能（Phase 2）

#### 4.2.1 目的
- シミュレーション設定の保存・読込
- 複数シナリオの管理
- 過去のシミュレーション履歴の参照

#### 4.2.2 使用技術
- **データベース**: SQLite3（Python標準ライブラリ）
- **ファイル**: `simulations.db`（アプリと同じディレクトリ）
- **ORM**: 使用しない（直接SQL実行でシンプルに保持）

#### 4.2.3 データベーススキーマ

**テーブル1: simulations（シミュレーション基本情報）**
```sql
CREATE TABLE simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Investment parameters
    initial_amount INTEGER NOT NULL,
    nisa_contribution INTEGER NOT NULL,
    risk_return REAL NOT NULL,
    risk_ratio REAL NOT NULL,
    investment_years INTEGER NOT NULL,
    -- Family composition
    husband_age INTEGER,
    wife_age INTEGER,
    child1_age INTEGER,
    child2_age INTEGER,
    child3_age INTEGER,
    -- Metadata
    language TEXT DEFAULT 'ja'
);
```

**テーブル2: life_events（ライフイベント）**
```sql
CREATE TABLE life_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    event_name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE
);
```

#### 4.2.4 機能仕様

**保存機能**:
- UI: サイドバーに「💾 シミュレーションを保存」ボタン
- 動作:
  1. シミュレーション名入力ダイアログ表示
  2. 現在の設定を全てDBに保存
  3. 成功メッセージ表示

**読込機能**:
- UI: サイドバーに「📂 保存済みシミュレーション」セレクトボックス
- 表示: シミュレーション名一覧（作成日時順）
- 動作:
  1. ユーザーが選択
  2. DBから設定を読み込み
  3. 全入力フィールドに反映
  4. 自動的にシミュレーション実行

**削除機能**:
- UI: 各シミュレーションの横に「🗑️ 削除」ボタン
- 動作:
  1. 確認ダイアログ表示
  2. 関連する全データを削除（CASCADE）

**上書き保存機能**:
- UI: 読込済みシミュレーションの場合、「💾 上書き保存」ボタン表示
- 動作: 同じIDのレコードを更新

#### 4.2.5 データベース操作モジュール
```python
# database.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

class SimulationDB:
    def __init__(self, db_path='simulations.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables (SQL as shown above)
        cursor.execute('''CREATE TABLE IF NOT EXISTS simulations ...''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS life_events ...''')
        
        conn.commit()
        conn.close()
    
    def save_simulation(self, name: str, params: Dict, events: List[Dict]) -> int:
        """Save simulation to database"""
        # Implementation
        pass
    
    def load_simulation(self, simulation_id: int) -> Dict:
        """Load simulation from database"""
        # Implementation
        pass
    
    def list_simulations(self) -> List[Dict]:
        """Get list of all simulations"""
        # Implementation
        pass
    
    def delete_simulation(self, simulation_id: int):
        """Delete simulation"""
        # Implementation
        pass
```

#### 4.2.6 UI配置（Phase 2）
サイドバー構成:
```
[言語選択]
─────────────
[シミュレーション管理]
  💾 シミュレーションを保存
  📂 保存済みシミュレーション
     └─ [セレクトボックス]
     └─ 🗑️ 削除ボタン
─────────────
[投資パラメータ]
  ...
```

---

## 5. ビジネスロジック

### 5.1 基本投資シミュレーション（タブ1）
既存ロジックを維持：
1. 初期資産をリスク・安全比率で配分
2. 毎年NISA積立をリスク資産に追加
3. リスク資産に期待リターンを適用
4. 年末にリバランス実行

**追加要件**:
- NISA累積投資額を追跡
- 1,800万円到達後は通常投資扱い（リターンは同じ）
- 上限到達年を表示

### 5.2 統合シミュレーション（タブ2）

#### 5.2.1 年次処理フロー（簡略化版）
```
各年について:
  1. NISA積立実行（上限チェック）
  2. リスク資産にリターン適用
  3. イベント支出処理
     a. 該当年のイベントを確認
     b. 安全資産から支出
     c. 不足時はリスク資産から補填
  4. リバランス処理
     a. 現在の資産比率を計算
     b. 目標比率に基づいてリスク・安全資産を調整
  5. 年末の資産状態を記録（リスク資産、安全資産、総資産、NISA累積額のみ）
```

**変更理由**: 支出前/後の詳細記録を省略し、最終的な資産状態のみを記録することでシンプル化しました。

#### 5.2.2 支出処理ロジック
```python
def process_event_withdrawal(risk_asset, safe_asset, event_amount):
    """
    イベント支出を処理
    優先順位: 安全資産 → リスク資産
    """
    if safe_asset >= event_amount:
        safe_asset -= event_amount
    else:
        shortage = event_amount - safe_asset
        safe_asset = Decimal('0')
        risk_asset -= shortage
        if risk_asset < 0:
            # 警告: 資産不足
            raise InsufficientFundsError
    
    return risk_asset, safe_asset
```

#### 5.2.3 リバランス処理ロジック（簡略化）
```python
def rebalance_assets(risk_asset, safe_asset, target_risk_ratio):
    """
    年末リバランス実行
    目標比率に基づいて資産を調整
    """
    total = risk_asset + safe_asset
    target_risk = total * target_risk_ratio
    target_safe = total * (Decimal('1') - target_risk_ratio)

    risk_asset = target_risk
    safe_asset = target_safe

    return risk_asset, safe_asset
```

**変更理由**: リバランス必要額の記録を削除し、処理をシンプル化しました。

#### 5.2.4 NISA上限管理
```python
def apply_nisa_contribution(risk_asset, nisa_contribution, nisa_cumulative, nisa_limit=18000000):
    """
    NISA投資を適用（上限1800万円）
    """
    remaining_nisa_capacity = nisa_limit - nisa_cumulative
    
    if remaining_nisa_capacity <= 0:
        # NISA枠満了
        actual_contribution = nisa_contribution  # 通常投資として継続
        nisa_contribution_used = Decimal('0')
    elif nisa_contribution <= remaining_nisa_capacity:
        actual_contribution = nisa_contribution
        nisa_contribution_used = nisa_contribution
    else:
        # 一部のみNISA枠使用
        actual_contribution = nisa_contribution
        nisa_contribution_used = remaining_nisa_capacity
    
    risk_asset += actual_contribution
    nisa_cumulative += nisa_contribution_used
    
    return risk_asset, nisa_cumulative
```

---

## 6. UI/UX要件

### 6.1 多言語切替
- **配置場所**: サイドバー最上部
- **UI要素**: ドロップダウンまたはラジオボタン
- **選択肢**: "English" / "日本語"
- **デフォルト言語**: 日本語
- **切替動作**: 即座に全UI要素（ラベル、ボタン、グラフ、メッセージ）を選択言語に更新
- **セッション保持**: 選択言語は`st.session_state`で保持

### 6.2 入力バリデーション
- 年齢: 0 ～ 120歳
- 金額: 正の整数
- イベント年: シミュレーション期間内

### 6.3 エラーハンドリング
- 資産不足エラー: 「指定されたイベント支出を賄う資産が不足しています」（日本語）/ "Insufficient funds to cover event expenses"（英語）
- NISA上限表示: 「NISA枠は第X年に上限到達しました」（日本語）/ "NISA limit reached in Year X"（英語）

### 6.4 表示フォーマット
- 金額: カンマ区切り（例: 1,000,000）
- グラフY軸: 億円単位（例: 2.5B = 2.5億円）
- パーセンテージ: 小数点1桁（例: 5.0%）

### 6.5 レスポンシブ対応
- グラフサイズ: Plotlyのデフォルトサイズを使用（レスポンシブ）
- テーブル: Streamlitのデータフレーム表示機能を使用
- モバイル表示: Plotlyの自動調整機能により対応

---

## 7. 技術仕様

### 7.1 使用技術
- フレームワーク: Streamlit
- グラフ描画: **Plotly** (インタラクティブグラフ、多言語対応)
- データ処理: pandas, Decimal（高精度計算）
- 言語: Python 3.8以上

**Plotly採用理由**:
- 動的な多言語切替が容易（ラベルを変数で管理）
- インタラクティブ機能（ズーム、ホバー情報）が標準装備
- 日本語フォント設定が不要（ブラウザレンダリング）
- Streamlitとの高い親和性（`st.plotly_chart()`）

**Plotly実装例**:
```python
import plotly.graph_objects as go

# 翻訳テキスト取得
t = TRANSLATIONS[selected_language]

# 積上げ棒グラフの作成
fig = go.Figure()
fig.add_trace(go.Bar(
    name=t["risk_asset"],
    x=df['Year'],
    y=df['Risk Assets (JPY)'],
    marker_color='lightblue'
))
fig.add_trace(go.Bar(
    name=t["safe_asset"],
    x=df['Year'],
    y=df['Safe Assets (JPY)'],
    marker_color='lightgreen'
))

fig.update_layout(
    barmode='stack',
    title=t["chart_title"],
    xaxis_title=t["years"],
    yaxis_title=t["amount_billion"],
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
```

### 7.2 パフォーマンス要件
- シミュレーション実行時間: 5秒以内（50年間）
- UIレスポンス: 1秒以内

### 7.3 データ永続化
- **Phase 1**: セッション内のみ（st.session_state使用）
- **Phase 2**: SQLiteによるローカルDB保存

---

## 8. 制約事項

### 8.1 機能制約
- 家族構成: 最大5人（夫婦+子3人）
- イベント登録: 1年につき1件まで
- シミュレーション期間: 最大50年

### 8.2 計算制約
- リターン: 固定値（年ごとの変動なし）
- インフレ: 考慮しない
- 税金: 考慮しない（NISA前提）

---

## 9. 実装フェーズ

### 9.1 Phase 1: コア機能（優先実装）✅ 完了
- [x] 基本的な資産運用シミュレーション（タブ1）
- [x] 家族構成入力とライフイベント登録（タブ2）
- [x] イベント支出の反映とリバランス計算
- [x] NISA上限管理
- [x] 多言語切替機能（日本語・英語）
- [x] Plotlyによるインタラクティブグラフ表示
- [x] **CSV/XLSXエクスポート機能**

### 9.2 Phase 2: データ管理機能（後続実装）✅ 完了
- [x] SQLiteデータベースの実装
- [x] シミュレーション設定の保存機能（新規保存・上書き保存）
- [x] 保存済みシミュレーションの読込機能
- [x] シミュレーション履歴管理（一覧・削除）
- [x] **複数シナリオ比較機能（最大3シナリオ）**

### 9.3 Phase 3: 将来拡張候補
- 収入入力機能（給与・年金など）
- 複数イベント/年の登録
- モンテカルロシミュレーション（リターンの変動を考慮）
- 税金計算（特定口座投資の場合）
- 複数シナリオ比較機能
- PDFレポート出力

---

## 10. 受入基準

### 10.1 Phase 1 必須要件
- [ ] 言語切替機能が正常に動作する（全UI要素が即座に切り替わる）
- [ ] タブ1で基本シミュレーションが実行できる
- [ ] タブ2で家族構成を入力できる
- [ ] タブ2でイベントをテーブル形式で登録できる
- [ ] イベント支出が資産シミュレーションに反映される
- [ ] リバランス必要額が計算・表示される
- [ ] NISA上限（1800万円）が管理される
- [ ] Plotlyグラフと詳細テーブルが正しく表示される
- [ ] グラフのラベル・凡例が選択言語で表示される
- [ ] **CSV形式でデータをエクスポートできる**
- [ ] **Excel形式でデータをエクスポートできる**

### 10.2 Phase 2 必須要件
- [ ] シミュレーション設定を保存できる
- [ ] 保存済みシミュレーションを読み込める
- [ ] シミュレーション一覧が表示される
- [ ] 保存済みシミュレーションを削除できる
- [ ] 上書き保存機能が動作する

### 10.3 品質要件
- [ ] 計算精度: 小数点以下を適切に丸める
- [ ] エラー時に適切なメッセージを表示
- [ ] 50年シミュレーションが5秒以内に完了

---

## 11. 用語集

| 用語 | 定義 |
|------|------|
| リスク資産 | 株式・投資信託など、価格変動リスクのある資産 |
| 安全資産 | 預金・国債など、元本保証に近い資産 |
| リバランス | 目標とする資産配分比率を維持するための調整 |
| NISA | 少額投資非課税制度（上限1800万円） |
| ライフイベント | 進学、住宅購入など、大型支出を伴うイベント |
| Plotly | Pythonのインタラクティブグラフ描画ライブラリ |
| i18n (国際化) | 多言語対応のための設計・実装手法 |
| SQLite | ファイルベースの軽量データベース（Python標準） |
| エクスポート | データを外部ファイル（CSV/Excel）として出力する機能 |

---

## 12. 依存パッケージ

### 12.1 Phase 1 必須パッケージ
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
openpyxl>=3.1.0  # Excel出力用
```

### 12.2 Phase 2 追加パッケージ
```
# Phase 1のパッケージに加えて
# (なし - SQLite3はPython標準ライブラリ)
```

### 12.3 インストール方法
**Phase 1**:
```bash
pip install streamlit plotly pandas openpyxl
```

**Phase 2**:
```bash
# Phase 1と同じ（追加パッケージなし）
```

---

## 付録A: 計算例

### A.1 イベント支出とリバランスの例
```
前提:
- 総資産: 20,000,000円
- リスク資産: 16,000,000円（80%）
- 安全資産: 4,000,000円（20%）
- イベント支出: 3,000,000円
- 目標比率: リスク80% / 安全20%

処理:
1. 支出後
   - リスク: 16,000,000円
   - 安全: 1,000,000円（4,000,000 - 3,000,000）
   - 総額: 17,000,000円
   - 実質比率: リスク94.1% / 安全5.9%

2. リバランス
   - 目標リスク額: 17,000,000 × 0.8 = 13,600,000円
   - 目標安全額: 17,000,000 × 0.2 = 3,400,000円
   - リバランス必要額: 16,000,000 - 13,600,000 = 2,400,000円（リスク→安全）

3. リバランス後
   - リスク: 13,600,000円（80%）
   - 安全: 3,400,000円（20%）
   - 総額: 17,000,000円
```

---

**文書バージョン**: 2.0
**作成日**: 2025-11-27
**最終更新日**: 2025-11-27
**作成者**: システム設計担当
**変更履歴**:
- v1.0: 初版作成
- v1.1: 多言語対応機能追加、グラフライブラリをMatplotlibからPlotlyに変更
- v1.2: データエクスポート機能（CSV/XLSX）追加、データベース機能（Phase 2）追加
- v1.3: ライフプラン表の投資結果テーブルをシンプル化（支出前/後、リバランス詳細を削除し、最終資産のみ表示）、未登録家族メンバーの列を非表示に変更、日本語・英語表示対応を明記
- v2.0: **Phase 2完全実装** - SQLiteデータベース機能（保存・読込・削除・上書き）、複数シナリオ比較機能（最大3シナリオ）を追加
