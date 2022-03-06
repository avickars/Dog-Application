from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome(ChromeDriverManager().install())

def main():
    # Starting URL
    link = 'https://www.petfinder.com/search/dogs-for-adoption/ca/british-columbia/?distance=Anywhere&page='

    driver = webdriver.Chrome(ChromeDriverManager().install())

    COUNT=0

    for i in range(1, 2800):
        driver.get(link + str(i))
        timeout = 5  # seconds
        wait = WebDriverWait(driver, timeout)
        time.sleep(5)
        pet_links = driver.find_elements(By.CLASS_NAME, "petCard-link")

        for pet_link in pet_links:
            # print(pet_link.get_attribute('href'))
            with open('pet_links.txt', 'a') as f:
                f.write(pet_link.get_attribute('href'))
                f.write('\n')

            COUNT += 1

            if COUNT % 500 == 0:
                print(f"{round((COUNT / 15000) * 100, 3)} %")

            if COUNT >= 15000:
                return True




if __name__ == '__main__':
    main()