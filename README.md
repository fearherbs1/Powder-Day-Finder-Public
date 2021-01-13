# Powder Day Finder Public
My CSI-160 Final Project for Finding That Sweet Pow.  

This was created duing my sophomore year by myself, Thomas, and my good friend Ethan.    

Using this program you can check for snow and powder days a week out at any ski resort.

# Usage
install the requests library with `pip install requests`  

Grab a **free** api key from [HERE](https://developer.weatherunlocked.com/plans/pricing)  
Place your API key and APP ID on lines 354 and 355 respectively.  

Configure your options and resorts in the options.ini file.

Resorts have to be added in this format:  
`ski resort = coordinates`  
Note: coordinates must be rounded to 3 decimal places and comma separated without a space.  
ex: `Killington = 43.603,-72.804`  
These coordinates can be easily found using Google Maps.


Run the program and hit enter to start. This will bring you to the main menu.

A quick rundown of the options is listed below:
1. Will return all resorts with a powder day over the next week. This mode also lists any snow if found
2. Will return all accounts of snow at the configured resorts for the next week
3. Shows your currently configured ski resorts
4. Shows your currently configured options (currently only units is supported)
5. Brings you to the about page
6. Exits the program

# Options
units: i or m  
(Sets units to either imperial to metric)

# Dependencies
* requests

