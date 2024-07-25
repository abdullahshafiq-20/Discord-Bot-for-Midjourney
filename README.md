# 🤖 Discord AI Image Generator Bot

Welcome to the Discord AI Image Generator Bot repository! This bot automates the process of generating AI images using Discord's `/imagine` command. 🎨✨

## 🌟 Features

- 🔐 Automated login to Discord
- 📊 Reads prompts from a CSV file
- 🖼️ Sends `/imagine` commands to a specified Discord channel
- 🕹️ Simulates human-like browsing behavior
- ⏱️ Implements random delays for natural interaction

## 🛠️ Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## 📦 Dependencies

Install the required packages using:

```
pip install time random pandas selenium
```
```
pip install --upgrade pandas selenium
```
## 🚀 Getting Started

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Discord-Bot-for-Midjourney.git
   ```

2. Navigate to the project directory:
   ```
   cd Discord-Bot-for-Midjourney
   ```

3. Set up your environment variables or modify the script to include your Discord credentials and channel URL.

4. Prepare your `ai_image_prompts.csv` file with the image prompts you want to generate.

5. Run the script:
   ```
   python main.py
   ```

## ⚙️ Configuration

Modify the following variables in the script to customize the bot's behavior:

### 🔑 Credentials and URLs
- `email`: Your Discord email
- `password`: Your Discord password
- `channel_url`: The URL of the Discord channel where you want to send the commands

### 📁 File Paths
- `csv_file`: The name of your CSV file containing image prompts

### 🎯 CSS Selector
- `css_selector`: The CSS selector for the Discord message input field

  right click on message input field -> inspection panel will open -> right click on selcted <div> -> in copy, copy the selector.

### ⏱️ Time Delay Variables
- `time_delay_loading_discord_login`: (2, 4)
- `time_delay_after_login`: (4, 5)
- `time_delay_loading_channel`: (2, 4)
- `time_delay_after_typing_imagine`: 1
- `time_delay_between_words_min`: 0.00001
- `time_delay_between_words_max`: 0.00002
- `time_delay_after_typing_message`: 2
- `time_delay_retry_sending_message_min`: 2
- `time_delay_retry_sending_message_max`: 4
- `time_delay_after_message_sent_min`: 3
- `time_delay_after_message_sent_max`: 5
- `time_delay_human_like_browsing_min`: 0.01
- `time_delay_human_like_browsing_max`: 0.03

Adjust these values to fine-tune the bot's behavior and timing. Time delays are in seconds and can be integers or floats. Ranges are represented as tuples (min, max).

## 🚨 Disclaimer

This bot is for educational purposes only. The creator of this bot does not endorse or encourage its use in violation of any terms of service or rules.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/discord-ai-image-generator-bot/issues).

## 📝 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 🙏 Acknowledgements

- Selenium WebDriver
- Pandas library
- Discord platform

Happy image generating! 🎉🖼️
