# Synthetix-Statistics-Bot-For-Twitter
is an advanced tweet bot that provides information about Synthetix platform statistics, with fine-tuning options.
## Features
The bot provides information about:
* the current price of SNX
* total exhange volume
* Trading fees
* Total value locked ETH/BTC
* Amount of SNX staked
* Issuance ratio, Networck c-ratio, Active c-ratio (weekly)
* includes two finished templates 

Scraper has the ability to manage the collected data by means of a json file,this file has the following structure:
```
"ObjectName":Patch
```
where ObjectName is the name that can be used from the template later on , Patch is the path to the item you are looking for in xpatch string format
example:
```
"snxPr":"//div[text()='SNX PRICE']/following::div[3]/div[1]"
```

Bot has a flexible system of templates that allows you to change the published material without changing the source code, this system is based on python f string,where the available objects for substitution are any object described in the file `config/object_list.json`
Sample template:
```
SNX price: {snxPr}$
Exhange volume: {ExchangeVolume}$
Trading fees: {TotatTradingFees}$
Total value locked ETH: {ETHLocked} ETH
Total value locked BTC: {BTCLocked} BTC
Amount of SNX staked: {snx_staked_percent}% of total
```
The default hourly and weekly templates are located: `tamplates/hourly.txt` and `tamplates/weekly.txt` this can be changed in the configuration file.
twit exemple:

# Deployment
1. Clone this repo
2. Make Python `venv`
3. Run `pip install requirement.txt` in the `venv`
4. Create a new app in your tweeter developer account (https://developer.twitter.com/en/portal/projects-and-apps)
5. Insert the tweeter tokens in the appropriate places in the file  `config/config.py`
6. Create Heroky app
7. In sttings tap on heroku add Buildpacks *heroku/python *heroku/google-chrome *heroku/chromedriver
8. On the Settings tab of your Heroku app, under Config Vars, add `CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver` and `GOOGLE_CHROME_BIN=/app/.apt/usr/bin/google-chrome`
9. Install Heroku CLI
10. Follow the instruction on the Deploy tab of your Heroku App
11. If the application does not work check if your worker is running in the resources tab, If the application does not work after that, try this `heroku ps:scale worker=1`
