"""
SQLiteデータベースモジュール
シミュレーション設定の保存・読込・管理機能を提供
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class SimulationDB:
    """シミュレーションデータベース管理クラス"""

    def __init__(self, db_path='simulations.db'):
        """
        データベース初期化

        Args:
            db_path: データベースファイルのパス
        """
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """データベーステーブルを初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # シミュレーション基本情報テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulations (
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
            )
        ''')

        # ライフイベントテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS life_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulation_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                event_name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                FOREIGN KEY (simulation_id) REFERENCES simulations(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def save_simulation(self, name: str, params: Dict, events: List[Dict], simulation_id: Optional[int] = None) -> int:
        """
        シミュレーションを保存

        Args:
            name: シミュレーション名
            params: パラメータ辞書
            events: ライフイベントリスト
            simulation_id: 既存のシミュレーションID（上書き保存の場合）

        Returns:
            保存されたシミュレーションのID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            if simulation_id:
                # 上書き保存
                cursor.execute('''
                    UPDATE simulations
                    SET name = ?,
                        updated_at = CURRENT_TIMESTAMP,
                        initial_amount = ?,
                        nisa_contribution = ?,
                        risk_return = ?,
                        risk_ratio = ?,
                        investment_years = ?,
                        husband_age = ?,
                        wife_age = ?,
                        child1_age = ?,
                        child2_age = ?,
                        child3_age = ?,
                        language = ?
                    WHERE id = ?
                ''', (
                    name,
                    params['initial_amount'],
                    params['nisa_contribution'],
                    params['risk_return'],
                    params['risk_ratio'],
                    params['investment_years'],
                    params.get('husband_age'),
                    params.get('wife_age'),
                    params.get('child1_age'),
                    params.get('child2_age'),
                    params.get('child3_age'),
                    params.get('language', 'ja'),
                    simulation_id
                ))

                # 既存のイベントを削除
                cursor.execute('DELETE FROM life_events WHERE simulation_id = ?', (simulation_id,))
                saved_id = simulation_id
            else:
                # 新規保存
                cursor.execute('''
                    INSERT INTO simulations (
                        name, initial_amount, nisa_contribution, risk_return, risk_ratio,
                        investment_years, husband_age, wife_age, child1_age, child2_age,
                        child3_age, language
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    name,
                    params['initial_amount'],
                    params['nisa_contribution'],
                    params['risk_return'],
                    params['risk_ratio'],
                    params['investment_years'],
                    params.get('husband_age'),
                    params.get('wife_age'),
                    params.get('child1_age'),
                    params.get('child2_age'),
                    params.get('child3_age'),
                    params.get('language', 'ja')
                ))
                saved_id = cursor.lastrowid

            # ライフイベントを保存
            for event in events:
                cursor.execute('''
                    INSERT INTO life_events (simulation_id, year, event_name, amount)
                    VALUES (?, ?, ?, ?)
                ''', (saved_id, event['year'], event['event_name'], event['amount']))

            conn.commit()
            return saved_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def load_simulation(self, simulation_id: int) -> Optional[Dict]:
        """
        シミュレーションを読み込む

        Args:
            simulation_id: シミュレーションID

        Returns:
            シミュレーションデータの辞書、存在しない場合はNone
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # シミュレーション基本情報を取得
            cursor.execute('SELECT * FROM simulations WHERE id = ?', (simulation_id,))
            sim_row = cursor.fetchone()

            if not sim_row:
                return None

            # ライフイベントを取得
            cursor.execute('''
                SELECT year, event_name, amount
                FROM life_events
                WHERE simulation_id = ?
                ORDER BY year
            ''', (simulation_id,))
            event_rows = cursor.fetchall()

            # データを辞書形式に変換
            simulation = {
                'id': sim_row['id'],
                'name': sim_row['name'],
                'created_at': sim_row['created_at'],
                'updated_at': sim_row['updated_at'],
                'params': {
                    'initial_amount': sim_row['initial_amount'],
                    'nisa_contribution': sim_row['nisa_contribution'],
                    'risk_return': sim_row['risk_return'],
                    'risk_ratio': sim_row['risk_ratio'],
                    'investment_years': sim_row['investment_years'],
                    'husband_age': sim_row['husband_age'],
                    'wife_age': sim_row['wife_age'],
                    'child1_age': sim_row['child1_age'],
                    'child2_age': sim_row['child2_age'],
                    'child3_age': sim_row['child3_age'],
                    'language': sim_row['language']
                },
                'events': [
                    {
                        'year': event['year'],
                        'event_name': event['event_name'],
                        'amount': event['amount']
                    }
                    for event in event_rows
                ]
            }

            return simulation

        finally:
            conn.close()

    def list_simulations(self) -> List[Dict]:
        """
        全シミュレーションのリストを取得

        Returns:
            シミュレーション情報のリスト
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT id, name, created_at, updated_at
                FROM simulations
                ORDER BY updated_at DESC
            ''')
            rows = cursor.fetchall()

            simulations = [
                {
                    'id': row['id'],
                    'name': row['name'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                for row in rows
            ]

            return simulations

        finally:
            conn.close()

    def delete_simulation(self, simulation_id: int) -> bool:
        """
        シミュレーションを削除

        Args:
            simulation_id: シミュレーションID

        Returns:
            削除成功の場合True
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM simulations WHERE id = ?', (simulation_id,))
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def get_simulation_name(self, simulation_id: int) -> Optional[str]:
        """
        シミュレーション名を取得

        Args:
            simulation_id: シミュレーションID

        Returns:
            シミュレーション名、存在しない場合はNone
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT name FROM simulations WHERE id = ?', (simulation_id,))
            row = cursor.fetchone()
            return row[0] if row else None

        finally:
            conn.close()

    def simulation_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        同名のシミュレーションが存在するか確認

        Args:
            name: シミュレーション名
            exclude_id: 除外するシミュレーションID（上書き保存時に使用）

        Returns:
            存在する場合True
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            if exclude_id:
                cursor.execute('SELECT COUNT(*) FROM simulations WHERE name = ? AND id != ?', (name, exclude_id))
            else:
                cursor.execute('SELECT COUNT(*) FROM simulations WHERE name = ?', (name,))

            count = cursor.fetchone()[0]
            return count > 0

        finally:
            conn.close()
