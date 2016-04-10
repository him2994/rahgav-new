File with proxies(now contains 2 proxies):
	proxy_list.txt
    
See input arguments for the program:
	python patent.py -h
    

Installation:
All python requirements are listed in requirements.txt.
You can install them all like this:
	pip install -r requirements.py

You will also nee PhantomJs install in you system for selenium to work without a browser window.
That's a separate program.

Death by captcha login and password can be set in patent.py, change these values to match yours:
	captcha_login = "login"
	captcha_pwd = "password"
