# Auto Weather Change
##### Made in partnership with [@Legendkiller21](https://github.com/Legendkiller21)

This submod will map the weather in MAS according to the location you're at.

## How to install:
1. Open the zip file from the release

2. Copy the `game/` folder inside the zip to the `DDLC/` folder (the folder with the DDLC exe in it) and **MERGE** the folders

## How to set *Auto Weather Change* up:
1. Head over to [open weather network](https://home.openweathermap.org/api_keys) and generate an api key (Don't worry, they're free)

2. Copy the key and put it into your `DDLC/` folder (the folder with the DDLC exe) in a file called `apikey.txt`.

3. On load, once your api key is valid (it takes a couple hours after generation), Monika will ask you about getting your location, enter your **city name** and she'll do her best to get the right one.

4. A few seconds after this, the weather should start to reflect the weather where you are!

On a side note, if you find that there's locations missing from the menu/lookup txt file, feel free to add them by opening a [pull request](https://github.com/multimokia/MAS-Submods/compare) to this repository adding them!

Just add a line in the bottom of `awc_citylookup.txt` in the following format: `city_name,country_Code,latitude,longitude,state_or_province` (you can check that file for a bunch of examples)