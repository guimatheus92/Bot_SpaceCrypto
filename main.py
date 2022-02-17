import os
import asyncio
import tzlocal
from bot import reload_page, start_game, login_metamask, new_map, SetTrigger, skip_error_on_game, how_many_coins, first_start, send_ships_to_fight, refresh_game, continue_fighting
from controllers import get_browser, countdown_timer, setup_logger, initialize_pyautogui, read_configurations, delete_log_files, delete_folders
from pywinauto import Desktop
from itertools import cycle
from apscheduler.schedulers.background import BackgroundScheduler

try:
    streamConfig = read_configurations()
    refresh_ships_time = streamConfig['game_options']['refresh_ships_time']
    work_ships_time = streamConfig['game_options']['work_ships_time']
    refresh_browser_time = streamConfig['bot_options']['refresh_browser_time']
    enable_multiaccount = streamConfig['bot_options']['enable_multiaccount']
    chest_screenshot_time = streamConfig['game_options']['chest_screenshot_time']    
except FileNotFoundError:
    print('Error: config.yaml file not found, make sure config.yaml are placed in the folder..')
    exit()

async def main():
    logger = setup_logger(telegram_integration=True)

    # Init message
    print('\nPress Ctrl-C to quit at anytime!\n' )

    hello_world = """
    #**************************** SpaceCrypto Bot *******************************#
    #────────────────────────────────────────────────────────────────────────────#
    #─██████████████─██████████████─██████████████─██████████████─██████████████─#
    #─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─#
    #─██░░██████████─██░░██████░░██─██░░██████░░██─██░░██████████─██░░██████████─#
    #─██░░██─────────██░░██──██░░██─██░░██──██░░██─██░░██─────────██░░██─────────#
    #─██░░██████████─██░░██████░░██─██░░██████░░██─██░░██─────────██░░██████████─#
    #─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██─────────██░░░░░░░░░░██─#
    #─██████████░░██─██░░██████████─██░░██████░░██─██░░██─────────██░░██████████─#
    #─────────██░░██─██░░██─────────██░░██──██░░██─██░░██─────────██░░██─────────#
    #─██████████░░██─██░░██─────────██░░██──██░░██─██░░██████████─██░░██████████─#
    #─██░░░░░░░░░░██─██░░██─────────██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─#
    #─██████████████─██████─────────██████──██████─██████████████─██████████████─#
    #────────────────────────────────────────────────────────────────────────────#
    #****************************************************************************#
    #*************** Please donate to help improve the hard work ♥ **************#
    #****************************************************************************#
    #** BUSD/BCOIN/ETH/BNB (BEP20): 0xf1e43519fca44d9308f889baf99531ed0de903fc **#
    #** PayPal: https://www.paypal.com/donate/?hosted_button_id=82CABN6CYVG6U ***#
    #*********** Nubank: https://nubank.com.br/pagar/1jxcl/z5fyuL6S28 ***********#
    #**************** Pix: 42a762ed-e6ec-4059-a88e-f168b9fbc63f *****************#
    #****************************************************************************# 
    """

    print(hello_world)
            
    # Initialize pyautogui library
    await asyncio.create_task(initialize_pyautogui())

    # Delete old log files
    await asyncio.create_task(delete_log_files())

    # Delete old folders
    await asyncio.create_task(delete_folders())

    # Countdown timer before start the bot
    await asyncio.create_task(countdown_timer())

    logger.info('------------------- New Execution ----------------\n')
    logger.info('Donate on BUSD/BCOIN/ETH/BNB (BEP20): 0xf1e43519fca44d9308f889baf99531ed0de903fc')
    logger.info('Donate on PayPal: https://www.paypal.com/donate/?hosted_button_id=82CABN6CYVG6U')
    logger.info('Donate on Nubank: https://nubank.com.br/pagar/1jxcl/z5fyuL6S28')
    logger.info('Donate on Pix: 42a762ed-e6ec-4059-a88e-f168b9fbc63f')
    logger.info('Starting Bot..... Bot started!')

    # Create a scheduler for certain functions
    scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
    trigger = SetTrigger()

    if refresh_ships_time > 4:
        logger.info('Scheduling to the refresh game every %s minute(s)!' % (refresh_ships_time))
        # - Do a full review on games        
        scheduler.add_job(trigger.UpdateSetRefresh, 'interval', minutes=refresh_ships_time, id='1', name='refresh_game', misfire_grace_time=180)        

    if work_ships_time > 9:
        logger.info('Scheduling the time for ships to fight every %s minute(s)!' % (work_ships_time))
        # - Send ships to work
        scheduler.add_job(trigger.UpdateSetWork, 'interval', minutes=work_ships_time, id='2', name='send_ships_to_work', misfire_grace_time=300)

    if refresh_browser_time > 29:
        logger.info('Scheduling the time for refreshing the browser every %s minute(s)!' % (refresh_browser_time))
        # - Do a full review on games        
        scheduler.add_job(trigger.UpdateSetReload, 'interval', minutes=refresh_browser_time, id='3', name='refresh_browser_time', misfire_grace_time=900)

    if chest_screenshot_time > 29:
        logger.info('Scheduling to take screenshot from coins every %s minute(s)!' % (chest_screenshot_time))
        # - Do a full review on games        
        scheduler.add_job(trigger.UpdateSetCoin, 'interval', minutes=chest_screenshot_time, id='4', name='chest_screenshot_time', misfire_grace_time=180)            

    if len(scheduler.get_jobs()) > 0:
        scheduler.start()

    applications, website_browser = get_browser()
    logger.info('Number of accounts that the bot will run: %s' % (len(applications)))
    
    if 'Space' not in website_browser:
        logger.error('Space Crypto website not open yet, please open the browser before starting this bot! Exiting bot...')
        os._exit(0)
    else:
        if len(applications) > 0:            
            # Iterate through applications *once*, starting the app and creating the related bot name for future use.
            for app in applications:
                if enable_multiaccount != False:
                    print('Going to bot: ' + str(app[1]))
                    browser = Desktop(backend="uia").windows(title=app[0])[0]
                    browser.set_focus()
                    app.append(browser)
                await asyncio.create_task(first_start(app_name=app[1]))

            bot_executions_refresh = []
            bot_executions_work = []
            bot_executions_reload = []
            bot_executions_coin = []
            # Cycle through the bots in one loop rather than restarting the loop in an infinite loop
            for app in cycle(applications):
                if enable_multiaccount != False:
                    print('Going to bot: ' + str(app[1]))
                    app[2].set_focus()

                # Steps of this bot:
                # - Connect Wallet
                await asyncio.create_task(start_game(app_name=app[1]))
                # - Login Metamask
                await asyncio.create_task(login_metamask(app_name=app[1]))
                # - New map feature
                await asyncio.create_task(new_map(app_name=app[1]))
                # - Continue to play
                await asyncio.create_task(continue_fighting(app_name=app[1]))
                # - Check for errors on game
                await asyncio.create_task(skip_error_on_game(app_name=app[1]))

                # - Time to call some functions
                if trigger.set_refresh != False:
                    if app[1] not in bot_executions_refresh:
                        bot_executions_refresh.append(app[1])
                        await asyncio.create_task(refresh_game(app_name=app[1]))                
                if trigger.set_work != False:
                    if app[1] not in bot_executions_work:
                        bot_executions_work.append(app[1])
                        await asyncio.create_task(send_ships_to_fight(app_name=app[1]))
                if trigger.set_reload != False:
                    if app[1] not in bot_executions_reload:
                        bot_executions_reload.append(app[1])
                        await asyncio.create_task(reload_page(app_name=app[1]))
                if trigger.set_coin != False:
                    if app[1] not in bot_executions_coin:
                        bot_executions_coin.append(app[1])
                        await asyncio.create_task(how_many_coins(app_name=app[1]))                            

                # - Reset trigger to call functions from schedule
                if (len(bot_executions_refresh) == len(applications)) and trigger.set_refresh != False:
                    bot_executions_refresh.clear()
                    trigger.set_refresh = False
                if (len(bot_executions_work) == len(applications)) and trigger.set_work != False:
                    bot_executions_work.clear()
                    trigger.set_work = False
                if (len(bot_executions_coin) == len(applications)) and trigger.set_coin != False:
                    bot_executions_coin.clear()
                    trigger.set_coin = False
                if (len(bot_executions_reload) == len(applications)) and trigger.set_reload != False:
                    bot_executions_reload.clear()
                    bot_executions_work.clear()
                    bot_executions_coin.clear()
                    bot_executions_refresh.clear()
                    trigger.set_reload = False
                    trigger.set_coin = False
                    trigger.set_work = False
                    trigger.set_refresh = False                                        
        else:
            logger.error('No account/profile found in the config.yaml file or profile do not match with profile opened, please check and restart the bot. Exiting bot...')
            os._exit(0)

if __name__ == "__main__":
    try:                
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except Exception as e:
        print("Exception: " + str(e))
        exit()