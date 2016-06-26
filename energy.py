from selenium import webdriver
from selenium.webdriver.common.keys import Keys

user = input("Enter the user: ")
passw = input("Enter the password: ")

driver = webdriver.Chrome('/opt/chromedriver')
driver.get("http://www.energeeinc.com/energee/login2.cfm")
# Get username and password fields
userLogin = driver.find_element_by_id("user_username")
passLogin = driver.find_element_by_id("user_password")

# Fill the username and password fields
userLogin.send_keys(user)
passLogin.send_keys(passw)
passLogin.send_keys(Keys.RETURN)

# Format and get the numbers
def get_num(numInText): 
    return int(''.join(ele for ele in numInText if ele.isdigit()))

# Get the week, probability and revenue
def buyProperty():
    driver.get("http://www.energeeinc.com/energee/solar_report_mega.cfm?country=11")
    #Return weeks and convert it into numbers
    weeksNoFormat = driver.find_element_by_xpath("//div[@id='wide_content']/table/tbody/tr[7]/td[2]").text
    weeks = get_num(weeksNoFormat)
    #Return probability of completing the project
    probabilityNoFormat = driver.find_element_by_xpath("//div[@id='wide_content']/table/tbody/tr[9]/td[2]").text
    probability = get_num(probabilityNoFormat)
    #Return revenue of the project
    revenueNoFormat = driver.find_element_by_xpath("//div[@id='wide_content']/table/tbody/tr[13]/td[2]").text
    revenue = get_num(revenueNoFormat)
    results = {'weeks':weeks, 'probability':probability, 'revenue':revenue}
    return results

# Check if is worth to buy.
def isValuable(data):
    weeks = 14
    probability = 90
    revenue = 2000015000
    weeksEnergy = data['weeks']
    probabilityEnergy = data['probability']
    revenueEnergy = data['revenue']
    print(data)
    if weeksEnergy < weeks and probabilityEnergy > probability and revenueEnergy > revenue:
        return True
    else:
        return False

#Buys the property if the requirements are enough
def buildIt():
    while (True):
        if isValuable(buyProperty()) == True:
            driver.find_element_by_xpath("//div[@id='wide_content']/table/tbody/tr[1]/td[3]/p/a").click()
            if "Congratulations" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text:
                print("Finished")
                break
            elif "continue" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text:
                while True:
                    print("building")
                    driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/map/area[2]").click()
                    
                    if "Congratulations" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text:
                        break
                    
                    elif "Sorry" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text:
                        break
                    
                    elif "run out" in driver.find_element_by_xpath("//div[@id='wide_content']/p[2]").text:
                        break
            
            elif "Sorry" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text:
                print("Failed")
                break
        
        try:
            if "run out" in driver.find_element_by_xpath("//div[@id='wide_content']/p[2]").text:
                print ("Run out of credits")
                return False
        except:
            print("Hola")
        return True

while True:
    if buildIt():
        print("Ok")
    else:
        break


# click to buy  driver.find_element_by_xpath("//div[@id='wide_content']/table/tbody/tr[1]/td[3]/p/a").click()

# Message when the project is complete   "Congratulations" in driver.find_element_by_xpath("//table[@class='black_13']/tbody/tr/td[1]/div").text
