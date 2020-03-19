<h1>google_image_downloader.py</h1>
<em>build with Python 3.7.4</em><br><br>

-----
**This script downloads images from Google Images based on provided `--search` *SEARCH_TERM* and `--amount` *AMOUNT*.**<br>
**By default script is running Google Chrome. But You may run the program headless using `--headless` flag.**<br>
**Imges will be saved in folder with *SEARCH_TERM* name that will be created where *google_image_downloader.py* is located.**<br><br>

**NOTE:** If folder named *SEARCH_TERM* exists in *google_image_downloader.py* location, script removes it with all content and creates new one.

-----
**How to use?**<br>
`python3 google_image_downloader.py --search SEARCH_TERM --amount N`

1) Make sure there is proper chromedriver in chromedriver_folder.<br>
There is already one zip file with chromedriver for MacOS, **unzip** and done!<br>
If you need different chromedriver, [download it here](https://chromedriver.chromium.org/downloads).

2) Make sure that dependencies are installed and ready to use (*requirements.txt*).

3) Run script using **Python3** (see examples below).<br><br><br>

-----
**Examples:**

* Download 30 images of 'snowboard' using headless browser:<br>
`python3 google_image_downloader.py --search snowboard --amount 30 --headless`<br>

* Download 5 images of 'apple cortland' without headless mode:<br>
`python3 google_image_downloader.py --search apple cortland --amount 5`<br><br>

-----
**3 types of flags ready to use:**<br>
* `--search` : determines search term
* `--amount` : determines amount of images to download
* `--headless` : determine headless browser run when provided

-----
**Modules used:**<br>
* `selenium`
* `requests`
* `os`
* `shutil`
* `time`
* `sys`

-----
-----
