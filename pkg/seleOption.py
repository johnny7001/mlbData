import time
from bs4 import BeautifulSoup
from pkg.driver import open_driver
from selenium.webdriver.common.by import By

time_list = []
season_list = []
team_list = []
date_range = []
positions_list = []
pool_list = []
split_list = []

def main(url):
    driver = open_driver()
    driver.get(url)
    driver.maximize_window()
    # 大分類：Player, Team
    # 抓取時間清單
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[1]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    all_time_totals = soup.find('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option bui-dropdown__option--is-focused css-1n7v3ny-option').text
    time_list.append(all_time_totals)
    seasonYears = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for s_year in seasonYears:
        time_list.append(s_year.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-2-option-1-0"]/div').click()
    time.sleep(1)
    
    # 抓取賽季分類
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[2]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    seasonTitles = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for seasonType in seasonTitles:
        season_list.append(seasonType.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-3-option-0"]').click()
    time.sleep(1)
    
    # 抓取球隊
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[3]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    AllTeams = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for team in AllTeams:
        team_list.append(team.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-4-option-0-0"]').click()
    time.sleep(1)
    
    # 抓取最近日期
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[4]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    AllRanges = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for date in AllRanges:
        date_range.append(date.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-5-option-0"]').click()
    time.sleep(1)
    
    # 抓取守備位置
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[5]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    AllPosition = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for position in AllPosition:
        positions_list.append(position.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-6-option-0"]').click()
    time.sleep(1)
    
    # 選手池
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[6]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    AllPool = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for pool in AllPool:
        pool_list.append(pool.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-7-option-0"]').click()
    time.sleep(1)
    
    # 篩選條件
    driver.find_element(By.XPATH, '//*[@id="stats-app-root"]/section/section/div[1]/div[1]/div[7]/div').click()
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    AllSplit = soup.find_all('div', class_='dropdownPrefix-3lLVtYkH bui-dropdown__option css-yt9ioa-option')
    for split in AllSplit:
        split_list.append(split.text)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="react-select-8-option-0-3"]').click()
    time.sleep(1)
        
    
if __name__=='__main__':
    url = 'https://www.mlb.com/yankees/stats/'
    main(url)
    # print(time_list)
    print(team_list[2:])
    # print(season_list)
    # print(date_range)
    # print(positions_list)
    # print(pool_list)
    # print(split_list)







