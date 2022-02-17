import datetime
import pyautogui
import os
import pathlib
import asyncio
import numpy as np
from random import randint
from controllers import setup_logger, take_screenshot, read_configurations, send_telegram_pic

try:
    streamConfig = read_configurations()
    work_ships_options = streamConfig['game_options']['work_ships_options']
    enable_login_metamask = streamConfig['bot_options']['metamask_options']['enable_login_metamask']
    metamask_password = streamConfig['bot_options']['metamask_options']['metamask_password']
    telegram_integration = streamConfig['telegram_options']['telegram_integration']
    clicks = streamConfig['game_options']['clicks_count']
    drag = streamConfig['game_options']['drag_count']
except FileNotFoundError:
    print('Error: config.yaml file not found, make sure config.yaml are placed in the folder..')
    exit()

async def connect_wallet(app_name=''):
    '''
    Function to connect into wallet, it's the first step of the bot.
    '''    

    await asyncio.sleep(np.random.uniform(2.5,3.5))

    logger = setup_logger()
    logger.info('Checking if needs to connect wallet..')
    
    ConnectWalletBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'connect-wallet-btn.png')
    if pyautogui.locateOnScreen(ConnectWalletBtnImg, grayscale=True, confidence=0.8) != None:
        # The connect button is visible        
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(pyautogui.locateOnScreen(ConnectWalletBtnImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on connect button
        pyautogui.click()
        logger = setup_logger(telegram_integration=True, bot_name=app_name)
        logger.info('Connect wallet button clicked..')
        await asyncio.sleep(np.random.uniform(0.8,1.5))
        return

async def open_metamask(app_name=''):
    '''
    Function to open Metamask only.
    '''

    await asyncio.sleep(np.random.uniform(1.5,2.5))
    # Move to a point where it can be clicked without a problem in order to make the Metamask screen disapear 
    pyautogui.moveTo(930, 328, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
    # Click on Metamask icon
    pyautogui.click()    

    image_list = ['metamask-icon-notification-btn.png', 'metamask-icon-notification-btn2.png']
    for metamaskimg in image_list:
        MetamaskBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', metamaskimg)
        if pyautogui.locateOnScreen(MetamaskBtnImg, grayscale=True, confidence=0.8) != None:        
            # Move mouse in a random place first
            move_mouse_random()
            # Move to location
            pyautogui.moveTo(pyautogui.locateOnScreen(MetamaskBtnImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
            # Click on Metamask icon
            pyautogui.click()
            logger = setup_logger(telegram_integration=True, bot_name=app_name)
            logger.info('Metamask icon clicked..')
            await asyncio.sleep(np.random.uniform(0.5,1))
            return

async def unlock_metamask(app_name=''):
    '''
    Function to only unlock Metamask.
    The options comes from the yaml file.
    '''

    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    image_list = ['unlock-btn.png', 'desbloquear-btn.png', 'unlock-btn2.png']
    for unlock_image in image_list:
        UnlockBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', unlock_image)
        # The unlock button is visible
        if pyautogui.locateOnScreen(UnlockBtnImg, confidence=0.8) != None:
            if enable_login_metamask != False:
                image_list = ['password-tittle.png', 'password-tittle2.png', 'senha-title.png', 'senha-title2.png']                
                for password_img in image_list:
                    PasswordImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', password_img)
                    if pyautogui.locateOnScreen(PasswordImg, confidence=0.8) != None:
                        await asyncio.sleep(np.random.uniform(0.8,1.5))
                        # Move mouse in a random place first
                        move_mouse_random()
                        # Move to location
                        pyautogui.moveTo(pyautogui.locateOnScreen(PasswordImg, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                        # Click on password field
                        pyautogui.click()
                        # Write password to unlock Metamask
                        pyautogui.write(metamask_password, interval=0.05)
                        # Move to location
                        pyautogui.moveTo(pyautogui.locateOnScreen(UnlockBtnImg, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                        # Click on unlock button
                        pyautogui.click()
                        await asyncio.sleep(np.random.uniform(1.5,2.5))
                        IncorrectPasswordImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'incorrect-password.png')
                        if pyautogui.locateOnScreen(IncorrectPasswordImg, confidence=0.8) != None:
                            logger.error('Password is wrong, remeber to change on the "metamask_password" option from .yaml file! Exiting bot because it cannot unlock Metamask with the given password..')
                            exit()
                        image_list = ['connected-title.png', 'conectado-title.png']
                        for connectImg in image_list:
                            ConnectImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', connectImg)
                            if pyautogui.locateOnScreen(ConnectImg, confidence=0.8) != None:
                                logger.info('Password correct, Metamask unlocked succesfully!')
                                # Open Metamask icon
                                await asyncio.create_task(open_metamask())
                                return                            
            elif enable_login_metamask != True:
                logger.warning('The "enable_login_metamask" option is set to False, so it is not possible to unlock Metamask automatically, unless you change the option to True. Unlock Metamask manually first! Exiting bot..')
                exit()

async def signin_metamask(app_name=''):
    '''
    Function to sign in into Metamask.    
    ''' 
    
    image_list = ['assinar-btn.png', 'sign-btn.png']
    for sign_image in image_list:
        SignBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', sign_image)
        # The sign button is visible
        if pyautogui.locateOnScreen(SignBtnImg, confidence=0.8) != None:
            await asyncio.sleep(np.random.uniform(0.4,0.8))
            # Move mouse in a random place first
            move_mouse_random()
            # Move to location
            pyautogui.moveTo(pyautogui.locateOnScreen(SignBtnImg, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
            # Click on sign button            
            pyautogui.click()
            logger = setup_logger(telegram_integration=True,bot_name=app_name)
            logger.info('Metamask signed..')
            # Close Metamask window
            pyautogui.hotkey('esc')
            await asyncio.sleep(np.random.uniform(3,4))
            return                

async def login_metamask(app_name=''):
    '''
    Function to login into Metamask, it requires to open the Metamask icon and then signin or unlock Metamask account.
    '''

    logger = setup_logger()
    logger.info('Checking if need to login in Metamask..')

    # Open Metamask icon
    await asyncio.create_task(open_metamask(app_name=app_name))
    # Unlock Metamask
    await asyncio.create_task(unlock_metamask(app_name=app_name))
    # Sign Metamask
    await asyncio.create_task(signin_metamask(app_name=app_name))
    return

async def first_start(app_name=''):
    
    await asyncio.sleep(np.random.uniform(3.5,5.5))

    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    logger.info('First start function..')

    # Check some routines before refresh the page

    # Check if confirm button is available
    await asyncio.create_task(confirm_button(app_name=app_name))

    # Check if is it possible to send heroes to work available at screen
    await asyncio.create_task(how_many_coins(app_name=app_name))

    # Check if needs to send ships to fight
    await asyncio.create_task(continue_fighting(app_name=app_name))

    # Check if needs to send ships to fight
    await asyncio.create_task(send_ships_to_fight(app_name=app_name))

    # Refresh page if game is not already logged
    GameImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'game-screen.png')
    if pyautogui.locateOnScreen(GameImg, grayscale=True, confidence=0.8) != None:
        await asyncio.create_task(reload_page(app_name=app_name))

    logger.info('Exiting start function..')

async def play_game(app_name=''):
    '''
    Function to play the game.
    '''    

    logger = setup_logger()
    logger.info('Checking if needs to play game..')
    
    PlayBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'play-btn.png')
    if pyautogui.locateOnScreen(PlayBtnImg, grayscale=True, confidence=0.8) != None:
        # The connect button is visible        
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(pyautogui.locateOnScreen(PlayBtnImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on connect button
        pyautogui.click()
        logger = setup_logger(telegram_integration=True, bot_name=app_name)
        logger.info('Play game button clicked..')
        await asyncio.sleep(np.random.uniform(8,10))
        # Check if treasure hunt mode is already available at screen
        await asyncio.create_task(send_ships_to_fight(app_name=app_name))
        return

async def start_game(app_name=''):
    '''
    Function to start the game from connect wallet e playing the game.
    '''  

    # Check if connect wallet is already available at screen
    await asyncio.create_task(connect_wallet(app_name=app_name))

    # Check if play game button is already available at screen
    await asyncio.create_task(play_game(app_name=app_name))

async def fight_boss(app_name=''):
    
    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    FightBossImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fightboss-btn.png')

    # Send them to fight by click on the button 'Fight Boss'
    if pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8) != None:
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location
        pyautogui.moveTo(pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on Treasure Hunt game mode
        pyautogui.click()
        logger.info('Fight boss game mode clicked..')
        await asyncio.sleep(np.random.uniform(0.8,1.5))
        return

async def confirm_button(app_name=''):
    
    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    ConfirmImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'confirm-btn.png')

    # Click on 'Confirm' button if applicable because the boss might loss
    if pyautogui.locateOnScreen(ConfirmImgBtn, grayscale=True, confidence=0.8) != None:
        # Move to location
        pyautogui.moveTo(pyautogui.locateOnScreen(ConfirmImgBtn, grayscale=True, confidence=0.8), None, np.random.uniform(0.2,0.4), pyautogui.easeInOutQuad)
        # Click on Treasure Hunt game mode
        pyautogui.click()
        logger.info('Confirm buttom clicked..')
        await asyncio.sleep(np.random.uniform(0.3,0.6))
        return

async def remove_ships_from_fight(app_name=''):

    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    CloseImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'close-btn.png')
    FightBossImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fightboss-btn.png')

    remove_flag = False

    # Check if button is already available at screen
    await asyncio.create_task(confirm_button(app_name=app_name))
    # Check if button is already available at screen
    await asyncio.create_task(go_to_ships(app_name=app_name))
    # Send them to fight by click on the button 'Fight Boss'
    if pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8) != None:   
        # Move mouse in a random place first
        move_mouse_random()
        while True:
            if pyautogui.locateOnScreen(CloseImgBtn, confidence=0.8) != None:
                # Move to location               
                pyautogui.moveTo(pyautogui.locateOnScreen(CloseImgBtn, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)                
                pyautogui.click()
                remove_flag = True
            else:
                break
                
    if remove_flag != False:
        logger.info('Ships were removed from fight!')

async def send_ships_to_fight(app_name=''):    

    logger = setup_logger(telegram_integration=False, bot_name=app_name)
    logger.info('[Work] Calling send ships to fight function..')
    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    FightFullImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fightfull-btn.png')
    FightImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fight-btn.png')
    FightBossImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fightboss-btn.png')
    FullShipsImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fullships.png')

    # Check if button is already available at screen
    await asyncio.create_task(confirm_button(app_name=app_name))

    # Call function
    await asyncio.create_task(remove_ships_from_fight(app_name=app_name))

    if work_ships_options == 'full':
        clicks_count = 0
        drag_count = 0
        # Send them to fight by click on the button 'Fight Boss'
        if pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8) != None:
            # Choose ships first
            while True:
                buttons = list(pyautogui.locateAllOnScreen(FightFullImgBtn, confidence=0.99))
                if pyautogui.locateOnScreen(FullShipsImg, grayscale=True, confidence=0.95) != None:
                    break
                elif clicks_count > clicks:
                    break
                elif drag_count > drag:
                    break
                
                if len(buttons) > 0:
                    for position in buttons:
                        if pyautogui.locateOnScreen(FightFullImgBtn, grayscale=True, confidence=0.8) != None:
                            pyautogui.moveTo(position, None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                            pyautogui.click()
                            clicks_count += 1
                else:
                    if pyautogui.locateOnScreen(FightFullImgBtn, grayscale=True, confidence=0.8) != None:
                        pyautogui.moveTo(pyautogui.locateOnScreen(FightFullImgBtn, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                        pyautogui.dragRel(0, -200, duration=1, button='left')
                        #pyautogui.scroll(-60)
                        await asyncio.sleep(np.random.uniform(3.8,4))
                        drag_count += 1
            
            if clicks_count > 0:
                logger.info('Ships were sending to fight!')
                
            # Check if fight boss button is already available at screen
            await asyncio.create_task(fight_boss(app_name=app_name))

            # Check if play game button is already available at screen
            await asyncio.create_task(confirm_button(app_name=app_name))

            await asyncio.sleep(np.random.uniform(1.8,2.8))
            # Take screenshot
            path_file = take_screenshot('screenshot', 'report', 'fight_boss')
            if telegram_integration != False:
                # Send picture to Telegram
                send_telegram_pic(path_file)
    elif work_ships_options == 'all':
        clicks_count = 0
        drag_count = 0
        # Send them to fight by click on the button 'Fight Boss'
        if pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8) != None:
            # Choose ships first
            while True:
                buttons = list(pyautogui.locateAllOnScreen(FightImgBtn, confidence=0.99))
                if pyautogui.locateOnScreen(FullShipsImg, grayscale=True, confidence=0.95) != None:
                    break
                elif clicks_count > clicks:
                    break
                elif drag_count > drag:
                    break

                if len(buttons) > 0:
                    for position in buttons:
                        if pyautogui.locateOnScreen(FightImgBtn, grayscale=True, confidence=0.8) != None:
                            pyautogui.moveTo(position, None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                            pyautogui.click()
                            clicks_count += 1
                else:
                    if pyautogui.locateOnScreen(FightImgBtn, grayscale=True, confidence=0.8) != None:
                        pyautogui.moveTo(pyautogui.locateOnScreen(FightImgBtn, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
                        pyautogui.dragRel(0, -200, duration=1, button='left')
                        #pyautogui.scroll(-60)
                        await asyncio.sleep(np.random.uniform(3.8,4))
                        drag_count += 1
            
            if clicks_count > 0:
                logger.info('Ships were sending to fight!')
                
            # Check if fight boss button is already available at screen
            await asyncio.create_task(fight_boss(app_name=app_name))

            # Check if play game button is already available at screen
            await asyncio.create_task(confirm_button(app_name=app_name))

            await asyncio.sleep(np.random.uniform(1.8,2.8))
            # Take screenshot
            path_file = take_screenshot('screenshot', 'report', 'fight_boss')
            if telegram_integration != False:
                # Send picture to Telegram
                send_telegram_pic(path_file)                   

async def continue_fighting(app_name=''):
    '''
    Function to continuing fighting the boss in the game, because the ships ammo might be empty.
    '''

    logger = setup_logger(telegram_integration=False, bot_name=app_name)
    logger.info('Checking if needs to send ships to fight again..')
    ZeroAmmoImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'zero-ships.png')    

    if pyautogui.locateOnScreen(ZeroAmmoImgBtn, grayscale=True, confidence=0.8) != None:
        # Send ships to fight again
        await asyncio.create_task(send_ships_to_fight(app_name=app_name))        

async def refresh_game(app_name=''):
    '''
    Function to refresh the game, so the game it's not disconnected.
    '''

    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    logger.info('[Refresh] Calling refresh heroes position function..')
    FightBossImgBtn = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'fightboss-btn.png')    

    if pyautogui.locateOnScreen(FightBossImgBtn, grayscale=True, confidence=0.8) != None:        
        # Go to base menu
        await asyncio.create_task(go_to_base(app_name=app_name))
        # Go to spaceship menu
        await asyncio.create_task(go_to_ships(app_name=app_name))
        return

async def new_map(app_name=''):
    '''
    Function to check for a new map available    
    '''
    logger = setup_logger(telegram_integration=False, bot_name=app_name)
    logger.info('Checking if is there any new map..')   

    NewMapImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'victory-screen.png')
    if pyautogui.locateOnScreen(NewMapImg, grayscale=True, confidence=0.8) != None:
        path_file = take_screenshot('screenshot', 'new_map', 'antes')
        if telegram_integration != False:
            # Send picture to Telegram
            send_telegram_pic(path_file)
        await asyncio.create_task(confirm_button(app_name=app_name))
        await asyncio.sleep(np.random.uniform(0.8,1.5))
        take_screenshot('screenshot', 'new_map', 'depois')
        return

async def go_to_base(app_name=''):
    '''
    Function to recognize the image of ships from menu and go to the ships menu.
    From this we can select ships to battle.
    '''

    BaseBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'base-btn.png')
    logger = setup_logger(telegram_integration=True,bot_name=app_name)
    if pyautogui.locateOnScreen(BaseBtnImg, grayscale=True, confidence=0.8) != None:
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(pyautogui.locateOnScreen(BaseBtnImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on Treasure Hunt game mode
        pyautogui.click()
        logger.info('Going to base menu..')
        await asyncio.sleep(np.random.uniform(0.8,1.5))
        return

async def go_to_ships(app_name=''):
    '''
    Function to recognize the image of ships from menu and go to the ships menu.
    From this we can select ships to battle.
    '''

    ShipsImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'ships-btn.png')
    logger = setup_logger(telegram_integration=True,bot_name=app_name)
    if pyautogui.locateOnScreen(ShipsImg, grayscale=True, confidence=0.8) != None:
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(pyautogui.locateOnScreen(ShipsImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on Treasure Hunt game mode
        pyautogui.click()
        await asyncio.sleep(np.random.uniform(0.5,1.5))
        logger.info('Going to ships menu..')
        await asyncio.sleep(np.random.uniform(2.5,3.5))
        return

async def close_button(app_name=''):
    '''
    Function to recognize the close button image.
    '''

    logger = setup_logger()
    logger.info('Checking if needs to close any screen open..')

    CloseBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'close-btn.png')
    if pyautogui.locateOnScreen(CloseBtnImg, grayscale=True, confidence=0.8) != None:    
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(pyautogui.locateOnScreen(CloseBtnImg, grayscale=True, confidence=0.8), None, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)    
        # Click on close
        pyautogui.click()        
        logger = setup_logger(telegram_integration=True,bot_name=app_name)
        logger.info('Close button clicked..')
        await asyncio.sleep(np.random.uniform(0.3,0.9))
        return

async def skip_error_on_game(app_name=''):
    '''
    Function to skip any error on game that might occur.
    It's looking only to an error message, but in case more error appears with different images, we need to add them here.
    '''

    logger = setup_logger()
    logger.info('Checking if game has any erros or crash..')

    ErrorTittleImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'error-tittle.png')
    BrowserErrorBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'browser-error.png')
    logger = setup_logger(telegram_integration=True,bot_name=app_name)

    await asyncio.create_task(confirm_button(app_name=app_name))

    if pyautogui.locateOnScreen(ErrorTittleImg, grayscale=True, confidence=0.8) != None:
        # Take screenshot of the error
        path_file = take_screenshot('screenshot', 'errors')
        if telegram_integration != False:
            # Send picture to Telegram
            send_telegram_pic(path_file)        
        await asyncio.sleep(np.random.uniform(0.8,1.5))
        logger.warning('Error on game, check screenshot image to find it..')
        # Start game again
        await asyncio.create_task(reload_page(app_name=app_name))
        return
        
async def shoot_boss(app_name=''):
    '''
    Function to shoot boss automatically
    '''

    logger = setup_logger()
    logger.info('Checking if needs to close any screen open..')

    CloseBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'close-btn.png')
    while pyautogui.locateOnScreen(CloseBtnImg, grayscale=True, confidence=0.8) != None:    
        # Move mouse in a random place first
        move_mouse_random()
        # Move to location               
        pyautogui.moveTo(100, 200, np.random.uniform(0.4,0.9), pyautogui.easeInOutQuad)
        # Click on close
        pyautogui.click()
        return

async def how_many_coins(app_name=''):
    '''
    Function to send screenshot to telegram of how many coins the player has.
    '''
    
    ClaimBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'claim-btn.png')
    SurrenderBtnImg = os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), 'static', 'img', 'game', 'surreder-btn.png')
    logger = setup_logger(telegram_integration=True,bot_name=app_name)
    if pyautogui.locateOnScreen(SurrenderBtnImg, grayscale=True, confidence=0.8) != None:
        await asyncio.create_task(go_to_ships(app_name=app_name))
        await asyncio.sleep(np.random.uniform(1.8,2.8))
        # Take screenshot
        path_file = take_screenshot('screenshot', 'report', 'coins')        
        if telegram_integration != False:
            # Send picture to Telegram
            send_telegram_pic(path_file)
        logger.info('Screenshot took from coins, you can check how many coins you have!')
        await asyncio.create_task(fight_boss(app_name=app_name))
        return
    elif pyautogui.locateOnScreen(ClaimBtnImg, grayscale=True, confidence=0.8) != None:
        await asyncio.sleep(np.random.uniform(1.8,2.8))
        # Take screenshot
        path_file = take_screenshot('screenshot', 'report', 'coins')        
        if telegram_integration != False:
            # Send picture to Telegram
            send_telegram_pic(path_file)
        logger.info('Screenshot took from coins, you can check how many coins you have!')
        return        

def move_mouse_random():
    '''
    Function to move mouse in a random place.
    '''

    # Get the size of the screen
    screen_width , screen_height = pyautogui.size()

    x = randint(0, screen_width - 1)
    y = randint(0, screen_height -1)
 
    #print("Moving to ({},{})".format(x,y))
    pyautogui.moveTo(x,y, duration=0.50)

async def reload_page(app_name=''):
    '''
    Function to reload the page by the keys CTRL + F5.
    '''

    # Reload page
    logger = setup_logger(telegram_integration=True, bot_name=app_name)
    logger.warning('[Reload] Reloading the page in order to clear any error if exist..')
    pyautogui.hotkey('ctrl','shift', 'r')
    await asyncio.sleep(np.random.uniform(25,30))
    return

class SetTrigger(object):
    def __init__(self):
        self.set_work = False
        self.set_reload = False
        self.set_refresh = False
        self.set_coin = False
    
    def UpdateSetRefresh(self):
        self.set_refresh = True
        return self.set_refresh

    def UpdateSetWork(self):
        self.set_work = True
        return self.set_work

    def UpdateSetReload(self):
        self.set_reload = True
        return self.set_reload
    
    def UpdateSetCoin(self):
        self.set_coin = True
        return self.set_coin
