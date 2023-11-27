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
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1080,1080')
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--disable-gpu")
        return Chrome(chrome_options)

    def get_random_persona(self):
        df = pd.read_csv('/Users/a13/Documents/vsc_file/team07_with_company/data/persona_data.csv')
        value = random.randint(0, (len(df) - 1))
        name = df.iloc[value]['페르소나 이름']
        keyword = random.choice((df.loc[value]['키워드']).split(", "))
        return name, keyword

    def first_video(self, keyword):
        self.driver.get('https://www.youtube.com/')
        time.sleep(5)
        try:
            self.driver.find_element(By.TAG_NAME, 'ytd-rich-grid-row')
        except:
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/tp-yt-app-drawer/div[2]/div/div[2]/div[2]/ytd-guide-renderer/div[1]/ytd-guide-section-renderer[1]/div/ytd-guide-entry-renderer[2]/a').click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer/a/div').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/tp-yt-app-drawer/div[2]/div/div[2]/div[2]/ytd-guide-renderer/div[1]/ytd-guide-section-renderer[1]/div/ytd-guide-entry-renderer[2]/a').click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer/a/div').click()
            time.sleep(2)
        self.driver.find_element(By.ID, 'search-form').find_element(By.ID, 'search').send_keys(f'{keyword}')
        time.sleep(0.3)
        self.driver.find_element(By.ID, 'search-icon-legacy').click()
        time.sleep(3)
        video_all_list = self.driver.find_element(By.XPATH, '//*[@id="container"]/ytd-two-column-search-results-renderer')
        time.sleep(1)
        to_click_video = video_all_list.find_elements(By.XPATH, '//*[@id="contents"]/ytd-video-renderer')
        while True:
            random_value = random.randint(0, (len(to_click_video) - 1))
            try:
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
            except:
                element = to_click_video[random_value].find_element(By.ID, 'thumbnail')
                try:
                    element.click()
                except:
                    self.driver.execute_script("arguments[0].click();", element)
                break
                

    # 영상을 한 개만 봤을 때, 메인 페이지에 키워드와 관련된 영상이 별로 보이지 않음. 더군다나 짧게 보면 더 안보이게 되기 때문에 첫 영상에서 옆에 뜨는 관련영상을 시청하게 함
    def next_video(self):
        try:
            try:
                popup = self.driver.find_element(By.TAG_NAME, 'tp-yt-paper-dialog')
                popup.find_element(By.ID, 'dismiss-button').click()
            except:
                pass
            self.driver.find_element(By.CLASS_NAME, 'ytp-left-controls').find_element(By.CLASS_NAME, 'ytp-play-button').click()
            time.sleep(random.uniform(0.5, 1))
            next_video_up_class = self.driver.find_element(By.ID, 'related')
            next_videos = next_video_up_class.find_elements(By.TAG_NAME, 'ytd-compact-video-renderer')
            next_video_random_click = random.randint(0, (len(next_videos) - 1))
            try:
                next_videos[next_video_random_click].click()
            except:
                self.driver.execute_script("arguments[0].click();", next_videos[next_video_random_click])
        except:
            # next_video 작업이 실패할 경우 main_page에서 video를 select하게
            self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer').click()
            time.sleep(random.uniform(5, 6))
            video_list = self.driver.find_elements(By.TAG_NAME, 'ytd-rich-grid-row')
            random_number = random.randint(0, (len(video_list) - 1))
            youtube_to_click = video_list[random_number].find_elements(By.ID, 'thumbnail')
            random_number = random.randint(0, (len(youtube_to_click) - 1))
            element = youtube_to_click[random_number]
            print("next_videos요소를 찾지 못했습니다.")
            try:
                element.click()
            except:
                self.driver.execute_script("arguments[0].click();", element)
        
        # next_videos = self.driver.find_elements(By.TAG_NAME, 'ytd-compact-video-renderer')
        # random_number = random.randint(0, (len(next_videos) - 1))
        # element = next_videos[random_number].find_element(By.ID, 'video-title')
        # try:
        #     element.click()
        #     try:
        #         self.driver.execute_script("arguments[0].click();", element)
        #     except:
        #         pass
        # except:
        #     self.main_page_video()
            


    def main_page_video(self):
        self.driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[1]/ytd-topbar-logo-renderer').click()
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
        time.sleep(3.5)
        try:
            popup = self.driver.find_element(By.TAG_NAME, 'tp-yt-paper-dialog')
            popup.find_element(By.ID, 'dismiss-button').click()
        except:
            pass
        self.driver.find_element(By.CLASS_NAME, 'ytp-left-controls').find_element(By.CLASS_NAME, 'ytp-play-button').click()
        time.sleep(random.uniform(0.15, 0.2))
        time_str = self.driver.find_element(By.CLASS_NAME, 'notranslate').find_element(By.CLASS_NAME, 'ytp-time-duration').text
        time.sleep(random.uniform(0.15, 0.2))
        self.driver.find_element(By.CLASS_NAME, 'ytp-left-controls').find_element(By.CLASS_NAME, 'ytp-play-button').click()
        print(time_str)
        if len(time_str) == 0:
            return 0
        
        if time_str.count(':') == 3:
            match = re.match(r'(?:(\d+):)?(?:(\d+):)?(\d+):(\d+)', time_str)
                    
            if match:
                groups = match.groups()
                
                days = int(groups[0]) if groups[0] is not None else 0
                hours = int(groups[1]) if groups[1] is not None else 0
                minutes = int(groups[2])
                seconds = int(groups[3])
                
                total_seconds = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
                return total_seconds
            else:
                # 매치되지 않을 경우 예외 처리 또는 기본값 설정
                print(f"올바른 시간 형식이 아닙니다: {time_str}")
                return None
        else:
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
        time.sleep(0.5)
        viewing_time = (random.randint(1, 10)) * 60
        video_time = self.video_len()
        if video_time > viewing_time or video_time == 0:
            pass
        else:
            viewing_time = video_time
        start_time = time.time()
        print(video_time)
        print(viewing_time)
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
        time.sleep(random.uniform(2.3, 2.5))
        try:
            ad_site = None
            ad_site2 = None
            # ad_site = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
            ad_site = self.driver.find_element(By.CLASS_NAME, 'ytp-flyout-cta-description-container').find_element(By.CLASS_NAME, 'ytp-ad-text').text
            print("ad_site : ", ad_site)
            value = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
            if '재생' in value or '종료' in value:
                ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                time.sleep(int(ad_time) + random.uniform(1, 1.5))
                value2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-preview-slot').find_element(By.TAG_NAME, 'div').text
                if '재생' in value2 or '종료' in value2:
                    # ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                    ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-flyout-cta-description-container').find_element(By.CLASS_NAME, 'ytp-ad-text').text
                    print("ad_site2 : ", ad_site2)
                    ad_time = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-duration-remaining').find_element(By.TAG_NAME, 'div').text.split('0:')[1]
                    time.sleep(int(ad_time))
                else:
                    time.sleep(random.uniform(6, 6.3))
                    # ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-ad-visit-advertiser-button').find_element(By.CLASS_NAME, 'ytp-ad-button-text').text
                    ad_site2 = self.driver.find_element(By.CLASS_NAME, 'ytp-flyout-cta-description-container').find_element(By.CLASS_NAME, 'ytp-ad-text').text
                    print("ad_site2c : ", ad_site2)
                    self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
            else:
                time.sleep(random.uniform(6, 6.3))
                self.driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-container").click()
        except:
            time.sleep(1)
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
        
        
        for _ in range(2):
            name_list.append(name)
            keyword_list.append(keyword)
            
            first_ad, second_ad = self.ad_skip()
            first_ad_list.append(first_ad)
            second_ad_list.append(second_ad)
            
            viewing_time = self.user_session()
            session.append(viewing_time)
            
            title, channel_name, viewership, uploaded_date, describe, current_url, like = self.video_info()
            viewership_list.append(viewership)
            title_list.append(title)
            channel_list.append(channel_name)
            uploaded_date_list.append(uploaded_date)
            describe_list.append(describe)
            url_list.append(current_url)
            like_list.append(like)
            
            self.next_video()
        
        
        for _ in range(8):
            algorithm_random_value = random.randint(0, 1)
            print(algorithm_random_value)
            if algorithm_random_value == 0:
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
                
                self.main_page_video()
            else:
                first_ad, second_ad = self.ad_skip()
                viewing_time = self.user_session()
                title, channel_name, viewership, uploaded_date, describe, current_url, like = self.video_info()
                
                name_list.append(name)
                keyword_list.append(keyword)
                first_ad_list.append(first_ad)
                second_ad_list.append(second_ad)
                session.append(viewing_time)
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
    

