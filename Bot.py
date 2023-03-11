from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common
import time
class Bot:
    """Bot used as high level interaction with web-browser via Javascript exec"""
    def __init__(self, bot):
        self.bot = bot

    def getBot(self):
        return self.bot

    def getVideoUploadInput(self):
        # Click accept cookies
        element = self.bot.execute_script("""return document.querySelector("tiktok-cookie-banner").shadowRoot.querySelector(".button-wrapper").querySelector("button")""")
        element.click()

        # Button is nested in iframe document. Select iframe first then select upload button
        WebDriverWait(self.bot, 20).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.bot.switch_to.frame(0)
        self.bot.implicitly_wait(10)
        file_input_element = self.bot.find_elements(By.CLASS_NAME, "upload-card")[0]
        # document.getElementsByClassName("op-part")[0].childNodes[1]  # New locator
        return file_input_element

    def getCaptionElem(self):
        # Button Works
        self.bot.implicitly_wait(3)
        self.bot.execute_script(
            f'var element = document.getElementsByClassName("public-DraftStyleDefault-block")[0].children['
            f'0].getAttribute("data-offset-key");')
        caption_elem = self.bot.find_elements(By.CLASS_NAME, "public-DraftStyleDefault-block")[0]
        return caption_elem

    def selectPrivateRadio(self):
        try:
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tiktok-select-selector")))
            # open_menu = self.bot.find_elements(By.CLASS_NAME, "permission")[0].find_elements(By.XPATH, './*')[1].find_elements(By.XPATH, './*')[0]
            open_menu = self.bot.find_elements(By.CLASS_NAME, "tiktok-select-selector")[0]
            open_menu.click()
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tiktok-select-dropdown-item")))
            self.bot.find_elements(By.CLASS_NAME, "tiktok-select-dropdown-item")[2].click()

        except Exception as e:
            print(f"Private Toggle Error: {e}")
            self.click_elem(
                # 'document.getElementsByClassName("radio-group")[0].children[2].click()',
                "document.getElementsByClassName('permission')[0].childNodes[1].childNodes[2].click()",
                "Javascript had trouble finding the 'private' toggle radio button with given selector,"
                " please submit yourself and edit submit button placement.!!")


    def selectPublicRadio(self):
        # Button Works
        try:
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tiktok-select-selector")))
            # open_menu = self.bot.find_elements(By.CLASS_NAME, "permission")[0].find_elements(By.XPATH, './*')[1].find_elements(By.XPATH, './*')[0]
            open_menu = self.bot.find_elements(By.CLASS_NAME, "tiktok-select-selector")[0]
            open_menu.click()
            WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "tiktok-select-dropdown-item")))
            self.bot.find_elements(By.CLASS_NAME, "tiktok-select-dropdown-item")[0].click()

        except Exception as e:
            self.click_elem(
                # 'document.getElementsByClassName("radio-group")[0].children[0].click()',
                "document.getElementsByClassName('permission')[0].childNodes[1].childNodes[0].click()",
                "Javascript had trouble finding the 'public' toggle radio button with given selector,"
                " please submit yourself and edit submit button placement.!!")


    def selectScheduleToggle(self):
    # deprecated function
        self.click_elem(
            "document.getElementsByClassName('switch-container')[0].click()",
            "Javascript had trouble finding the 'schedule' toggle radio button with given selector,"
            " please submit yourself and edit submit button placement.!!")

    def uploadButtonClick(self):
        # Button Works
        try:
            """Newer layout."""
            # WebDriverWait(self.bot, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "op-part-v2")))
            # operation_elems = self.bot.find_elements(By.CLASS_NAME, "op-part-v2")[0]
            # upload_elem = operation_elems.find_elements(By.XPATH, './*')[1]
            # upload_elem.click()
            post_button = self.bot.find_elements(By.CLASS_NAME, "css-y1m958")[0]
            post_button.click()
        except Exception as e:
            try:
                upload_name = "Post"
            except Exception as e:
                try:
                    """Older Layout"""
                    self.click_elem(
                        'document.getElementsByClassName("btn-post")[0].click()',
                        "Javascript had trouble finding the post button with given selector,"
                        " please submit yourself and edit submit button placement.!!")
                except Exception as e:
                    print("Could not upload, please upload manually.")



    def click_elem(self, javascript_script, error_msg):
        try:
            self.bot.execute_script(javascript_script)
        except selenium.common.exceptions.JavascriptException as je:
            print(error_msg)
            print(je)
        except Exception as e:
            print(f"Unhandled Error: {e}")
            exit()
        return