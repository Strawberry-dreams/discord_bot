![discord_icon](https://github.com/Strawberry-dreams/discord_bot/blob/main/images/discord_icon.png)
# Discord Bot
(Single) branch contains one-time files that output embedded messages.<br />
# Files
announcement_discord.py: Output an embedded message in the notification channel<br />
eventalert_discord.py: Print event details already registered in the event channel<br />
hello_discord.py: Check if the bot is working<br />
instruction_discord.py: Output an embedded message in the instruction channel<br />
laboratory_discord.py: Output an embedded message in the laboratory channel<br />
makeparty_discord.py: Party recruitment and participation functions<br />
prohibition_discord.py: Banned word filtering function<br />
rule_discord.py: Output an embedded message in the rule channel<br />
suggestion_discord.py: Output 2 embedded messages in the suggestion channel<br />
update_discord.py: Output an embedded message in the update channel<br />
<br />
# How to use
The files here work alone.<br />
You can use the prefix command (default is *)<br />
The forbidden word filter runs automatically.<br />
Discord bot tokens can be entered directly or set in a .env file.<br />
The list of banned words can be created as a .txt file.<br />
For certain files, a specific channel ID on the server is required. (Discord developer mode needed)<br />
<br />
# Deployment method
(Local) Open Windows cmd / MacOS Terminal
```
  cd ~/discord_bot
  python (file_name)
```
<br />
