"""
Powder Day Finder
Thomas & Ethan
CSI 160-1/2
11/29/2020
https://github.com/fearherbs1/Powder-Day-Finder
"""

# Default python Libraries.
import configparser
import os
import sys
import datetime

# External python Libraries.
import requests


class Colors:
    """
    Class that holds our color ASCII escape characters and color values.

    """
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def welcome():
    """
    First run Welcome function that displays the splash screen and prompts the user to press enter to start.

    :return: None
    """
    clear_screen()
    # welcome the user with cool asci art
    print_splash_screen()
    input("Press Enter to Start")


def main():
    """
    The Main menu function caller. Calls the function based on the users task choice.

    :return: None
    """

    task = main_menu()

    # task checker (this could be a switch statement)
    if task == 1:
        print("Option 'Check for Powder Days' Selected!")
        clear_screen()
        check_for_powder_day()
    elif task == 2:
        print("Option 'Check for any snowfall' Selected!")
        clear_screen()
        check_for_any_snowfall()
    elif task == 3:
        print("Option 'Print loaded resorts' Selected!")
        clear_screen()
        print_loaded_resorts()
    elif task == 4:
        print("Option 'Print loaded options' Selected!")
        clear_screen()
        print_loaded_options()
    elif task == 5:
        print("Option 'About' Selected!")
        clear_screen()
        about()
    elif task == 6:
        clear_screen()
        sys.exit()


def print_loaded_resorts():
    """
    Prints the resorts that are loaded into the config file.
    Loads the options into a dictionary then prints them one by one.

    :return: None
    """
    tracked_resorts = readconfig("ski_resorts")
    print(f"{Colors.RED} Resorts I found in the config file are:{Colors.END}\n")
    for resort in tracked_resorts:
        print(f"{Colors.BLUE}{resort} {Colors.GREEN}with a location of: "
              f"{Colors.PURPLE}{tracked_resorts[resort]}{Colors.END}\n")
    input("Press Enter to return to the main menu.")
    main()


def print_loaded_options():
    """
    Prints the options that are loaded into the config file.
    Loads the options into a dictionary then prints them one by one.
    Brings the user back to the main menu one finished.

    :return: None
    """
    options = readconfig("options")
    print("The Options I found in the config file are:\n")
    for option in options:
        print(f"{Colors.BLUE}{option}{Colors.GREEN} with a value of: "
              f"{Colors.PURPLE}{options[option]}{Colors.END}\n")
    input("Press Enter to return to the main menu.")
    main()


def check_for_any_snowfall():
    """
    Reads the config then checks for snow using the get_weather() and weather_check_snow() functions.
    The results are loaded into a dictionary from these functions and displayed depending on the values.
    The units provided to the user are based on what units are selected in the config file.
    Brings the user back to the main menu one finished.

    :return: None
    """
    options = readconfig("options")
    units = options["units"]
    tracked_resorts = readconfig("ski_resorts")
    if units == 'i':
        big_unit = "Feet"
        small_unit = "Inches"
    else:
        big_unit = "Centimeters"
        small_unit = "Millimeters"

    print("checking for snow...\n")

    for resort in tracked_resorts:
        resort_weather = get_weather(tracked_resorts[resort])
        snow_present = weather_check_snow(resort_weather, units)
        dict_empty = not snow_present
        if dict_empty is False:
            print(f"{Colors.GREEN}Snow forecasted at {resort}!{Colors.END}")
            for key, val in snow_present.items():
                us_date = datetime.datetime.strptime(key, '%d/%m/%Y').strftime('%m/%d/%Y')
                if units == 'i':
                    print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                          f"{Colors.PURPLE} {val // 12} {big_unit} {val % 12} {small_unit}!{Colors.END}\n")
                else:
                    print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                          f"{Colors.PURPLE} {val // 10} {big_unit} {val % 10} {small_unit}!{Colors.END}\n")
        else:
            print(f"{Colors.RED}No Snow Forecasted at {resort} :({Colors.END}\n")
    input("Press Enter to return to the main menu.")
    main()


