# pip install undetected_chromedriver selenium pillow
#pip3 install --upgrade requests
# wget https://github.com/electron/electron/releases/download/v19.0.2/chromedriver-v19.0.2-lin                                                                                                                ux-arm64.zip



import random
import time
import json
import requests
import sys
import re
import os
from PIL import Image
from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from urllib.parse import urlparse
import undetected_chromedriver as uc



uid=os.environ['UID']
apikey=os.environ['API_KEY']
BASE_URL=os.environ['BASE_URL']
api_url = BASE_URL+'solve'
fb_url = BASE_URL+'feedback'

total_task = 50
enable_time_limit=True
banch_mark=True

if banch_mark:
    print("Sending file upload enabled. will take 2s for every request.")

start_ts = time.time()
tt = random.uniform(13, 25)
end_ts = start_ts + int(tt*60)
order_id=""

total_t = []
s_time = time.time()

total_request_to_api=0
total_response_received=0
total_solved=0
total_error=0
total_skip=0
time_took=0.0
total_failed=0
failed_list=[]
skip_list=[]
error_list=[]


sites = ['https://shimuldn.github.io/hcaptcha/', 'https://shimuldn.github.io/hcaptcha/2',
         'https://shimuldn.github.io/hcaptcha/3', 'https://shimuldn.github.io/hcaptcha/4',
         'https://shimuldn.github.io/hcaptcha/5', 'https://shimuldn.github.io/hcaptcha/oracle',
         'https://shimuldn.github.io/hcaptcha/discord', 'https://shimuldn.github.io/hcaptcha/epic', ]
#    'https://signup.cloud.oracle.com/?sourceType=_ref_coc-asset-opcSignIn&language=en_US']


