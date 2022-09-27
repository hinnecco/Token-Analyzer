from web3 import Web3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

bsc = 'https://bsc-dataseed.binance.org/'    
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())

def findAbi(address, driver):
    url = f'https://bscscan.com/address/{address}#code'

    if not driver:
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(url)
    page_soup = BeautifulSoup(driver.page_source, features="lxml")
    abi = page_soup.find_all("pre", {"class": "wordwrap js-copytextarea2"})

    with open(f'data/ABI_{address}.txt', 'w') as f:
        f.write(abi[0].text)

    driver.delete_all_cookies()
    driver.get("chrome://settings/clearBrowserData")
    # driver.close()
    return abi[0].text

def tokenAbi(address, driver=None):
    try:
        filename = f'ABI_{address}.txt'
        with open(f"data/{filename}") as f:
            abi = f.readlines()
            return abi[0]
    except IOError:
        abi = findAbi(address, driver)
        return abi

coinToCheck = Web3.toChecksumAddress('0x0ecaf010fc192e2d5cbeb4dfb1fee20fbd733aa1')
TokenAbi = tokenAbi(coinToCheck)
coinToCheckContract = web3.eth.contract(address=coinToCheck, abi=TokenAbi)
symbol = coinToCheckContract.functions.symbol().call()
events = coinToCheckContract.getPastEvents('allEvents')
print(symbol)