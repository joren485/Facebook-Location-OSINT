# Facebook-Location-OSINT
Retrieve someones private Facebook location, using their public information.

What does it do?
------
If the place where someone lives is not public on their Facebook account, this program will guess it given the targets public facebook account.

How does it work?
------
1.Login to Facebooks mobile site.
2.Get the links to every public photo
3.Get the usernames of everyone that liked a photo
4.Get the public hometowns and current cities of every user from step 3
5.Return the city / town that was found the most times.

How to use it?
------
Python 

Why do I need to give my Facebook credentials?
------
Public information on Facebook is only available to people that have logged in.
Thus, to get the public information an account is needed.

**Warning:** This will generate a login warning.

Requirements
------
* Requests library for Python
* Not the Python Facebook API, this is a scraper it gets all the information from the mobile facebook site.
