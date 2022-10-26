from pkg.getData import playerHitting, playerPitching
from pkg.message import message
from apscheduler.schedulers.blocking import BlockingScheduler


def main():
    try:
        # 爬取投手資料
        playerPitching()
    except Exception as err:
        message(f'爬取投手資料失敗, 錯誤碼：{err}')
        
    try:    
        # 爬取打者資料
        playerHitting()
    except Exception as err:
            message(f'爬取打擊資料失敗, 錯誤碼：{err}')
    
if __name__=='__main__':
    # main()
    scheduler = BlockingScheduler(timezone="Asia/Taipei")
    # 每週一到日 下午16:00更新
    scheduler.add_job(main, 'cron', day_of_week='*', hour=16, minute=00)

    scheduler.start()