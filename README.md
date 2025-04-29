![discord_icon](https://github.com/Strawberry-dreams/discord_bot/blob/main/images/discord_icon.png)
# Discord Bot
A simple Discord bot that can be used on private servers.<br />
(Main) branch is the origin of all branches.<br />
(Single) branch contains one-time files that output embedded messages.<br />
(Module) branch contains persistent functionality files that need to run on the server.<br />
<br />
The discord_bot repository started out as a collection of personal files for use on my own servers.<br />
More features may be added in the future.<br />
Since I live in Korea, there may be many Korean words included.<br />
The parts written in Korean are not core code but simple output, so there should be no problem if you change them to English.<br />
<br />
# Main Features
You can print embed messages containing the notice contents.<br />
You can create and join parties with simple commands and buttons.<br />
You can now more easily check information about events registered on Discord server.<br />
Detects words that you designate as banned words and outputs a warning message.<br />
<br />
# What you need
Python 3.13 or later<br />
Python libraries including discord.py, git, pip, python-dotenv<br />
Server platform to deploy the Discord bot<br />
No need for a virtual environment as it only contains small functions.<br />
<br />
# Installation method
### Simple installation
```
  bash
  cd (folder you want)
  git clone https://github.com/Strawberry-dreams/discord_bot.git
  cd discord_bot
  pip install -r requirements.txt
```
### Direct installation
```
  bash
  cd (folder you want)
  git clone https://github.com/Strawberry-dreams/discord_bot.git
  cd discord_bot
  pip install discord.py
  pip install python-dotenv
```
# How to use
You can use the prefix command (default is *)<br />
The forbidden word filter runs automatically.<br />
Discord bot tokens can be written directly or set in a .env file, and server environment variables can also be registered.<br />
The list of banned words can be created as a .txt file or registered as an environment variable on the server.<br />
<br />
# Setting environment variables on the server
<br />
|      KEY      |          VALUE         |
| DISCORD_TOKEN | Your Discord bot Token |
|  BANNED_WORDS | Banned words list (JSON string) |
<br />
# Deployment method
(For Korea) 24-hour free operation using Cloudtype Free Tier (stopped once a day)<br />
(For overseas) Use of services such as AWS, Oracle Cloud, Heroku, Railway, and etc.<br />
