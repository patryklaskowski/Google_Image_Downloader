Python 3.7.4

google_image_downloader.py

====================================
This program downloads n files of 'XYZ' from google images and save them inside a folder
with the same name as term that is searching that is prepared inside the folder where google_image_downloader.py is located.
====================================
NOTE: If folder exists, script removes it with all content and creates new one.
====================================

To determine SERCH TERM:
- use '--search' flag and then type in search term.
To determine AMOUNT of needed images:
- use '--amount' flag then type in number from 0 to 500.

Normally program runs browser without headless mode.
To run program in HEADLESS mode:
- add '--headless' flag.

====================================
Example:
[1] Download 30 images of 'snowboard' using headless browser:
> python3 google_image_downloader.py --search snowboard --amount 30 --headless

[2] Download 5 images of 'apple cortland' without headless mode:
> python3 google_image_downloader.py --search apple cortland --amount 5
====================================



MAKE SURE ChromeDriver path is correct
====================================