def main():
    try:
        options = webdriver.ChromeOptions()
        # options.binary_location = "C:\\Users\\ROG\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
        # options.binary_location = "C:\\Users\\ROG\\Documents\\Chromium-Portable-win64-codecs-sync-oracle\\bin\\chrome.exe"
        # options.binary_location="/usr/games/chromium-bsu"
        # options.add_argument("start-maximized")
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        options.add_argument('--lang=en_US')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        # driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path='/home/ubuntu/python/chromedriver')
        # print("Before driver")
        
        
        # print(driver)

        from sys import platform
        if platform.startswith("linux"):
            print("linux")
            options.add_argument('--headless')
            import platform
            if platform.processor().startswith("aarch"):
                driver = uc.Chrome(options=options, use_subprocess=True, driver_executable_path='/home/ubuntu/python/chromedriver')
            else:
                driver = uc.Chrome(options=options, use_subprocess=True)
        elif platform.startswith("darwin"):
            print("OSX")
        elif platform.startswith("win"):
            print("win")
            driver = uc.Chrome(options=options, use_subprocess=True)
            # options.add_argument('--headless')
        else:
            driver = uc.Chrome(options=options, use_subprocess=True)
        driver.set_window_size(300, 610)

        def face_the_checkbox():
            # print("face_the_checkbox")
            try:
                WebDriverWait(driver, 8, ignored_exceptions=WebDriverException).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//iframe[contains(@title,'checkbox')]"))
                )
                return True
            except TimeoutException:
                return False

        def get_site_key():
            for i in range(10):
                try:
                    obj = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@class='h-captcha']"))
                    )
                    key = obj.get_attribute("data-sitekey")
                    return key
                except:
                    time.sleep(0.03)
                    pass

        def handle_checkbox():
            for i in range(3):
                check_time_limit(driver)
                try:
                    time.sleep(1)

                    try:
                        WebDriverWait(driver, 2, ignored_exceptions=ElementNotVisibleException).until(
                            EC.frame_to_be_available_and_switch_to_it(
                                (By.XPATH, "//iframe[contains(@title,'checkbox')]")
                            )
                        )
                    except:
                        # print("frame to switch")
                        pass

                    try:
                        WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.ID, "checkbox"))).click()
                    except:
                        # print("click on the checkbox")
                        pass
                    try:
                        driver.switch_to.default_content()
                    except:
                        # print("Switching back")
                        pass

                    try:
                        HOOK_CHALLENGE = "//iframe[contains(@title,'content')]"
                        WebDriverWait(driver, 15, ignored_exceptions=ElementNotVisibleException).until(
                            EC.frame_to_be_available_and_switch_to_it(
                                (By.XPATH, HOOK_CHALLENGE))
                        )
                    except:
                        # print("hook")
                        pass

                    time.sleep(1)
                    try:
                        tg = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//h2[@class='prompt-text']"))
                        )
                        # print(f"Target from the try block {tg.text}")
                        return True
                    except:
                        # print("not able to find text")
                        pass
                except Exception as _e:
                    # print(f"Error on checkbox clicking.")
                    pass
            print("refreshing and checkbox again")
            driver.navigate().refresh()
            handle_checkbox()

        def get_target():
            for i in range(3):
                try:
                    tg = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//h2[@class='prompt-text']"))
                    )
                    return tg.text
                except Exception as _e:
                    # print("Error on get_terget")
                    pass
            return False

        def get_data_for_api():
            try:
                for i in range(5):
                    # print("get_data_for_api")
                    try:
                        # print("getting images data")
                        WebDriverWait(driver, 10, ignored_exceptions=ElementNotVisibleException).until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, "//div[@class='task-image']"))
                        )
                        images_div = driver.find_elements(
                            By.XPATH, "//div[@class='task-image']")
                        image_data = {}

                        # Getting the data for api server format
                        if len(images_div) == 9:
                            for item in images_div:
                                name = item.get_attribute("aria-label")
                                number = int(name.replace(
                                    "Challenge Image ", ""))-1
                                image_style = item.find_element(
                                    By.CLASS_NAME, "image").get_attribute("style")
                                url = re.split(r'[(")]', image_style)[2]
                                image_data[number] = url
                            # print(image_data)
                            return image_data
                        else:
                            # print("images len not 9")
                            pass
                    except Exception as _e:
                        # print(f"{_e} exception on get_data_for_api")
                        time.sleep(1)
            except:pass

        def do_the_magic(site_key, target):
            check_time_limit(driver)
            try:
                # print("do_the_magic")
                # site_key=get_site_key()

                images = get_data_for_api()
                target = get_target()
                site = urlparse(driver.current_url).netloc

                required_data = {}
                required_data['target'] = target
                required_data['data_type'] = 'url'
                required_data['site_key'] = site_key
                required_data['site'] = site
                required_data['images'] = images
                order_ta = []
                order_t0 = time.time()

                global total_request_to_api, total_error, time_took, total_skip, order_id
                total_request_to_api=total_request_to_api+1

                r = requests.post(url=api_url, headers={'Content-Type': 'application/json',
                                                        'uid': uid, 'apikey': apikey}, data=json.dumps(required_data))
                # print(r.status_code, r.json()["id"])
                if r.json()["status"] == "new":
                    order_id=str(r.json()["id"])
                    images_div = driver.find_elements(
                        By.XPATH, "//div[@class='task-image']")
                    time.sleep(2)
                    for i in range(15):
                        st_res = requests.get(r.json()["url"])


                        # print(st_res.json()['status'])
                        if st_res.json()['status'] == "solved":
                            tg = re.split(r"containing a", target)[-1][1:].strip()
                            order_ta.append(time.time() - order_t0)

                            time_took+=(time.time() - order_t0)

                            print(f"API solved {round(sum(order_ta), 2)}seconds for target {tg} ID {order_id} Time passed {calculate_total_time_passed()}m. Task done {total_request_to_api}")
                            order_ta = []


                            for item in images_div:
                                nn = int(item.get_attribute(
                                    "aria-label").replace("Challenge Image ", ""))-1
                                if nn in st_res.json()['solution']:

                                    time.sleep(random.uniform(0.1, 0.5))
                                    item.click()
                            # print("clicking done")
                            break
                        elif st_res.json()['status'] == "in queue":
                            time.sleep(1)
                        elif st_res.json()['status'] == "error":
                            total_error+=1

                            print(f"API not able to solve this one. Clicking refresh target {target}")
                            WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, "//div[@class='refresh button']"))
                            ).click()

                            time.sleep(2)
                            do_the_magic(site_key, target)
                        else:
                            print(f"{st_res.json()['status']} unknown error")
                            break

                elif r.json()["status"] == "skip":
                    order_id=""
                    print("API not able to solve this issue. Requested skip")
                    total_skip+=1
                    print(f"API not able to solve this one. Clicking refresh target {target}")
                    WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@class='refresh button']"))
                    ).click()

                    time.sleep(2)
                    print("After refresh",get_target())
                    do_the_magic(site_key, target)
                else:
                    order_id=""
                    print("Unknown error with the request")

                def get_button_name(driver):
                    try:
                        button = WebDriverWait(driver, 1, 0.1).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, "//div[@class='button-submit button']"))
                        )
                        return button.text
                    except Exception as _e:
                        return False

                def click_submit(driver):
                    cwd = os.getcwd()
                    order_id=str(r.json()["id"])
                    newpath = os.path.join(cwd, "images")
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    # os.makedirs(os.path.dirname(newpath), exist_ok=True)
                    rnd='img'+str(int(random.uniform(10, 20)))
                    final_path=os.path.join(newpath, order_id + '.png')
                    # driver.save_screenshot(final_path)
                    driver.get_screenshot_as_file(final_path)
                                    
                    img = Image.open(final_path)
                    img = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
                    img.save(final_path, optimize=True)

                    #### Uploading to imageDB ##################################################################
                    if banch_mark == True:
                        try:
                            tt0=time.time()
                            tta=[]
                            # print("Sending upload... report by banchmark tool")
                            url = f'{BASE_URL}upload?id={order_id}'
                            files = {'media': open(final_path, 'rb')}
                            requests.post(url, files=files)
                            tta.append(time.time() - tt0)
                            # print(f"Time took to send upload {round(sum(tta), 2)}seconds")
                        except Exception as _e:
                            print(f"Error in uploading image {_e}")


                    WebDriverWait(driver, 35, ignored_exceptions=ElementClickInterceptedException).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@class='button-submit button']"))
                    ).click()

                def check_if_solved(driver):
                    global total_failed, order_id
                    if order_id != "":
                        # print("check_if_solved")
                        try:
                            error_txt = WebDriverWait(driver, 1, 0.1).until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, "//div[@class='error-text']"))
                            )
                            tg = re.split(r"containing a", target)[-1][1:].strip()
                            print(
                                f'error found {error_txt.text} order ID {r.json()["id"]} target {tg} . Sending feedback to api')

                            if error_txt.text == "Please try again.":
                                # Sending feedback to api
                                if banch_mark==True:
                                    total_failed+=1
                                    print(f"From banchmark tool sending feedback of failed target {tg} order id {order_id}")
                                else:
                                    print(f"Sending feedback of failed target {tg} order id {order_id}")
                                try:
                                    fb = {"id": r.json()['id'], "feedback": "False"}
                                    requests.post(url=fb_url, headers={'Content-Type': 'application/json',
                                                                    'uid': uid, 'apikey': apikey}, data=json.dumps(fb))
                                except:
                                    pass
                            

                            ##### If there is error in solving. Solve the new one. ##################
                            time.sleep(1)
                            do_the_magic(site_key, target)
                        except:
                            pass

                        try:
                            tg = WebDriverWait(driver, 5, ignored_exceptions=ElementNotVisibleException).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//h2[@class='prompt-text']"))
                            )
                            # print(tg.text)
                            do_the_magic(site_key, target)
                        except:
                            tg = re.split(r"containing a", target)[-1][1:].strip()
                            # order_id=str(r.json()["id"])



                if get_button_name(driver) == "Verify":
                    time.sleep(1)
                    click_submit(driver)
                    # print("clicking submit")
                    time.sleep(1)
                    check_if_solved(driver)
                elif get_button_name(driver) == "Next":
                    # print("There is more")
                    time.sleep(1)
                    # print("clicking submit on NEXT")
                    click_submit(driver)
                    time.sleep(0.3)
                    check_if_solved(driver)
                else:
                    # print("btn name not verify")
                    time.sleep(0.3)
                    check_if_solved(driver)
            except Exception as _e:
                print(f"Exception on do the magic {_e}")



        for i in range(total_task):
            try:
                # print(f"Starting {i}")
                driver.get(random.choice(sites))

                if not face_the_checkbox:
                    break
                site_key = get_site_key()
                handle_checkbox()
                if get_target() != False:
                    target = get_target()
                    do_the_magic(site_key, target)


                check_time_limit(driver)
            except:pass


        # Close the browser

        total_t.append(time.time() - s_time)
        # print(f"{total_task} done in {(round(sum(total_t), 2))/60}m. Closing browser.")
        driver.close()

    except Exception as _e:
        if int(time.time()) < end_ts:
            print("time not done yet. Calling from exception")
            main()
        else:
            print("Error closing browser.")
        # driver.close()

def check_time_limit(driver):
    if enable_time_limit:
        if int(time.time()) > end_ts:
            global total_request_to_api
            total_task = 1
            print("Timeout closing the browser but requesting one more")
            do_another_api_call()
            driver.close()
            
def do_another_api_call():
    try:
        r = requests.post(os.environ['DISPATCHE_URL'],
            headers={'Authorization' : 'token ' +  os.environ['G_AUTH']},
            data=json.dumps({"event_type": str(int(time.time()))}))
        print(r)
    except:
        pass

def calculate_total_time_passed():
    tt=[]
    tt.append(time.time() - s_time)
    # print(f"{total_task} done in {(round(sum(total_t), 2))/60}m
    return (round(sum(tt)/60, 2))

main()

# while True:
#     import time
#     time.sleep(1)
