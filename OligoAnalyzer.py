from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class OligoAnalyzer(object):
    def __init__(self):
        self.chromedriver_location = "/Users/Eric/Documents/myStuff/PrimerFinder/chromedriver"
        self.oligo_analyzer_link = "http://idtdna.com/calc/analyzer"
        self.browser = webdriver.Chrome(self.chromedriver_location)
        self.browser.get(self.oligo_analyzer_link)

        self.temperature_dict = {}

    def analyze_temp(self, DNA_string):
        print(DNA_string)

        if DNA_string in self.temperature_dict:
            return self.temperature_dict[DNA_string]

        text_box = self.browser.find_element_by_xpath("//*[@id='OligoAnalyzer']/div[2]/div[1]/div/div[1]/div[1]/div/div/textarea")
        text_box.clear()
        text_box.send_keys(DNA_string)

        analyze_button = self.browser.find_element_by_xpath("//*[@id='analyze-button']")
        analyze_button.click()

        temp = None
        temp_val = None

        while (not temp or not temp_val):
            try:
                temp = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='OAResults']/div/div[1]/div[3]/div/div/table/tbody/tr[5]/td[2]/span")))
                temp_text = temp.text
                temp_val = float(temp_text[:temp_text.find(' ºC')])
            except Exception:
                temp_val = None

        self.temperature_dict[DNA_string] = temp_val
        return temp_val


    def __del__(self):
        try:
            self.browser.quit()
        except Exception:
            pass







if __name__ == "__main__":
    import random

    oa = OligoAnalyzer()
    bases = ['A','C','G','T']
    for _ in range(10):
        print(oa.analyze_temp("".join([random.choice(bases) for _ in range(random.randint(32,64))])))