def check_for_powder_day():
    """
    Reads the config then checks for Powder Days using the get_weather() and weather_check_snow() functions.
    The results are loaded into a dictionary from these functions and displayed depending if the snow meets a
    threshold.
    The units provided to the user are based on what units are selected in the config file.
    Brings the user back to the main menu one finished.


    :return:
    """
    options = readconfig("options")
    units = options["units"]
    tracked_resorts = readconfig("ski_resorts")
    if units == 'i':
        big_unit = "Feet"
        small_unit = "Inches"
    else:
        big_unit = "Centimeters"
        small_unit = "Millimeters"

    print("checking for snow...\n")

    for resort in tracked_resorts:
        resort_weather = get_weather(tracked_resorts[resort])
        snow_present = weather_check_snow(resort_weather, units)
        dict_empty = not snow_present
        if dict_empty is False:
            for key, val in snow_present.items():
                us_date = datetime.datetime.strptime(key, '%d/%m/%Y').strftime('%m/%d/%Y')
                if units == 'i':
                    if val >= 6.0:
                        print(f"{Colors.BOLD}{Colors.BLUE}Powder{Colors.YELLOW} Day{Colors.RED} Found!!{Colors.END}")
                        print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                              f"{Colors.PURPLE }{val // 12} {big_unit} {val % 12} {small_unit}!{Colors.END}\n")
                    else:
                        print(f"{Colors.YELLOW}Snow Found, but not reaching powder day levels at {resort}{Colors.END}")
                        print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                              f"{Colors.PURPLE} {val // 12} {big_unit} {val % 12} {small_unit}!{Colors.END}\n")
                else:
                    if val >= 152.4:
                        print(f"{Colors.BOLD}{Colors.BLUE}Powder{Colors.YELLOW} Day{Colors.RED} Found!!{Colors.END}")
                        print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                              f"{Colors.PURPLE} {val // 10} {big_unit} {val % 10} {small_unit}!{Colors.END}\n")
                    else:
                        print(f"{Colors.YELLOW}Snow Found, but not reaching powder day levels at {resort}{Colors.END}")
                        print(f"{Colors.GREEN}Date of snow: {Colors.BLUE}{us_date}{Colors.GREEN} Amount of Snow:"
                              f"{Colors.PURPLE} {val // 10} {big_unit} {val % 10} {small_unit}!{Colors.END}\n")
        else:
            print(f"{Colors.RED}No Powder Day, Or Snow Forecasted at {resort} :({Colors.END}\n")
    input("Press Enter to return to the main menu.")
    main()


def main_menu():
    """
    Draws the main menu and prompts the user to make a selection. User input is monitored to prevent a traceback.
    notifies the user if they enter an invalid selection.

    :return: the users choice from the prompt
    """
    clear_screen()
    print_menu()
    while True:
        try:
            choice = int(input("Please Choose Your Option:\n"))
            if 0 < choice < 7:
                break
            else:
                clear_screen()
                print_menu()
                print("That is not a valid option! Try Again")
                continue
        except ValueError:
            clear_screen()
            print_menu()
            print("That is not a valid option! Try Again")

    return choice


def print_menu():
    """
    Main menu ascii art. This is put in its own function to prevent spam of the main menu art in the code.

    :return: None
    """
    print(
        '''
        +----------------------------+
        |         Main Menu:         |
        +----------------------------+
        | 1.) Check for Powder Days  |
        | 2.) Check for any snowfall |
        | 3.) Print loaded resorts   |
        | 4.) Print loaded options   |
        | 5.) About                  |
        | 6.) Exit                   |
        +----------------------------+
        '''
    )


