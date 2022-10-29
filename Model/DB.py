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
      

# 模型( model )定義
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