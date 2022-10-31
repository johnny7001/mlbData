from flask import Flask
import json
from Model.DB import mlb_DB, Mlb_playerHitting, Mlb_teamName, Mlb_playerPitching
import pymysql
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
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

@app.route('/group=<group>/top=<int:sortRange>/orderBY=<order_by>', methods=['GET'])
def SearchFromGroup(group:str, sortRange:int, order_by:str) -> dict:
    """
    輸入分類, 可查詢該分類所有資料
        Args:
            group (string): hitting / pitching
            sortRange (int): 要篩選的數量
            order_by (string): 篩選條件
        Returns:
            回傳範例：
                    {
                        "AVG": 0.311,
                        "BB": 111,
                        "HR": 62,
                        "Hits": 177,
                        "RBI": 131,
                        "SO": 175,
                        "name": "Aaron_Judge",
                        "positions": "CF",
                        "team_id": 147
                     }

    """
    group_type = group.capitalize() # 第一個字變大寫
    groupData_list = []
    if group_type == 'all':
        result = db.session.query(Mlb_playerHitting).order_by("id").all()
    elif group_type == 'Hitting':
        result = db.session.query(Mlb_playerHitting).order_by(desc(f"{order_by}")).limit(sortRange)
        
        for items in result:
            memberData_dict = {}
            memberData_dict['name'] = items.name
            memberData_dict['positions'] = items.positions
            memberData_dict['team_id'] = items.team_id
            memberData_dict['Hits'] = items.h
            memberData_dict['HR'] = items.hr
            memberData_dict['RBI'] = items.rbi
            memberData_dict['BB'] = items.bb
            memberData_dict['SO'] = items.so
            memberData_dict['AVG'] = items.avg
            groupData_list.append(memberData_dict)
            
    elif group_type == 'Pitching':
        result = db.session.query(Mlb_playerPitching).order_by(desc(f"{order_by}")).limit(sortRange)
        
        for items in result:
            memberData_dict = {}
            memberData_dict['BB'] = items.bb
            memberData_dict['SO'] = items.so
            memberData_dict['Lose'] = items.l
            memberData_dict['Wins'] = items.w
            memberData_dict['name'] = items.name
            memberData_dict['team_id'] = items.team_id
    
            groupData_list.append(memberData_dict)
    else:
        content = '輸入參數錯誤，請輸入hitting or pitching'
        groupData_list.append(content)
    
    return groupData_list
    
app.run(host='0.0.0.0', port=4434, debug=True) 