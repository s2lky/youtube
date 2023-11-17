from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent


def first_vidoe(driver):
    value = '안녕하세요'
    driver.get(f'https://www.youtube.com/results?search_query={value}')

    time.sleep(3)

    video_all_list = driver.find_element(By.XPATH, '//*[@id="container"]/ytd-two-column-search-results-renderer')
    either_shelf = random.randint(1,2)

    if either_shelf == 1:
        time.sleep(1)
        to_click_vidoe = video_all_list.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        random_value = random.randint(0, (len(to_click_vidoe) - 1))
        to_click_vidoe[random_value].click()
    else:
        time.sleep(1)
        related_videos = video_all_list.find_elements(By.TAG_NAME, 'ytd-shelf-renderer')
        random_value1 = random.randint(0, (len(related_videos) - 1))
        shelf_videoes = related_videos[random_value1].find_elements(By.TAG_NAME, 'ytd-thumbnail')
        random_value2 = random.randint(0, (len(shelf_videoes) - 1))
        time.sleep(1)
        shelf_videoes[random_value2].click()



def next_video(driver):
    driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer/a/div').click()
    time.sleep(5)
    video_list = driver.find_elements(By.TAG_NAME, 'ytd-rich-grid-row')
    random_number = random.randint(0, (len(video_list) - 1))
    youtube_to_click = video_list[random_number].find_elements(By.ID, 'thumbnail')
    random_number = random.randint(0, (len(youtube_to_click) - 1))
    # 믹스 재생목록 제외 예외코드 추가 예정
    element = youtube_to_click[random_number]
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def user_session():
    viewing_time = random.randint(1, 10)
    time.sleep(viewing_time * 60)
    return viewing_time
    
    
def video_info(driver):
    # ad_skip 함수에서 sleep을 걸어서 필요가 사라짐
    # time.sleep(4)
    # driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]').click()
    element = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.3)
    title = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
    channel_name = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').text
    viewership = driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text
    if "조회" in viewership:
        uploaded_date = driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
    else:
        view_date_upclass = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-watch-info-text/div')
        viewership = view_date_upclass.find_element(By.ID, 'view-count').get_attribute('aria-label').strip()
        uploaded_date = view_date_upclass.find_element(By.ID, 'info').find_element(By.TAG_NAME, 'span').text
    describe = driver.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string').text
    current_url = driver.current_url
    like = ''.join(filter(str.isdigit, driver.find_element(By.CLASS_NAME, 'yt-spec-button-shape-next--segmented-start').get_attribute('aria-label')))
    # 좋아요가 안찍히는 경우
    if len(like) == 0:
        like = None
    return title, channel_name, viewership, uploaded_date, describe, current_url, like
    

def ad_skip(driver):
    time.sleep(2)
    try:
        ad_site = None
        ad_site2 = None
        ad_site = driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
        print("ad_site : ", ad_site)
        value = driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
        if '재생' in value or '종료' in value:
            ad_time = driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
            time.sleep(int(ad_time) + 2)

            value2 = driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
            if '재생' in value2 or '종료' in value2:
                ad_site2 = driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                print("ad_site2 : ", ad_site2)
                ad_time = driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                time.sleep(int(ad_time))
            else:
                time.sleep(5.5)
                ad_site2 = driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                print("ad_site2c : ", ad_site2)
                driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
        else:
            time.sleep(6)
            driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
    except:
        pass
    
    return ad_site, ad_site2


def record(driver):
    session = []
    title_list = []
    channel_list = []
    viewership_list = []
    uploaded_date_list = []
    describe_list = []
    url_list = []
    first_ad_list = []
    second_ad_list = []
    like_list = []
    first_vidoe(driver=driver)
    
    for _ in range(10):
        first_ad, second_ad = ad_skip(driver=driver)
        first_ad_list.append(first_ad)
        second_ad_list.append(second_ad)
        
        viewing_time = user_session()
        session.append(viewing_time)
        
        title, channel_name, viewership, uploaded_date, describe, current_url, like = video_info(driver=driver)
        title_list.append(title)
        channel_list.append(channel_name)
        viewership_list.append(viewership)
        uploaded_date_list.append(uploaded_date)
        describe_list.append(describe)
        url_list.append(current_url)
        like_list.append(like)
        # 영상이 재생되는 도중 종료
        next_video(driver=driver)
        
    youtube_data = {'session': session, 'title': title_list, 'channel': channel_list, 
                    'viewership': viewership_list, 'uploaded_date': uploaded_date_list, 'describe': describe_list, 
                    'like': like_list, 'url': url_list, 'first_ad': first_ad_list, 'second_ad': second_ad_list}
    df = pd.DataFrame(youtube_data)
    df.to_csv('./youtube_bot_log.csv', index=False)


if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_extension()
    # driver = Chrome(options=chrome_options)
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--disable-gpu")
    driver = Chrome(chrome_options)
    record(driver=driver)
    driver.quit()
    
    
