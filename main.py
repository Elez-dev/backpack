from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import threading
import random
import string

# option
option = webdriver.ChromeOptions()
option.add_extension("jopa.crx")
option.add_argument(f'--user-agent={UserAgent().random}')
option.add_argument('--disable-gpu')
option.page_load_strategy = 'eager'
option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
option.add_argument("--disable-blink-features=AutomationControlled")

# ref code
ref_code = 'https://backpack.app/ref/elezdev'

# invite code
invite_code = "a6a99b56-3428-419b-9516-29db82897a8a"

# number of threads
number_of_threads = 5

lock = threading.Lock()

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def follow(driver):
    driver.get(ref_code)
    time.sleep(1)
    password = 'qwerqwer'
    driver.get('chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/options.html?onboarding=true')
    time.sleep(4)
    driver.find_element(by=By.NAME, value="inviteCode").send_keys(invite_code)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Go']").click()
    time.sleep(1)
    driver.find_element(by=By.NAME, value="username").send_keys(generate_random_string(10))
    driver.find_element(by=By.XPATH, value="//*[text() = 'Continue']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Create a new wallet']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Create with recovery phrase']").click()
    time.sleep(1)
    name = ''
    for i in range(2, 10):
        name += driver.find_element(by=By.ID, value=f":r{i}:").get_attribute('value')
        name += ' '
    for i in ['a', 'b', 'c', 'd']:
        name += driver.find_element(by=By.ID, value=f":r{i}:").get_attribute('value')
        name += ' '
    lock.acquire()
    with open('seed.txt','a') as f:
        f.write(name + '\n')
    lock.release()
    driver.find_element(by=By.XPATH, value="//*[text() = 'I saved my secret recovery phrase']").click()
    driver.find_element(by=By.XPATH, value="//*[text() = 'Next']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Ethereum']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Solana']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Next']").click()
    time.sleep(1)
    driver.find_element(by=By.NAME, value="password").send_keys(password)
    driver.find_element(by=By.NAME, value="password-confirmation").send_keys(password)
    driver.find_element(by=By.XPATH, value="//*[text() = 'terms of service']").click()
    time.sleep(1)
    driver.switch_to.window((driver.window_handles[1]))
    driver.close()
    time.sleep(1)
    driver.switch_to.window((driver.window_handles[0]))
    driver.find_element(by=By.XPATH, value="//*[text() = 'Next']").click()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value="//*[text() = 'Disable']").click()
    time.sleep(1)


def main():
    while True:
        driver = webdriver.Chrome(options=option)
        try:
            follow(driver)
        except Exception:
            print(f'Ошибка ')
        finally:
            driver.close()
            driver.quit()


if __name__ == '__main__':
    for _ in range(number_of_threads):
        threading.Thread(target=main).start()

