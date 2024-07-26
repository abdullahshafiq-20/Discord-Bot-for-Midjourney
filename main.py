import time
import random
import pandas as pd
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidElementStateException, WebDriverException

# Time delay variables
time_delay_loading_discord_login = (2, 4)
time_delay_after_login = (4, 5)
time_delay_loading_channel = (2, 4)
time_delay_after_typing_imagine = 1
time_delay_between_words_min = 0.000000001
time_delay_between_words_max = 0.000000002
time_delay_after_typing_message = 2
time_delay_retry_sending_message_min = 2
time_delay_retry_sending_message_max = 4
time_delay_after_message_sent_min = 3
time_delay_after_message_sent_max = 5
time_delay_human_like_browsing_min = 0.01
time_delay_human_like_browsing_max = 0.03

time_delay_after_10_prompts_min = 100  # 4 minutes in seconds
time_delay_after_10_prompts_max = 120  # 6 minutes in seconds


email = ""
password = ""
channel_url = ""
css_selector = "#app-mount > div.appAsidePanelWrapper_bd26cc > div.notAppAsidePanel_bd26cc > div.app_bd26cc > div > div.layers_d4b6c5.layers_a01fb1 > div > div > div > div > div.chat_a7d72e > div.content_a7d72e > main > form > div > div > div.scrollableContainer_d0696b.themedBackground_d0696b > div > div.textArea_d0696b.textAreaSlate_d0696b.slateContainer_e52116 > div > div.markup_f8f345.editor_a552a6.slateTextArea_e52116.fontSize16Padding_d0696b > div"
csv_file = "ai_image_prompts.csv"


def random_sleep(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))


def chrome_opt():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver


def human_like_browsing(driver):
    try:
        driver.switch_to.window(driver.current_window_handle)

        viewport_width = driver.execute_script("return window.innerWidth;")
        viewport_height = driver.execute_script("return window.innerHeight;")

        num_steps = random.randint(50, 100)

        start_x, start_y = random.randint(0, viewport_width - 1), random.randint(0, viewport_height - 1)
        end_x, end_y = random.randint(0, viewport_width - 1), random.randint(0, viewport_height - 1)

        step_x = (end_x - start_x) / num_steps
        step_y = (end_y - start_y) / num_steps

        actions = ActionChains(driver)

        actions.move_by_offset(start_x, start_y).perform()

        current_x, current_y = start_x, start_y

        for _ in range(num_steps):
            current_x += step_x
            current_y += step_y

            if 0 <= current_x < viewport_width and 0 <= current_y < viewport_height:
                actions.move_by_offset(step_x, step_y)
                actions.perform()
                time.sleep(random.uniform(time_delay_human_like_browsing_min, time_delay_human_like_browsing_max))
            else:
                break

        actions.move_to_element(driver.find_element(By.TAG_NAME, "body")).perform()

        time.sleep(random.uniform(0.5, 2))

    except WebDriverException as e:
        print(f"WebDriver exception during human-like browsing")
    except Exception as e:
        print(f"An unexpected error occurred during human-like browsing")


def login_to_discord(driver, email, password):
    try:
        email_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys(email)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print("Login information submitted successfully.")

        time.sleep(10)
        print("Successfully logged in to Discord.")

    except Exception as e:
        print(f"An error occurred during login: {e}")

    return


def send_message(driver, content):
    max_attempts = 3
    counter = 0
    for attempt in range(max_attempts):
        try:
            input_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )

            if counter == 0:
                counter += 1
                for char in "/imagine ":
                    input_element.send_keys(char)
                    time.sleep(random.uniform(0.01, 0.03))
                time.sleep(time_delay_after_typing_imagine)

            words = content.split()

            for word in words:
                for char in word:
                    input_element.send_keys(char)
                    time.sleep(random.uniform(time_delay_between_words_min, time_delay_between_words_max))

                input_element.send_keys(Keys.SPACE)
                time.sleep(random.uniform(0.0001, 0.0002))

            time.sleep(time_delay_after_typing_message)

            input_element.send_keys(Keys.RETURN)
            print(f"{Fore.GREEN}Message sent successfully: /imagine {content[:50]}...")
            counter = 0
            max_attempts = 0
            return True

        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} failed. Error: Retrying...")
            time.sleep(random.uniform(time_delay_retry_sending_message_min, time_delay_retry_sending_message_max))

    print("Failed to send message after multiple attempts.")
    return False


def main():
    csv_filename = csv_file

    driver = chrome_opt()
    driver.get('https://discord.com/login')
    random_sleep(*time_delay_loading_discord_login)

    login_to_discord(driver, email, password)
    random_sleep(*time_delay_after_login)

    driver.get(channel_url)
    random_sleep(*time_delay_loading_channel)

    data = pd.read_csv(csv_filename)
    prompt_count = 0
    for index, row in data.iterrows():
        content = row[0]
        if pd.isna(content) or content == "":
            break
        if send_message(driver, content):
            print(f"{Fore.GREEN}Message {index + 1 } ent successfully: {content}")
            prompt_count += 1
        else:
            print(f"Failed to send message {index}: {content}")
        
        human_like_browsing(driver)
        random_sleep(time_delay_after_message_sent_min, time_delay_after_message_sent_max)
        
        # Check if 10 prompts have been sent
        if prompt_count % 10 == 0:
            delay_time = random.uniform(time_delay_after_10_prompts_min, time_delay_after_10_prompts_max)
            print(f"10 prompts sent. Waiting for approximately {delay_time:.2f} seconds...")
            random_sleep(time_delay_after_10_prompts_min, time_delay_after_10_prompts_max)
    
    print(f"Finished sending {prompt_count} prompts.")
    print("Exiting...")
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
