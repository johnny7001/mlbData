from Model.DB import mlb_DB
from pkg.message import message
import requests
import json
db = mlb_DB()

# 篩選出球隊
def teamName_list():
    team_list = []
    sql = "SELECT `team_name` from shane.mlb_teamName;"
    result = db.query(sql).fetchall()
    for r in result:
        team_list.append(r['team_name'])
    return team_list
    
# 抓出球員打擊數據
def playerHitting():
    sele_object = 'player'
    group = 'hitting'
    g_type = 'R'
    rank = 'HomeRuns'
    team_list = teamName_list()
        
    for year in range(2020, 2023):
    # year = 2021 
        for p_team in team_list:
            sele_object = sele_object.replace("'", "")
            group = group.replace("'", "")
            g_type = g_type.replace("'", "")
            p_team = p_team.replace("'", "")

            # 找出 球隊 對應的 ID
            sql = "SELECT `id` from shane.mlb_teamName WHERE `team_name` = '{}'".format(p_team)
            result = db.query(sql).fetchone()
            p_team_id = result['id']
            # print(p_team_id)
            url = f"https://bdfed.stitch.mlbinfra.com/bdfed/stats/{sele_object}?stitch_env=prod&season={year}&sportId=1&stats=season&group={group}&gameType={g_type}&limit=25&offset=0&sortStat={rank}&order=desc&teamId={p_team_id}"
            resp = requests.get(url)
            respDict = json.loads(resp.text) # type = dict
            stats = respDict['stats']
            count = 1
            for player in stats:
                p_name = player['playerFullName'].replace(' ', '_').replace("'", " ")
                # print(count, p_name)
                p_positions = player['positionAbbrev']
                p_rank = player['rank']
                p_runs = player['runs']
                p_hits = player['hits']
                p_hr = player['homeRuns']
                p_rbi = player['rbi']
                p_bb = player['baseOnBalls']
                p_so = player['strikeOuts']
                p_avg = player['avg']
                p_ops = player['ops']
                
                # 先判斷該球員在球隊的排名, 球員姓名, 球隊是否跟前一筆數據相同, 如果相同則update, 不相同則把舊的資料刪掉並插入新的
                sql = "SELECT `id` from shane.mlb_playerHitting \
                    WHERE `year` = '{}' and `team_rank` = '{}' and `rank_count` = '{}' and `name` = '{}'\
                        ".format(year, p_rank, count, p_name)
                result = db.query(sql).fetchone()
                # print(result)
                if result != None:
                    sql = "UPDATE shane.mlb_playerHitting SET `name`='{}',`positions`='{}',`team_id`='{}',`team_rank`='{}', `rank_count`='{}',`R`='{}',\
                        `H`='{}', `HR`='{}', `RBI`='{}',`BB`='{}', `SO`='{}', `AVG`='{}', `OPS`='{}', `year`='{}'\
                            WHERE `id` = '{}';".format(p_name, p_positions, p_team_id, p_rank, count, p_runs, p_hits, p_hr, p_rbi, p_bb, p_so,
                                                       p_avg, p_ops, year, result['id'])
                    db.query(sql)
                    content = f'{year}, {p_team_id}, {p_rank} data success!!'
                    message(f'修改 {content}')
                else:
                    # 刪除舊的資料
                    sql = "DELETE FROM shane.mlb_playerHitting WHERE `year` = '{}' and `rank_count` = '{}' and `team_id` = '{}';\
                        ".format(year, count, p_team_id)
                    db.query(sql)
                    content = f'delete: ', {year}, {count},{p_team_id}, 'success!!'
                    message(content)

                    # 用球員順序還行當唯一值作為判斷, 因為排名可能重複, 所以設置count來做區分, count位置若名稱相同則更新資料, 若不相同則插入
                    sql = "INSERT INTO `mlb_playerHitting` (`group`, `name`, `positions`, `team_id`,`team_rank`,`rank_count`, `R`, `H`, `HR`, `RBI`, `BB`, `SO`, `AVG`, `OPS`, `year`) \
                        values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')\
                                ".format(group, p_name, p_positions, p_team_id, p_rank, count, p_runs, p_hits, p_hr, p_rbi, p_bb, p_so,
                        p_avg, p_ops, year)
                    db.query(sql)
                    content = f"insert: {group}, {p_name}, {p_positions}, {p_team_id}, {p_runs}, {p_hits}, {p_hr}, \
                            {p_rbi}, {p_bb}, {p_so},{p_avg}, {p_ops}, {year} success!!"
                    message(content)
                count += 1
            db.close()
    
    
    
