from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import requests

import os
import shutil
import time
import sys

################################################################################
def python_version_check():
    print()
    try:
        assert sys.version_info >= (3, 7)
        print('[INFO]: Your Python version >= 3.7 | SUCCESS.')
    except:
        print('[INFO]: Python version lower than 3.7 thus script may crash in runtime | FAIL.')
    print()

################################################################################
def get_flag_value(flag):
    '''flag e.g. --name'''
    value = []
    args = sys.argv[1:]
    if flag in args:
        start = args.index(flag) + 1

        for arg in args[start:]:
            if '--' in arg:
                break
            value.append(arg)

        print(f'[INFO]: Flag {flag} retrieved as {" ".join(value)} | SUCCESS.')

        return ' '.join(value)
    else:
        print(f'[INFO]: Flag {flag} has no values provided | FAIL.')
        return False

################################################################################

def chrome_webdriver(run_headless, exec_path='chromedriver'):
    try:
        options = webdriver.ChromeOptions()
        # Run incognito
        options.add_argument('--incognito')
        # Run headless if needed
        if run_headless:
            options.add_argument('--headless')

        try:
            driver = webdriver.Chrome(options=options, executable_path=exec_path)
        except:
            print('!!!!! Chromedriver executable_path incorrect !!!!!')
            print(f'Make sure there is correct chromedriver on path: {exec_path}')
            print('!!!!! Chromedriver executable_path incorrect !!!!!')
            raise Exception('ChromeDriver')

        driver.set_window_position(0, 0)
        driver.set_window_size(800, 750)
        print('[INFO]: ChromeDriver initialized | SUCCESS.')

        return driver

    except:
        print('[ERROR]: ChromeDriver initializing | FAIL.')
        raise Exception('chrome_webdriver()')

################################################################################


###### GET IMAGE ANCHORS

def get_anchors(driver, search_term, amount):
    print()
    def get_anchors(search_term):
        return driver.find_elements_by_xpath('//img[@alt="Image result for ' + search_term + '"]/../..')

    anchors = get_anchors(search_term)

    print(f'[INFO]: Found {len(anchors)} images on page. You need {amount} | SUCCESS.\n')


    ####################
    scroll = 1
    while len(anchors) < amount:
        # Scroll down untill number of images satisfy
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        anchors = get_anchors(search_term)
        print(f'[INFO]: After {scroll} scroll/s there is {len(anchors)} images on page | SUCCESS.')

        if scroll > 10:
            print(f'[INFO]: Too many scrolls (up to 10 scrolls) | STOP.')
            break
        scroll += 1
    ####################
    print()
    return anchors


###### GET IMAGE SOURCES

def get_http_sources(driver, anchors, amount):

    sources = []

    for idx, anchor in enumerate(anchors):
        print(f'[INFO]: Anchor idx: {idx})  ', end=' ')

        # CLICK
        for i in range(3):
            try:
                anchor.click()
                time.sleep(2)
                break
            except:
                print(f'IDX: {idx} CANNOT BE CLICKED FOR THE {i+1} TIME.', end=' ')

        # IMAGES AFTER CLICK
        images = driver.find_elements_by_xpath('//img[@class="n3VNCb"]')
        if len(images) == 0:
          time.sleep(1)
          images = driver.find_elements_by_xpath('//img[@class="n3VNCb"]')

        #print(f'has {len(images)} related images')

        # MAKE SURE PAGE IS LOADED
        stop = 0
        complete = driver.execute_script('return document.readyState;').lower()
        while complete != 'complete':
            time.sleep(1)
            print('loading page...')
            stop += 1
            if stop >= 5:
                print('Timeout 5s...')
                break

        wait_for_images_loaded(driver=driver)

        # QUICK CHECK
        is_http = False
        print('Quick check', end=' ')

        for image in images:
            src = image.get_attribute('src')

            if 'http' in src[:10]:
                sources.append(src)
                is_http = True
                print('| SUCCESS.')
                break

        if not is_http:
            print('| FAIL (HTTP NOT FOUND).')

#         # LONG CHECK IF QUICK FAILED
#         if not is_http:
#             print('| FAIL')
#             print('\nLong check.', end='')

#             for image in images:
#                 src = image.get_attribute('src')

#                 stop = 0
#                 while 'http' not in src[:10]:
#                     print(f'.', end='')
#                     time.sleep(1)
#                     stop += 1

#                     src = image.get_attribute('src')

#                     if stop >= 10:
#                         print(' | FAIL (Timeout 10s...)')
#                         break


#                 if 'http' in src[:10]:
#                     print(f' |   SUCCESS')
#                     sources.append(src)
#                     #print(f'There is {len(sources)} SOURCES now.')
#                     is_http = True
#                     break

#         if not is_http:
#             print(f' |   FAIL (HTTP NOT FOUND)')

        if idx+1 >= amount:
            break


    print(f'\n[INFO]: Retrieved {len(sources)}/{amount} image sources from {len(anchors)} images on page | SUCCESS.')

    return sources

################################################################################

