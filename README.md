# SpaceCrypto Bot

- [en-us] In order to change to english Readme version click [here](https://github.com/guimatheus92/Bot_SpaceCrypto/blob/main/README.md "here").
- [pt-br] Para alterar para a versão Readme em português, clique [aqui](https://github.com/guimatheus92/Bot_SpaceCrypto/blob/main/README.pt.md "aqui").

------------

This is an automation (bot) to play the game SpaceCrypto, it automatically login into the game, send ships to fight, refresh the game, new map, etc.

If you find this bot helpful to you, please donate so we can continue to improve the hard work and hours spent on this 🤯.

![Donation](https://github.com/guimatheus92/Bot_SpaceCrypto/blob/main/static/img/readme/qr_code.png)

**Donations options:**

- **BUSD/BCOIN/ETH/BNB (BEP20):** 0xf1e43519fca44d9308f889baf99531ed0de903fc
- **PayPal:** https://www.paypal.com/donate/?hosted_button_id=82CABN6CYVG6U
- **Pix:** 42a762ed-e6ec-4059-a88e-f168b9fbc63f (chave aleatória)

## Observations

- Check [Requirements](https://github.com/guimatheus92/Bot_SpaceCrypto#requirements "Requirements") topic to make sure in what environment, tools and versions we know that it works.
- I suggest you to turn off the feature `News and interests` from Windows, because the mouse might pass through it and click in some card without us know. You can turn off this feature from [Turn news and interests feature on and off](https://support.microsoft.com/en-us/windows/stay-up-to-date-with-news-and-interests-a39baa08-7488-4169-9ed8-577238f46f8f) guide.

### Does your bot is in endless loop and it's doing nothing? So read the note below!

> ### The problem now, is that it's not matching the same images I shared from the one you have on your screen. So you'll need to change those in order to make it work. So you'll need to replace the same images with the exactly same names in the path `/static/img/game`. 
> ### All images taken from the game was from a Full HD screen and scale at 100%. So if your bot is not working, make sure that your scale is at least 100%. After that, get all pictures again and save them as `.png` format.

## Main Steps

In a breafy way you'll need to:

1. Download `Python`
2. Install python packages from `requirements.txt`
3. Adjust `screen scale` to `100%` if needed
4. Download `Brave` browser (best option)
5. Change options on `config.yaml` file if needed
6. Create `Telegram` bot if needed

## Project structure
    .
    └── Bot_SpaceCrypto
        ├── main.py                     # setup our app
        ├── bot.py                      # all bot movements
        ├── controllers.py              # all controllers to help the bot to run
        ├── config.yaml                 # all configurations and options to run
        └── logs                        # all log files are saved daily here
        └── static
            ├── img
                ├── game                # all images related to game to run the bot
                ├── readme              # all images related to repository
                ├── screenshot          # all images taken from screenshot (folder will create automatically)

## Tutorial

The tutorial on how to install and use this bot can be found on [GitHub Wiki](https://github.com/guimatheus92/Bot_SpaceCrypto/wiki/How-to-execute-SpaceCrypto-bot "GitHub Wiki") page.

The tutorial on how to use Brave browser for this bot can be found on [GitHub Wiki](https://github.com/guimatheus92/Bot_SpaceCrypto/wiki/How-to-enable-multiaccount-feature-on-Bot "GitHub Wiki") page.

#### Some settings can be changed in the config.yaml file. If you change it, don't forget to restar the bot so that the new settings are activated.

## Changelog

- **17/02/2022**:
    - Improved the function to send pictures to Telegram
    - Improved the way it was looking for errors on game
    - Improved function to find the button `confirm`
- **16/02/2022**: Released bot first version

## Requirements

Browser: `Brave: Version 1.34.81 Chromium: 97.0.4692.99`

#### ⚠️ I really advise you to use the Brave browser instead of others, for so many reasons, especially if you want to use multiaccount feature.

#### For Brave tutorial, check [here](https://github.com/guimatheus92/Bot_SpaceCrypto/wiki/How-to-enable-multiaccount-feature-on-Bot "here").

------------

Windows version:
- `Windows 10`
- `Windows 11`

Python version (**Python 4+ versions DOES NOT work!**):
```python
Python 3.9.9
```

The requirements can be found in `requirements.txt` file also.
This project utilizes the following requirements:

    APScheduler==3.6.3
    asyncio==3.4.3    
    numpy==1.21.4
    opencv-python==4.5.4.60
    pandas==1.1.5
    pathlib==1.0.1
    Pillow==8.4.0
    PyAutoGUI==0.9.53
    python-telegram-bot==13.9
    pywin32==303
    pywinauto==0.6.8
    PyYAML==6.0
    requests==2.26.0
    tzlocal==4.1

Monitor scale: `100%`

## Features

- Schedule the refresh of the game in a period of time
- Schedule sending ships to fight in a period of time
- Delete old files and folders if you want automatically
- Connect into wallet
- Connect, signin, unlock Metamask
- Check if is there new map available
- Take screenshot of errors, new maps, sending to fight, etc
- Send Telegram message
- Works with as many accounts as you need

## YAML file configurations and options explained

**1. bot_options**
- **create_logfiles**: You can enable the creation of log in files availabe in the folder `logs`
- **delete_old_logfiles**: You can enable the deletion of old log files and keep today's date file.
- **delete_old_folders**: You can enable the deletion of older folders and keep today's date folders.
- **enable_multiaccount**: You can enable the multiaccount feature.
- **multiaccount_names**: You can set the account/profile names from Brave browser in each line.
- **refresh_browser_time**: You can set the time where the browser will be refreshed by the keys: CTRL + SHIFT + R
**1.1 metamask_options**
	- **enable_login_metamask**: You can enable the login in Metamask when it's locked and needs password to unlock
	- **metamask_password**: If `enable_login_metamask` option is set to `True`, you can pass the password to unlock Metamask.

**2. telegram_options**
- **telegram_integration**: You can enable the integration from log messages to Telegram messages as well
- **telegram_token**: If `telegram_integration` is set to `True`, you can pass the token from your Telegram bot.
- **telegram_chatid**: If `telegram_integration` is set to `True`, you can pass the chat_id number from your Telegram bot. Once the number is wrote, it doesn't change anymore.

**3. game_options**
- **work_ships_options**: You can set the fight mode for your ships. 
    - The option `all` send all ships to fight, whenever the fight button is available.
    - The option `full` send all ships to fight regardless of the rarity and only when the ammo is `100%`.
- **work_ships_time**: You can set the time when bot will send ships to fight automatically.
- **refresh_ships_time**: You can set the time when bot will just refresh the game, so the game don't disconnect.
- **chest_screenshot_time**: You can set the time when bot will take a screenshot from your coins from the game.
- **clicks_count**: You can set how many ships you have, so the bot will not keep clicking more than you need.
- **drag_count**: You can set for how many times you want the bot to drag the list searching for ships that has ammo.

## Improvements

- [ ] More options in sending ships to fight
- [ ] Sort ships automatically set from user

## Conclusion

1. Want my code? [Grab it here](https://github.com/guimatheus92/Bot_SpaceCrypto "Grab it here") 📎
2. Want the tutorial of how to use it? [Go to Wiki](https://github.com/guimatheus92/Bot_SpaceCrypto/wiki "Go to here") ✔️
3. New ideas for this app? Help me to improve it ❤️
4. Want something else added to this tutorial? Add an issue to the repo ⚠️
