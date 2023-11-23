from crawler.crawler import *
from DB.to_db import insert_db
import psutil
import os


if __name__ == "__main__":
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_info = py.memory_info()
    print(f"현재 메모리 사용량: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"가상 메모리 사용량: {memory_info.vms / 1024 / 1024:.2f} MB")
    try:
        bot = YouTubeBot()
        result_df = bot.run()  # Save the returned DataFrame as a variable
        pid = os.getpid()
        py = psutil.Process(pid)
        memory_info = py.memory_info()
        print(f"현재 메모리 사용량: {memory_info.rss / 1024 / 1024:.2f} MB")
        print(f"가상 메모리 사용량: {memory_info.vms / 1024 / 1024:.2f} MB")
        bot.cleanup()
        print("Script executed successfully.")
    except YouTubeBotError as e:
        print(f"Custom error raised: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")