# 抓出球員投球數據
def playerPitching():
    sele_object = 'player'
    group = 'pitching'
    g_type = 'R'
    rank = 'strikeouts'
    team_list = teamName_list()
        
    for year in range(2020, 2023):
    # year = 2021 
        for p_team in team_list:
            sele_object = sele_object.replace("'", "")
            group = group.replace("'", "")
            g_type = g_type.replace("'", "")
            p_team = p_team.replace("'", "")

            # 找出 球隊 對應的 ID
            sql = "SELECT `id` from shane.mlb_teamName WHERE `team_name` = '{}'".format(p_team)
            result = db.query(sql).fetchone()
            p_team_id = result['id']
            # print(p_team_id)
            url = f"https://bdfed.stitch.mlbinfra.com/bdfed/stats/{sele_object}?stitch_env=prod&season={year}&sportId=1&stats=season&group={group}&gameType={g_type}&limit=25&offset=0&sortStat={rank}&order=desc&teamId={p_team_id}"
            resp = requests.get(url)
            respDict = json.loads(resp.text) # type = dict
            stats = respDict['stats']
            count = 1
            for player in stats:
                p_name = player['playerName'].replace(' ', '_').replace("'", " ")
                p_rank = player['rank']
                p_win = player['wins']
                p_lose = player['losses']
                p_era = player['era']
                p_ip = player['inningsPitched']
                p_hits = player['hits']
                p_runs = player['runs']
                p_er = player['earnedRuns']
                p_hr = player['homeRuns']
                p_hb = player['hitByPitch']
                p_bb = player['baseOnBalls']
                p_so = player['strikeOuts']
                p_whip = player['whip']
                p_avg = player['avg']

                # 先判斷該球員在球隊的排名, 球員姓名, 球隊是否跟前一筆數據相同, 如果相同則update, 不相同則把舊的資料刪掉並插入新的
                sql = "SELECT `id` from shane.mlb_playerPitching \
                    WHERE `year` = '{}' and `team_rank` = '{}' and `rank_count` = '{}' and `name` = '{}'\
                        ".format(year, p_rank, count, p_name)
                result = db.query(sql).fetchone()
                # print(result)
                if result != None:
                    sql = "UPDATE shane.mlb_playerPitching SET `name`='{}', `team_id`='{}', `team_rank`='{}', `rank_count`='{}', \
                        `W`='{}', `L`='{}', `ERA`='{}', `IP`='{}',`H`='{}', `R`='{}', `ER`='{}', `HR`='{}', `HB`='{}', `BB`='{}', `SO`='{}', `WHIP`='{}',\
                        `AVG`='{}' WHERE `id` = '{}'\
                            ".format(p_name, p_team_id, p_rank, count, p_win, p_lose, p_era, p_ip, p_hits, p_runs, p_er, p_hr,
                        p_hb,p_bb,p_so,p_whip,p_avg, result['id'])
                    db.query(sql)
                    content = f'{year}, {p_team_id}, {p_rank} data success!!'
                    message(f'修改 {content}')
                else:
                    # 刪除舊的資料
                    sql = "DELETE FROM shane.mlb_playerPitching WHERE `year` = '{}' and `rank_count` = '{}' and `team_id` = '{}';\
                        ".format(year, count, p_team_id)
                    db.query(sql)
                    content = f'delete: ', {year}, {count}, {p_team_id}, 'success!!'
                    message(content)
                    
                    # 插入新的資料
                    sql = "INSERT INTO `mlb_playerPitching` (`group`,`name`,`team_id`,`team_rank`,`rank_count`, `W`,`L`,`ERA`,`IP`,`H`,`R`,`ER`,`HR`,`HB`,`BB` \
                        ,`SO`, `WHIP`, `AVG`, `year`) \
                    values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', \
                        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(group, p_name,p_team_id,p_rank, count,p_win, p_lose, p_era, p_ip, p_hits, p_runs, p_er, p_hr,
                    p_hb,p_bb,p_so,p_whip,p_avg,year)
                    db.query(sql)
                    content = f'insert: ', {year}, {group}, {p_name},{p_team_id}, {p_rank}, {count},{p_win}, {p_lose}, {p_era}, {p_ip}, {p_hits}, {p_runs}, {p_er}, {p_hr},
                    {p_hb},{p_bb},{p_so},{p_whip},{p_avg}, 'success!!'
                    message(content)
                count += 1
            db.close()
            
            