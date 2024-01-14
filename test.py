from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
 
url = "https://scrapeme.live/shop/" 
 
options = webdriver.ChromeOptions() #newly added 


with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver: 
    driver.get('https://www.google.com/maps/dir/899+Nebo+Rd,+Hannon,+ON+L0R+1P0,+Canada/91+Osler+Dr,+Hamilton,+ON+L9H+4H4,+Canada/700+Main+St+W,+Hamilton,+ON+L8S+1A5,+Canada/')
	# Scroll down till the end
    driver.find_element(By.CSS_SELECTOR, ".yra0jd").click()
    specific_element = driver.find_element(By.CSS_SELECTOR, "canvas.aFsglc:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(specific_element).perform()
    # Take a screenshot of just the located element and save it to a file
    specific_element.screenshot('selenium-dynamic-element.png')
 
 
    # Close the browser
    driver.quit()