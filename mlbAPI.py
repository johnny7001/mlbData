from flask import Flask
import json
from Model.DB import mlb_DB
import pymysql
import os
from flask_sqlalchemy import SQLAlchemy, session
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

db_host=os.getenv("db_host")
db_user=os.getenv("db_user")
db_password=os.getenv("db_password")
db_name=os.getenv("db_name")
db_charset=os.getenv("db_charset")
cursorclass=pymysql.cursors.DictCursor
db_port=8889

app = Flask(__name__)
mlb_db = mlb_DB()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://shane:GKbCoMubLMQ6o@sgpdb.itlab.tw:8889/shane"
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
db = SQLAlchemy(app)
# db.init_app(app)

# 模型( model )定義
# 打者數據
class Mlb_playerHitting(db.Model):
    __tablename__ = 'mlb_playerHitting'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    group = db.Column(db.String(45))
    name = db.Column(db.Text)
    positions = db.Column(db.String(45))
    team_id = db.Column(db.Integer, db.ForeignKey('mlb_teamName.id')) # team_id 外鍵
    team_rank = db.Column(db.Integer)
    rank_count = db.Column(db.Integer)
    r = db.Column(db.Integer)
    h = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    rbi = db.Column(db.Integer)
    bb = db.Column(db.Integer)
    so = db.Column(db.Integer)
    avg = db.Column(db.Float)
    ops = db.Column(db.Float)
    year = db.Column(db.Integer)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=8))


    def __init__(self, group, name, positions, team_id, team_rank, 
                 r, h, hr, rbi, bb, so, avg, ops, year):
        self.group = group
        self.name = name
        self.positions = positions
        self.team_id = team_id
        self.team_rank = team_rank
        self.r = r
        self.h = h
        self.hr = hr
        self.rbi = rbi
        self.bb = bb
        self.so = so
        self.avg = avg
        self.ops = ops
        self.year = year
        

# 球隊名稱
class Mlb_teamName(db.Model):
    __tablename__ = 'mlb_teamName'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    team_name = db.Column(db.String(45), unique=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=8))
    
    
@app.route('/')
def home():
    # 地點
    return ('this is mlbAPI !!')


@app.route('/player/group=<group>/team=<team>/year=<int:year>/top=<int:sortRange>/orderBY=<order_by>', methods=['GET'])  
def get_HittingData(group:str, team:str, year:int, sortRange:int, order_by:str) -> list:
    """
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
            and h.year = {year} order by {order_by} desc limit {sortRange};" 
    result = mlb_db.query(sql).fetchall() # type = list, len = 25
    return result


@app.route('/team_name=<name>', methods=['GET'])
def SearchFromTeamName(name:str) -> dict:
    """
    輸入球隊名稱, 可查詢對應的球隊id, 輸入all可查詢全部球隊
        Args:
            name (string): 球隊名稱
        Returns:
            回傳範例：
                {'球隊id':'球對名稱'}
    """
    # sql_cmd = """
    # select *
    # from mlb_teamName
    # """
    # 執行sql指令
    # query_data = db.engine.execute(sql_cmd)
    teamName_list = {}
    if name == 'all':
        result = db.session.query(Mlb_teamName).order_by("id").all()
    else:
        result = db.session.query(Mlb_teamName).filter_by(team_name=name)
    for items in result:
        teamName_list[f'{items.id}'] = items.team_name
    # print(teamName_list)
    return teamName_list

app.run(host='0.0.0.0', port=4434, debug=True) 