def prepare_file_system_structure(search_term):
    print()
    file_name = search_term.replace(' ', '_')
    if file_name in os.listdir():
        shutil.rmtree(file_name)
        print(f'[INFO]: "{file_name}" folder has been deleted | SUCCESS.')

    os.mkdir(file_name)
    print(f'[INFO]: New "{file_name}" empty folder has been created | SUCCESS.')

    curdir = os.path.abspath(os.curdir)
    print(f'[INFO]: I am on path: {curdir} | SUCCESS.')

    path = os.path.join(curdir, file_name)
    print(f'\n[INFO]: All images will be saved on path: {path} | SUCCESS.')

    return file_name, path

################################################################################

def save_sources(driver, sources, file_name, path):
    print()
    # Counter variable helps naming the files
    counter = 1
    invalid = 0

    for source in sources:

        # Save
        extension = '.png'
        full_file_name = str(counter).zfill(3) + file_name + extension


        try:
            r = requests.get(source, verify=True, timeout=10, headers={"User-Agent": "XY"})

            time.sleep(0.5)

            if r.status_code != 200:
                print(f'[INFO]: Status Code for provided url is incorect ({r.status_code}) | FAIL.')
                raise Exception('download()')

            with open(os.path.join(path, full_file_name), 'wb') as file:
                file.write(r.content)
            print(f'[INFO]: \tImage {str(counter).zfill(3)} uploaded as {full_file_name} | SUCCESS.')

        except:
            invalid += 1
            print(f'\n\
[Error]: Image {str(counter).zfill(3)} download failed ,\n\
[Error]: full name: {full_file_name} ,\n\
[Error]: source: {source} .\n')

        # Update name for the next file
        counter += 1

    print(f'\n[INFO]: Downloaded {counter-1-invalid} of {len(sources)} valid images on path: {path} | SUCCESS.')










def wait_for_images_loaded(driver):
    stop = 0
    while True:
        score = 0
        divs = driver.find_elements_by_xpath('//div[@class="k7O2sd"]')
        for div in divs:
            if div.get_attribute('style') == 'display: none;':
                score += 1

        if score == len(divs) or stop >= 30:
            if stop >= 15:
                print('TIMEOut 30s', end=' ')
            else:
                print('image loaded |', end=' ')
            time.sleep(1)
            break

        time.sleep(1)
        stop += 1
        if stop ==1:
            print('waiting for <display: none;>', end=' ')
        else:
            print('.', end='')



################################################################################
def main():
    print()
    print('='*57)
    print('='*57)
    print('google_image_downloader START')
    print('='*57)
    # Checks Python version
    python_version_check()

    # Determine if programm run headless (Chrome browser wont't appear)
    run_headless = False
    if '--headless' in sys.argv[1:]:
        run_headless = True

    # Determine term to search
    search_term = get_flag_value(flag='--search')
    if not search_term:
        print(f'[INFO]: Search term value error | FAIL.')
        raise Exception('Search term value incorrect.')

    # Determine amount of images to download
    try:
        amount = get_flag_value(flag='--amount')
        amount = int(amount)
    except:
        print(f'[INFO]: amount value error | FAIL.')
        raise Exception('Amount value incorrect.')

    try:
        assert amount in range(0, 500+1)
        assert search_term != 'chromedriver_folder'
    except:
        print('\n[INFO]: Amount has to be in range [0, 500] and search term cannot be "chromedriver_folder"! | FAIL.\n')
        return False

    print()
    print('='*57)
    print('| %26s | %8s | %13s |' % ('search_term', 'amount', 'run_headless'))
    print('-'*57)
    print('| %26s | %8s | %13s |' % (search_term, amount, run_headless))
    print('='*57)
    print()

    try:
        # ChromeDriver exec_path
        cur_dir = os.path.abspath(os.curdir)
        chromedriver_folder = 'chromedriver_folder'
        chromedriver_name = 'chromedriver'
        exec_path = os.path.join(cur_dir, chromedriver_folder, chromedriver_name)

        # Initilize driver (selenium object that manipulate chrome browser)
        driver = chrome_webdriver(exec_path=exec_path, run_headless=run_headless)

        # Create url from google image search pattern
        url = 'https://www.google.com/search?q=' + search_term.replace(' ', '+') + '&source=lnms&tbm=isch'

        # Go to webpage
        driver.get(url)

        # Make sure there is enough anchors on page with desired image source
        anchors = get_anchors(driver, search_term, amount)

        # Get image sources
        sources = get_http_sources(driver, anchors, amount)

        # Create folder to save (if one with the same name exists, delete it and create a new one)
        file_name, path = prepare_file_system_structure(search_term=search_term)

        # Save images inside created folder
        save_sources(driver=driver, sources=sources, file_name=file_name, path=path)
    finally:
        # Shut down driver session
        driver.quit()

        print()
        print('='*57)
        print('google_image_downloader STOP')
        print('='*57)
        print('='*57)
        print()

################################################################################

if __name__ == '__main__':
    main()

################################################################################
################################################################################
