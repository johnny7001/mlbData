from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.DB import mlb_DB
import json
db = mlb_DB()

app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://shane:GKbCoMubLMQ6o@sgpdb.itlab.tw:8889/shane"
# db = SQLAlchemy(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://account:password@IP:3306/db"
# sql = f"SELECT * FROM shane.jable01_tv where dir_name like '{dir_name}';"
# query_data = db.engine.execute(sql)
# result = query_data.fetchone()

@app.route('/')
def home():
    # 地點
    return ('this is mlbAPI !!')


@app.route('/player/<group>/<team>/<int:year>/top<int:sortRange>/orderBY=<order_by>', methods=['GET'])  
def get_HittingData(group, team, year, sortRange, order_by) -> list:
    """_summary_
    Args:
        group (string): hitting, pitching
        team (string): Yankees, Dodgers, Dodgers
        year (int): 2020, 2021, 2022
        sortRange (int): 輸入要抓取的數量, 最大range = 25
        order_by (string): 輸入要排序的條件, 可根據資料庫欄位進行排序
    Returns:
        回傳範例：
        {'id': 222, 'group': 'pitching', 'name': 'Jordan_Montgomery', 
        'team_id': 147, 'team_rank': 5, 'rank_count': None, 'W': 3, 'L': 3, 'ERA': 3.69, 'IP': 114, 
        'H': 103, 'R': 48, 'ER': 47, 'HR': 15, 'HB': 7, 'BB': 23, 'SO': 97, 'WHIP': 1.1, 'AVG': 0.236, 
        'year': 2022, 'updated_at': datetime.datetime(2022, 10, 26, 21, 25), 't.id': 147, 
        'team_name': 'Yankees', 't.updated_at': datetime.datetime(2022, 10, 23, 13, 6, 34)}
    """
    table_name = group.capitalize() # 第一個字變大寫

    sql = f"SELECT * from `mlb_player{table_name}` as h LEFT JOIN `mlb_teamName` as t\
        on h.team_id = t.id WHERE h.group = '{group}' and t.team_name = '{team}'\
            and h.year = {year} order by {order_by} limit {sortRange};" 
    result = db.query(sql).fetchall() # type = list, len = 25
    return result

app.run(host='0.0.0.0', port=4434, debug=True) 