def about():
    """
    The about page showing some basic info about the program.
    Send the user back to the main menu when finished.

    :return: None
    """

    print(
        '''
          _____                 _             _____                ______ _           _
         |  __ \               | |           |  __ \              |  ____(_)         | |
         | |__) |____      ____| | ___ _ __  | |  | | __ _ _   _  | |__   _ _ __   __| | ___ _ __
         |  ___/ _ \ \ /\ / / _` |/ _ \ '__| | |  | |/ _` | | | | |  __| | | '_ \ / _` |/ _ \ '__|
         | |  | (_) \ V  V / (_| |  __/ |    | |__| | (_| | |_| | | |    | | | | | (_| |  __/ |
         |_|   \___/ \_/\_/ \__,_|\___|_|    |_____/ \__,_|\__, | |_|    |_|_| |_|\__,_|\___|_| v1.0
         A tool to keep an eye out for that sweet pow.      __/ |
                                                           |___/
        Created by Thomas and Ethan
        
        ** Please Read the README for usage instructions! **
        
        This Program was created as a final project for CSI-160-1/2 Python Programming,
        a Class offered at Champlain College.
        I want to thank Professor Dr. Frank Canovatchel for offering us an awesome intro 
        to python, as well as running the class during the COVID-19 Pandemic.
        '''
    )
    input("Press Enter to return to the main menu.")
    main()


def print_splash_screen():
    """
    Splash screen ascii art. This is put in its own function to prevent spam of the main menu art in the code.

    :return: None
    """
    print(
        '''
        Welcome to the
          _____                 _             _____                ______ _           _
         |  __ \               | |           |  __ \              |  ____(_)         | |
         | |__) |____      ____| | ___ _ __  | |  | | __ _ _   _  | |__   _ _ __   __| | ___ _ __
         |  ___/ _ \ \ /\ / / _` |/ _ \ '__| | |  | |/ _` | | | | |  __| | | '_ \ / _` |/ _ \ '__|
         | |  | (_) \ V  V / (_| |  __/ |    | |__| | (_| | |_| | | |    | | | | | (_| |  __/ |
         |_|   \___/ \_/\_/ \__,_|\___|_|    |_____/ \__,_|\__, | |_|    |_|_| |_|\__,_|\___|_| v1.0
         A tool to keep an eye out for that sweet pow.      __/ |
                                                           |___/
        Created by Thomas and Ethan
        ** Please Read the README for usage instructions! **
        CSI-160-1/2
        '''
    )


def clear_screen():
    """
    Clears the screen based on the os that the user is running.
    Windows uses 'cls' instead of 'clear' so a check is run to make sure the correct command is used.

    :return:
    """
    if os.name == 'nt':
        _ = os.system('cls')

    else:
        _ = os.system('clear')


def readconfig(conf_section):
    """
    Reads the specified section of the config using the configparser library.


    :param conf_section: The config section to read from
    :return: the options and their values in a dictionary.
    """
    config = configparser.ConfigParser()
    config.read('options.ini')

    config_dict = {}  # our empty options dict

    for x in config[conf_section]:  # Loads our options int a dictionary
        config_dict[x] = config[conf_section][x]

    return config_dict


def get_weather(loc):
    """
    Grabs the weather data from the API based on the location provided.

    :param loc: Location in coordinates with 3 decimal places.
    :return: info from API in json format.
    """
    api_key = "API_KEY_HERE!!"
    app_id = "APP_ID_HERE!!"
    url = f"http://api.weatherunlocked.com/api/forecast/{loc}?app_id={app_id}&app_key={api_key}"

    weather = requests.get(url)
    return weather.json()


def weather_check_snow(raw_weather, unit_selection):
    """
    Sorts through the raw weather data and checks for days that have snow forecasted.

    :param raw_weather: The raw weather forecast with all days included.
    :param unit_selection: Units to be used this is either 'm' for metric and 'i' for imperial.
    :return: a dictionary with the days with forecasted snow in the unit system provided.
    """

    weather = raw_weather["Days"]  # loads the days into weather. The days are dictionary pairs inside a list.
    days_with_snow = {}  # create our empty dictionary that will contain our days with snowfall along with snow amount

    if unit_selection == 'i':
        for day in weather:

            if day['snow_total_in'] > 0:  # checks for snowfall in the total for day section of api reply.
                days_with_snow[day['date']] = day['snow_total_in']

            else:
                continue
    else:
        for day in weather:

            if day['snow_total_mm'] > 0:  # checks for snowfall in the total for day section of api reply.
                days_with_snow[day['date']] = day['snow_total_mm']

            else:
                continue

    return days_with_snow


welcome()
main()
