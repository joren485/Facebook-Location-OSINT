# Facebook-Location-OSINT
Retrieve someones private Facebook location, using their public information.

This is working, but needs alot of work.

This does not use the Facebook API, it is a scraper.
Input you're facebook email and password(they'll stay on you're computer, check the code) and the username of you're target, and the program does its magic.

Technique:
------
  1. Get every public photo's likes.
  2. Check wheter their hometown or current living city is public for every person that liked a photo .
  3. Return the city or town that was found the most times.

Warning: Using this script might trigger an login alert, nothing to worry about.
  
TODO:
------
* Improve error handeling
* Improve regular expressions
* Use more than only photos
* Check wheter the target has an available location


