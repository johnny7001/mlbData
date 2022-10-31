import pymysql
import os
from flask_sqlalchemy import SQLAlchemy
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

db = SQLAlchemy()

class mlb_DB:
    def connect(self):
        self.conn = pymysql.connect(
                             host=db_host,
                             user=db_user,
                             password=db_password,
                             db=db_name,
                             charset=db_charset,
                             cursorclass=cursorclass,
                             port=db_port)

    def query(self, sql):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
        except pymysql.OperationalError:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            print('重新連線')
        return cursor
    def close(self):
        self.connect()
        self.conn.close()
      

# 打擊數據
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


    def __init__(self, group, name, positions, team_id, team_rank, rank_count,
                 r, h, hr, rbi, bb, so, avg, ops, year):
        self.group = group
        self.name = name
        self.positions = positions
        self.team_id = team_id
        self.team_rank = team_rank
        self.rank_count = rank_count
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
    
# 投球數據
class Mlb_playerPitching(db.Model):
    __tablename__ = 'mlb_playerPitching'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    group = db.Column(db.String(45))
    name = db.Column(db.Text, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('mlb_teamName.id')) # team_id 外鍵
    team_rank = db.Column(db.Integer, nullable=False)
    rank_count = db.Column(db.Integer)
    w = db.Column(db.Integer)
    l = db.Column(db.Integer)
    era = db.Column(db.Float)
    ip = db.Column(db.Integer)
    h = db.Column(db.Integer)
    r = db.Column(db.Integer)
    er = db.Column(db.Integer)
    hr = db.Column(db.Integer)
    hb = db.Column(db.Integer)
    bb = db.Column(db.Integer)
    so = db.Column(db.Integer)
    whip = db.Column(db.Float)
    avg = db.Column(db.Float)
    year = db.Column(db.Integer)
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc) + timedelta(hours=8))


    def __init__(self, group, name, team_id, team_rank, rank_count,
                 w, l, era, ip, h, r, er, hr, hb, bb, so, whip, avg, year):
        self.group = group
        self.name = name
        self.team_id = team_id
        self.team_rank = team_rank
        self.rank_count = rank_count
        self.w = w
        self.l = l
        self.era = era
        self.ip = ip
        self.h = h
        self.r = r
        self.er = er
        self.hr = hr
        self.hb = hb
        self.bb = bb
        self.so = so
        self.whip = whip
        self.avg = avg
        self.year = year