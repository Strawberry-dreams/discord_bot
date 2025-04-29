![discord_icon](https://github.com/Strawberry-dreams/discord_bot/blob/main/images/discord_icon.png)
# Discord Bot
(Module) branch contains continuous functionality files that need to run on the server.
# Files
eventalert_module.py: Print event details already registered in the event channel<br />
main.py: Import and execute other files declared as functions<br />
makeparty_module.py: Party recruitment and participation functions<br />
prohibition_module.py: Banned word filtering function<br />
<br />
# How to use
he files here are executed simultaneously through the main.py file.<br />
You can use the prefix command (default is *)<br />
The forbidden word filter runs automatically.<br />
The list of banned words can be created as a .txt file or registered as an environment variable on the server.<br />
For certain files, a specific channel ID on the server is required. (Discord developer mode needed)<br />
<br />
# Deployment method
(Local) Open Windows cmd / MacOS Terminal
```
  (All files must be in the same directory)
  cd ~/discord_bot
  python main.py
```
(For Korea) 24-hour free operation using Cloudtype Free Tier (stopped once a day)<br />
(For Overseas) Use of services such as AWS, Oracle Cloud, Heroku, Railway, and etc.<br />
<br />
