from crawler.crawler import *
from DB.to_db import insert_db
import psutil
import os


if __name__ == "__main__":
    try:
        bot = YouTubeBot()
        result_df = bot.run()  # Save the returned DataFrame as a variable
        bot.cleanup()
        table_name = "crawl" 
        insert_db(df=result_df, table_name=table_name)
        print("Script executed successfully.")
    except YouTubeBotError as e:
        print(f"Custom error raised: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
