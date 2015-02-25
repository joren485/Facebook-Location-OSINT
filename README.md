# Facebook-Location-OSINT
Retrieve someones private Facebook location, using their public information.

This does not use the Facebook API, it is a scraper.
Input you're facebook email and password(they'll stay on you're computer, check the code) and the username of you're target, and the program does its magic.

Technique:
------
  1. Get every public photo's likes.
  2. Check wheter their hometown or current living city is public for every person that liked a photo .
  3. Return the city or town that was found the most times.
  
  
You need to input the username of a Facebook users.
Warning: Using this script might trigger an login alert, nothing to worry about.
  
  
