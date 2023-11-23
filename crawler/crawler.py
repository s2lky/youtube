from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import time
import random
from fake_useragent import UserAgent
from datetime import datetime
import re
# from memory_profiler import profile

class YouTubeBotError(Exception):
    pass

class YouTubeBot:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        ua = UserAgent()
        user_agent = ua.random
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--disable-gpu")
        return Chrome(chrome_options)

    def get_random_persona(self):
        df = pd.read_csv('/usr/src/data/persona_data.csv')
        value = random.randint(0, (len(df) - 1))
        name = df.iloc[value]['페르소나 이름']
        keyword = random.choice((df.loc[value]['키워드']).split(", "))
        return name, keyword

    def first_video(self, keyword):
        self.driver.get('https://www.youtube.com/')
        time.sleep(5)
        self.driver.find_element(By.ID, 'search-form').find_element(By.ID, 'search').send_keys(f'{keyword}')
        time.sleep(0.3)
        self.driver.find_element(By.ID, 'search-icon-legacy').click()
        time.sleep(3)
        video_all_list = self.driver.find_element(By.XPATH, '//*[@id="container"]/ytd-two-column-search-results-renderer')
        time.sleep(1)
        to_click_video = video_all_list.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        while True:
            random_value = random.randint(0, (len(to_click_video) - 1))
            video_type = to_click_video[random_value].find_element(By.TAG_NAME, 'ytd-thumbnail-overlay-time-status-renderer').get_attribute('overlay-style')
            if video_type == "SHORTS":
                continue
            else:
                element = to_click_video[random_value].find_element(By.ID, 'thumbnail')
                try:
                    element.click()
                except:
                    self.driver.execute_script("arguments[0].click();", element)
                break

    def next_video(self):
        self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer/a/div').click()
        time.sleep(random.uniform(5, 6))
        video_list = self.driver.find_elements(By.TAG_NAME, 'ytd-rich-grid-row')
        random_number = random.randint(0, (len(video_list) - 1))
        youtube_to_click = video_list[random_number].find_elements(By.ID, 'thumbnail')
        random_number = random.randint(0, (len(youtube_to_click) - 1))
        element = youtube_to_click[random_number]
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def video_len(self):
        # 정규표현식을 사용하여 시, 분, 초 추출
        time_str = self.driver.find_element(By.CLASS_NAME, 'ytp-time-duration')
        match = re.match(r'(?:(\d+):)?(\d+):(\d+)', time_str)
        
        if match:
            groups = match.groups()
            hours = int(groups[0]) if groups[0] is not None else 0
            minutes = int(groups[1])
            seconds = int(groups[2])
            
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        else:
            # 매치되지 않을 경우 예외 처리 또는 기본값 설정
            print(f"올바른 시간 형식이 아닙니다: {time_str}")
            return None

    def user_session(self):
        viewing_time = (random.randint(1, 10) * 60)
        print(viewing_time)
        video_time = self.video_len()
        if video_time > viewing_time:
            pass
        else:
            viewing_time = video_time
        start_time = time.time()
        while (time.time() - start_time) < viewing_time:
            try:
                ad_site = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                print("ad_site : ", ad_site)
                value = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
                if '재생' in value or '종료' in value:
                    ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                    time.sleep(int(ad_time) + random.uniform(1, 1.5))
                    value2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
                    if '재생' in value2 or '종료' in value2:
                        ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                        print("ad_site2 : ", ad_site2)
                        ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                        time.sleep(int(ad_time))
                    else:
                        time.sleep(random.uniform(5.5, 6))
                        ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                        print("ad_site2c : ", ad_site2)
                        self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
                else:
                    time.sleep(random.uniform(5.5, 6))
                    self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
            except:
                time.sleep(4.5)
        return viewing_time

    def video_info(self):
        element = self.driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-text-inline-expander/tp-yt-paper-button[1]")
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(random.uniform(0.2, 0.4))
        title = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
        channel_name = self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[1]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div/yt-formatted-string/a').text
        viewership = self.driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text
        if "조회" in viewership:
            viewership = ''.join(filter(str.isdigit, viewership))
            text = self.driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text
            if "최초" in text or "스트리밍" in text:
                pattern = r'(\d{4}\. \d{1,2}\. \d{1,2})'
                match = re.search(pattern, text)
                uploaded_date = datetime.strptime(match.group(1), "%Y. %m. %d")
            else:
                uploaded_date = datetime.strptime(self.driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text, "%Y. %m. %d.")
        else:
            view_date_upclass = self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[4]/div[1]/div/ytd-watch-info-text/div')
            viewership = ''.join(filter(str.isdigit, view_date_upclass.find_element(By.ID, 'view-count').get_attribute('aria-label').strip()))
            text = view_date_upclass.find_element(By.ID, 'info').find_element(By.TAG_NAME, 'span').text
            if "최초" in text or "스트리밍" in text:
                pattern = r'(\d{4}\. \d{1,2}\. \d{1,2})'
                match = re.search(pattern, text)
                uploaded_date = datetime.strptime(match.group(1), "%Y. %m. %d")
            else:
                uploaded_date = datetime.strptime(view_date_upclass.find_element(By.ID, 'info').find_element(By.TAG_NAME, 'span').text, "%Y. %m. %d.")
        describe = self.driver.find_element(By.XPATH, '//*[@id="description-inline-expander"]/yt-attributed-string').text
        current_url = self.driver.current_url
        print(current_url)
        like = ''.join(filter(str.isdigit, self.driver.find_element(By.CLASS_NAME, 'yt-spec-button-shape-next--segmented-start').get_attribute('aria-label')))
        if len(like) == 0:
            like = None
        return title, channel_name, viewership, uploaded_date, describe, current_url, like

    def ad_skip(self):
        time.sleep(random.uniform(1.7, 2))
        try:
            ad_site = None
            ad_site2 = None
            ad_site = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
            print("ad_site : ", ad_site)
            value = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
            if '재생' in value or '종료' in value:
                ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                time.sleep(int(ad_time) + random.uniform(1, 1.5))
                value2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
                if '재생' in value2 or '종료' in value2:
                    ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                    print("ad_site2 : ", ad_site2)
                    ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                    time.sleep(int(ad_time))
                else:
                    time.sleep(random.uniform(5.5, 6))
                    ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                    print("ad_site2c : ", ad_site2)
                    self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
            else:
                time.sleep(random.uniform(5.5, 6))
                self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
        except:
            pass
        return ad_site, ad_site2

    def record(self):
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
        name_list = []
        keyword_list = []
        
        name, keyword = self.get_random_persona()
        self.first_video(keyword=keyword)
        
        for _ in range(10):
            name_list.append(name)
            keyword_list.append(keyword)
            
            first_ad, second_ad = self.ad_skip()
            first_ad_list.append(first_ad)
            second_ad_list.append(second_ad)
            
            viewing_time = self.user_session()
            session.append(viewing_time)
            
            title, channel_name, viewership, uploaded_date, describe, current_url, like = self.video_info()
            title_list.append(title)
            channel_list.append(channel_name)
            viewership_list.append(viewership)
            uploaded_date_list.append(uploaded_date)
            describe_list.append(describe)
            url_list.append(current_url)
            like_list.append(like)

            self.next_video()
            
        youtube_data = {'name': name_list, 'keyword': keyword_list, 'session': session, 'title': title_list, 'channel': channel_list, 
                        'viewership': viewership_list, 'uploaded_date': uploaded_date_list, 'describe': describe_list, 
                        'like': like_list, 'url': url_list, 'first_ad': first_ad_list, 'second_ad': second_ad_list}
        df = pd.DataFrame(youtube_data)
        
        df.to_csv('./youtube_bot_log.csv', index=False)
        
        return df
    
    # @profile
    def run(self):
        try:
            result_df = self.record()  # Capture the returned DataFrame
            return result_df
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(error_message)
            # If you want to log the error to a file, you can use the following line instead
            # with open("error_log.txt", "a") as f:
            #     f.write(f"{error_message}\n")
            raise YouTubeBotError(error_message) from e

    def cleanup(self):
        self.driver.quit()


if __name__ == "__main__":
    bot = YouTubeBot()
    result_df = bot.run()  # Save the returned DataFrame as a variable
    bot.cleanup()
    

