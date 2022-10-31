# 作品構想  
使用爬蟲抓取運動網站的資料, 建立自動化爬取功能及更新資料庫內容, 設計API提供給使用者獲取想要的資料  
* Selenium解決js渲染網頁部分, BeautifulSoup解析Html  
* Requests將整理的參數串接後Get想要的內容  
* MySQL資料庫存放數據 (SQLAlchemy) 
* Flask建立API
* Docker打包爬蟲程式, 能直接在linux tmux上開啟多視窗執行爬蟲腳本並監測運行情況  
* 串接telegram bot, 建立指令對爬蟲腳本或資料庫進行操作, 並能自動通知目前更新的進度 (尚未完成)  
* 設定每週一到日下午16:00更新資料
================================================================================= 

# 資料庫結構設計  
* 抓取球隊名稱
table_name = mlb_teamName
column_name = 球隊名稱及ID(id, team_name, updated_at)
* 抓取近三年球員打擊數據 (2020-2022例行賽球員數據)    
table_name = mlb_playerHitting
column_name = 球員數據(id, team_id, rank, name, positions, years...)
* 抓取近三年球員投球數據 (2020-2022例行賽球員數據)    
table_name = mlb_playerPitching
column_name = 球員數據(id, team_id, rank, name, positions, years...)  
![image](https://github.com/johnny7001/mlbData/blob/c731f7615ab1bf6f5fa31aca0a5a2d2edbe9ca77/status/img/db_schemas.jpg)

=================================================================================

# 作品介紹
抓取聯盟的三支球隊的隊員例行賽數據排行 (隊伍選擇三支球隊 Yankees, Red_sox, Dodgers)  
* 打者 --> 篩選條件：全壘打排行，藉此用全壘打與其他數據比較   
* 投手 --> 篩選條件：三振排行，藉此用全壘打與其他數據比較   

=================================================================================

# mlb網站 -> URL參數參考
* url = https://bdfed.stitch.mlbinfra.com/bdfed/stats/player?stitch_env=prod&season=2022&sportId=1&stats=season& group=hitting&gameType=R&limit=25&offset=0&sortStat=homeRuns&order=desc&teamId=147

* 大分類 /stats/ + player or team  打者或球隊
* group = hitting, pitching 打擊或投球
* season = 賽季時間
* order = desc 降冪排序
* gameType = R 開頭的第一個字, R = Regular Season
* limit = 搜尋的數量
* sitCodes = 篩選條件
* position = 守備位置 (ex; 三壘 = 3B)
* playerPool = 打者分類 (Rookies, Current Players...)

=================================================================================

# API使用參考  
http://127.0.0.1:4434/player/group=pitching/team=Yankees/year=2022/top=1/orderBY=SO
* group (string): hitting, pitching -> 選擇打擊或投球數據  
* team (string): Yankees, Dodgers, Dodgers -> 選擇隊伍  
* year (int): 2020, 2021, 2022 -> 選擇年份  
* sortRange (int): 輸入要抓取的數量, 最大range = 25
* order_by (string): 輸入要排序的條件, 可根據資料庫欄位進行排序  
````
    {
        "AVG": 0.209,
        "BB": 50,
        "ER": 78,
        "ERA": 3.5,
        "H": 154,
        "HB": 2,
        "HR": 33,
        "IP": 200,
        "L": 8,
        "R": 81,
        "SO": 257,
        "W": 13,x
        "WHIP": 1.02,
        "group": "pitching",
        "id": 218,
        "name": "Gerrit_Cole",
        "rank_count": null,
        "t.id": 147,
        "t.updated_at": "Sun, 23 Oct 2022 13:06:34 GMT",
        "team_id": 147,
        "team_name": "Yankees",
        "team_rank": 1,
        "updated_at": "Wed, 26 Oct 2022 21:24:51 GMT",
        "year": 2022
    }
````
使用 SQLAlchemy 操作資料庫  
http://127.0.0.1:4434/team_name=all
*  輸入球隊名稱, 可查詢對應的球隊id, 輸入all可查詢全部球隊
````
    {
        "111": "Red_Sox",
        "119": "Dodgers",
        "147": "Yankees"
    }
````
http://127.0.0.1:4434/group=hitting/top=5/orderBY=hr  
* 輸入分類, 篩選條件及排名(降冪排序)
````
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
````
