from crawler.crawler import *
from DB.to_db import insert_db
import DB.to_es
import requests as rq
import pandas as pd
from datetime import datetime

def main() -> None:

    proxies: dict[str,str] = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }


if __name__ == "__main__":
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    try:
        # main()
        bot = YouTubeBot()
        result_df = bot.run()  # Save the returned DataFrame as a variable
        bot.cleanup()
        table_name = 'crawl'
        insert_db(df=result_df, table_name=table_name)
        print("Script executed successfully.")
        result_df['@timestamp'] = now
        DB.to_es.youtube_data(df=result_df)

    except YouTubeBotError as e:
        print(f"Custom error raised: {e}")
        error_data = {'ErrorMessage': str(e), '@timestamp': now}
        error_df = pd.DataFrame([error_data])
        DB.to_es.youtube_failed_log(df=error_df)
