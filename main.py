import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import time
import os
import random
import pandas as pd
import pickle
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import MoveTargetOutOfBoundsException, NoSuchElementException, StaleElementReferenceException, TimeoutException, InvalidElementStateException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

class DiscordBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Discord Bot for Midjourney AI")
        self.master.geometry("600x820")  # Increased height to accommodate new input
        self.bot_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        
        # Frame for input fields
        input_frame = ctk.CTkFrame(self.master)
        input_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1)

        # Email
        ctk.CTkLabel(input_frame, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(input_frame, width=300)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Password
        ctk.CTkLabel(input_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ctk.CTkEntry(input_frame, width=300, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Channel Link
        ctk.CTkLabel(input_frame, text="Channel Link:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.channel_link_entry = ctk.CTkEntry(input_frame, width=300)
        self.channel_link_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # CSV File Selection
        ctk.CTkLabel(input_frame, text="CSV File:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        csv_frame = ctk.CTkFrame(input_frame)
        csv_frame.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        csv_frame.grid_columnconfigure(0, weight=1)
        self.csv_file_entry = ctk.CTkEntry(csv_frame, width=250)
        self.csv_file_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.csv_file_button = ctk.CTkButton(csv_frame, text="Browse", command=self.browse_csv, width=80)
        self.csv_file_button.grid(row=0, column=1)

        # Frame for time settings
        time_frame = ctk.CTkFrame(self.master)
        time_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        time_frame.grid_columnconfigure(1, weight=1)

        # Time between sending prompts of batch 10
        ctk.CTkLabel(time_frame, text="Time between batches (seconds):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.batch_time_entry = ctk.CTkEntry(time_frame, width=100)
        self.batch_time_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Time on login page
        ctk.CTkLabel(time_frame, text="Time on login page (seconds):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.login_page_time_entry = ctk.CTkEntry(time_frame, width=100)
        self.login_page_time_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Time waiting for dashboard to load
        ctk.CTkLabel(time_frame, text="Dashboard load time (seconds):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.dashboard_load_time_entry = ctk.CTkEntry(time_frame, width=100)
        self.dashboard_load_time_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(time_frame, text="Typing speed (words per minute):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.typing_speed_entry = ctk.CTkEntry(time_frame, width=100)
        self.typing_speed_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.typing_speed_entry.insert(0, "2500")  # Default value
        self.typing_speed_entry.configure(placeholder_text="e.g., 2500")

        # Time waiting for channel to load
        ctk.CTkLabel(time_frame, text="Channel load time (seconds):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.channel_load_time_entry = ctk.CTkEntry(time_frame, width=100)
        self.channel_load_time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.delete_checkpoint_button = ctk.CTkButton(self.master, text="Delete Checkpoint", command=delete_checkpoint)
        self.delete_checkpoint_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Start Button
        self.start_button = ctk.CTkButton(self.master, text="Start Bot", command=self.toggle_bot, height=40)
        self.start_button.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.master, orientation="horizontal")
        self.progress_bar.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

        # Command Line Output
        self.output_text = ctk.CTkTextbox(self.master, height=200, width=560, state="disabled")
        self.output_text.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")



        # Status Label
        # self.status_label = ctk.CTkLabel(self.master, text="", height=30)
        # self.status_label.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def browse_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.csv_file_entry.delete(0, tk.END)
        self.csv_file_entry.insert(0, filename)

    def toggle_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.stop_event.set()
            self.start_button.configure(text="Start Bot")
            self.log_output("Stopping bot...")
        else:
            self.stop_event.clear()
            self.start_bot()
            self.start_button.configure(text="Stop Bot")

    def start_bot(self):
        # Get values from input fields
        email = self.email_entry.get()
        password = self.password_entry.get()
        channel_url = self.channel_link_entry.get()
        csv_file = self.csv_file_entry.get()
        batch_time = float(self.batch_time_entry.get())
        login_page_time = float(self.login_page_time_entry.get())
        dashboard_load_time = float(self.dashboard_load_time_entry.get())
        channel_load_time = float(self.channel_load_time_entry.get())

        # Update global variables
        global time_delay_after_10_prompts_min, time_delay_after_10_prompts_max
        global time_delay_loading_discord_login
        global time_delay_after_login
        global time_delay_loading_channel

        time_delay_after_10_prompts_min = batch_time
        time_delay_after_10_prompts_max = batch_time + 20
        time_delay_loading_discord_login = (login_page_time, login_page_time + 2)
        time_delay_after_login = (dashboard_load_time, dashboard_load_time + 1)
        time_delay_loading_channel = (channel_load_time, channel_load_time + 2)

        # Start the bot in a new thread
        self.bot_thread = threading.Thread(target=self.run_bot, args=(email, password, channel_url, csv_file))
        self.bot_thread.start()

    def run_bot(self, email, password, channel_url, csv_file):
        self.log_output("Bot starting...")
        self.log_output("Bot starting...")
        
        try:
            self.log_output("Opening Chrome...")
            driver = chrome_opt()
            self.log_output("Chrome opened successfully.")

            self.log_output("Navigating to Discord login page...")
            driver.get('https://discord.com/login')
            random_sleep(*time_delay_loading_discord_login)
            self.log_output("Discord login page loaded.")

            self.log_output("Entering login credentials...")
            login_to_discord(driver, email, password)
            self.log_output("Login credentials entered, waiting for login process...")
            random_sleep(*time_delay_after_login)
            self.log_output("Login successful.")

            self.log_output(f"Navigating to channel: {channel_url}")
            driver.get(channel_url)
            random_sleep(*time_delay_loading_channel)
            self.log_output("Channel loaded successfully.")

            self.log_output(f"Reading CSV file: {csv_file}")
            data = pd.read_csv(csv_file)
            prompt_count = 0
            start_index = load_checkpoint()
            total_prompts = len(data)

            if start_index > 0:
                self.log_output(f"Resuming from checkpoint: Starting at index {start_index}")
            else:
                self.log_output("Starting from the beginning of the CSV file")

            for index, row in data.iterrows():
                if self.stop_event.is_set():
                    self.log_output("Bot stopped.")
                    self.log_output("Bot operation manually stopped.")
                    break
                if index < start_index:
                    continue
                content = row[0]
                if pd.isna(content) or content == "":
                    self.log_output("Reached end of valid data in CSV file.")
                    break
                try:
                    self.log_output(f"Attempting to send message {index + 1}: {content[:50]}...")
                    if send_message(driver, content, float(self.typing_speed_entry.get())):
                        self.log_output(f"Message {index + 1} sent successfully")
                        self.log_output(f"{Fore.GREEN}Message {index + 1} sent successfully: /imagine {content[:50]}...")
                        prompt_count += 1
                        save_checkpoint(index + 1)
                        self.log_output(f"Checkpoint saved at index {index + 1}")
                    else:
                        self.log_output(f"Failed to send message {index}")
                        self.log_output(f"Failed to send message {index}: {content}")
                    
                    self.log_output("Performing human-like browsing...")
                    human_like_browsing(driver)
                    delay = random.uniform(time_delay_after_message_sent_min, time_delay_after_message_sent_max)
                    self.log_output(f"Waiting for {delay:.2f} seconds before next message...")
                    random_sleep(time_delay_after_message_sent_min, time_delay_after_message_sent_max)
                    
                    if prompt_count % 10 == 0:
                        delay_time = random.uniform(time_delay_after_10_prompts_min, time_delay_after_10_prompts_max)
                        self.log_output(f"10 prompts sent. Waiting for {delay_time:.2f} seconds...")
                        self.log_output(f"10 prompts sent. Waiting for approximately {delay_time:.2f} seconds...")
                        random_sleep(time_delay_after_10_prompts_min, time_delay_after_10_prompts_max)
                    
                    # Update progress bar
                    self.update_progress((index + 1) / total_prompts)
                except Exception as e:
                    self.log_output(f"An error occurred: {e}")
                    self.log_output(f"An error occurred while sending message {index}: {e}")
                    save_checkpoint(index)
                    self.log_output(f"Checkpoint saved at index {index} due to error")
                    driver.quit()
                    return
            
            self.log_output(f"Finished sending {prompt_count} prompts.")
            self.log_output(f"Finished sending {prompt_count} prompts.")
            time.sleep(5)
            driver.quit()
            self.log_output("Chrome browser closed.")

        except Exception as e:
            self.log_output(f"An error occurred: {e}")
            self.log_output(f"A critical error occurred: {e}")
        finally:
            self.start_button.configure(text="Start Bot")
            self.log_output("Bot operation completed or stopped.")

    def update_status(self, message):
        self.master.after(0, lambda: self.status_label.configure(text=message))

    def log_output(self, message):
        self.master.after(0, lambda: self._log_output(message))

    def _log_output(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")
        self.master.update_idletasks()

    def update_progress(self, value):
        self.master.after(0, lambda: self.progress_bar.set(value))

    def update_status(self, message):
        self.status_label.configure(text=message)
        self.master.update_idletasks()

    def log_output(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")
        self.master.update_idletasks()

    def update_progress(self, value):
        self.progress_bar.set(value)
        self.master.update_idletasks()

def chrome_opt():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def random_sleep(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))

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
        print("Waiting for email field to be visible...")
        email_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "email"))
        )   
        print("Email field found. Entering email...")
        email_field.send_keys(email)

        print("Locating password field...")
        password_field = driver.find_element(By.NAME, "password")
        print("Entering password...")
        password_field.send_keys(password)
        print("Submitting login information...")
        password_field.send_keys(Keys.RETURN)
        print("Login information submitted successfully.")

        time.sleep(10)
        print("Waiting period after login completed.")
        print("Successfully logged in to Discord.")

    except Exception as e:
        print(f"An error occurred during login: {e}")

def send_message(driver, content, typing_speed):
    max_attempts = 3
    counter = 0
    for attempt in range(max_attempts):
        try:
            print(f"Attempt {attempt + 1} to send message...")
            input_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            print("Message input field found and clickable.")

            if counter == 0:
                counter += 1
                print("Typing '/imagine '...")
                for char in "/imagine ":
                    input_element.send_keys(char)
                    time.sleep(random.uniform(0.01, 0.03))
                print("Waiting after typing '/imagine '...")
                time.sleep(time_delay_after_typing_imagine)

            print(f"Typing message content: {content[:50]}...")
            words = content.split()
            total_chars = sum(len(word) for word in words) + len(words) - 1
            total_time = (len(words) / typing_speed) * 60
            avg_delay = total_time / total_chars

            for word in words:
                for char in word:
                    input_element.send_keys(char)
                    time.sleep(random.uniform(avg_delay * 0.5, avg_delay * 1.5))

                if word != words[-1]:
                    input_element.send_keys(Keys.SPACE)
                    time.sleep(random.uniform(avg_delay * 0.5, avg_delay * 1.5))

            print("Waiting after typing message...")
            time.sleep(time_delay_after_typing_message)

            print("Sending message...")
            input_element.send_keys(Keys.RETURN)
            print(f"{Fore.GREEN}Message sent successfully: /imagine {content[:50]}...")
            counter = 0
            max_attempts = 0
            return True

        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}. Retrying...")
            time.sleep(random.uniform(time_delay_retry_sending_message_min, time_delay_retry_sending_message_max))

    print("Failed to send message after multiple attempts.")
    return False

def save_checkpoint(index):
    with open('checkpoint.pkl', 'wb') as f:
        pickle.dump(index, f)

def load_checkpoint():
    try:
        with open('checkpoint.pkl', 'rb') as f:
            checkpoint = pickle.load(f)
            print(f"Loaded checkpoint: Starting from index {checkpoint}")
            return checkpoint
    except FileNotFoundError:
        print("No checkpoint found. Starting from the beginning.")
        return 0
    
def delete_checkpoint():
    try:
        os.remove('checkpoint.pkl')
        print("Checkpoint file deleted. The bot will start from the beginning on the next run.")
    except FileNotFoundError:
        print("No checkpoint file found. The bot will start from the beginning on the next run.")

# Global variables
css_selector = '#app-mount > div.appAsidePanelWrapper_bd26cc > div.notAppAsidePanel_bd26cc > div.app_bd26cc > div > div.layers_d4b6c5.layers_a01fb1 > div > div > div > div > div.chat_a7d72e > div.content_a7d72e > main > form > div > div > div.scrollableContainer_d0696b.themedBackground_d0696b > div > div.textArea_d0696b.textAreaSlate_d0696b.slateContainer_e52116 > div > div.markup_f8f345.editor_a552a6.slateTextArea_e52116.fontSize16Padding_d0696b > div'
time_delay_after_10_prompts_min = 30
time_delay_after_10_prompts_max = 60
time_delay_loading_discord_login = (5, 7)
time_delay_after_login = (5, 6)
time_delay_loading_channel = (5, 7)
time_delay_after_message_sent_min = 2
time_delay_after_message_sent_max = 5
time_delay_human_like_browsing_min = 0.01
time_delay_human_like_browsing_max = 0.02
time_delay_after_typing_imagine = 0.5
time_delay_between_words_min = 0.02
time_delay_between_words_max = 0.05
time_delay_after_typing_message = 1
time_delay_retry_sending_message_min = 2
time_delay_retry_sending_message_max = 5

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiscordBotGUI(root)
    root.mainloop()