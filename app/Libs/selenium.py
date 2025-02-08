import os
import time
import undetected_chromedriver          as uc
from selenium                           import webdriver
from selenium.webdriver.support.ui      import WebDriverWait
from selenium.webdriver.common.by       import By
from selenium.webdriver.support         import expected_conditions as EC
from selenium.webdriver.chrome.service  import Service
from selenium.webdriver.chrome.options  import Options
from selenium.common.exceptions         import TimeoutException



CAPABILITIES = {
    "browserName"     : "chrome",
    "browserVersion"  : "110.0",
    "name"            : "default",
    "enableVNC"  : True,
    "enableVideo": False
}

class SeleniumLib:
    driver = None

    # def __del__(self):
    #     if self.driver:
    #         self.close()

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def wait_loads(self, tm=5):
        wait = WebDriverWait(self.driver, 60)
        wt = lambda a: self.driver.execute_script("return document.readyState==\"complete\";")
        wait.until(wt)
        time.sleep(tm)

    def open_page(self,page):
        self.driver.get(page)
        self.driver.implicitly_wait(2)
        self.wait_loads()

        return self.driver

    def wait_xpath(self,path,time=20,throw=True):
        try:
            element = WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located((By.XPATH, path)))
            return element
        except:
            if throw: raise
            return None
        
    def close_popup(self, by, value):
        self.driver.switch_to.default_content()
        elements = self.driver.find_elements(by, value)
        if elements:
            element = elements[0]
            if element.is_displayed():
                element.click()

    def swithc_iframe(self, by, value):
        self.driver.switch_to.default_content()
        iframe = self.driver.find_element(by,value)
        self.driver.switch_to.frame(iframe)


    def delayed_send(self,element, word, delay):    
        for c in word:
            element.send_keys(c)
            time.sleep(delay)

    def SCROLL_END(self):
        get_pos = lambda:self.driver.execute_script("return document.documentElement.scrollTop")

        while True:
            atual_pos = get_pos()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            future_pos = get_pos()
            if  future_pos == atual_pos:
                break

    def wait_download(self,folder_path, timeout=60, check_interval=1, file_extension='.xlsx'):
        start_time = time.time()
        
        while True:
            files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]
            
            if len(files) == 1:
                file_path = os.path.join(folder_path, files[0])
                file_size = os.path.getsize(file_path)
                
                time.sleep(check_interval)
                new_file_size = os.path.getsize(file_path)
                
                if file_size == new_file_size and file_size > 0:
                    return file_path
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout:
                return None
            
            time.sleep(check_interval)

    def click_element(self, by, value, timeout=10):
        try:
            element =  WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
            element.click()
            return True
        except:
            return None
    
    def digit_element(self, by, value, word, timeout=10):
        while timeout > 0:
            try:
                element =  WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
                element.clear()
                element.send_keys(word)
                return True
            except TimeoutException:
                break
            except:
                timeout -=1
                continue
        
    def digit_shadow_root(self, script, texto, loop=25):

        retorno = False
        counter = 1
        while loop > 0:
            try:
                elemento = self.driver.execute_script(script)
                elemento.send_keys(texto)
                retorno = True
                loop = 0

            except Exception as error:
                time.sleep(counter)
            counter += 1
            loop -= 1
        if not retorno:
            return None
        return retorno
        
    def setupSelenium(self,host="",name="default",use_selenoid=False,cust_opt = []) -> webdriver:
        """Setup selenium driver"""
        opts = ["--disable-web-security","--verbose","--no-sandbox","disable-infobars","--disable-extensions","--disable-notifications","--disable-gpu",'--start-maximized']
        opts += cust_opt

        download_path = os.path.join(os.getcwd(), "entrada")
        prefs = {
            "download.default_directory": download_path,
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": False,
            "credentials_enable_service":False,
            "profile.password_manager_enabled":False,
            "autofill.profile_enabled":False,
            "plugins.always_open_pdf_externally":True
        }

        if use_selenoid:
            # Options para camuflagem da automação -
            options = Options()
            prefs = {
                "download.default_directory": f"{download_path}",
                "download.directory_upgrade": True,
                "download.prompt_for_download": False,
            }
            options.add_experimental_option('prefs', prefs)
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.driver = webdriver.Chrome(service=Service(), options=options)
            self.driver.maximize_window() 
        else:
             #Código com Extensao -
            opts = uc.ChromeOptions()
            opts.add_experimental_option("prefs", prefs)
            self.driver = uc.Chrome(options=opts)
        self.driver.implicitly_wait(10)

        return self.driver