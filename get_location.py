import sys
import re

try:
    import requests

except ImportError:
    print "[!] Couldn't import requests"
    sys.exit()

if len(sys.argv) < 4:
    print "Usage: get_location.py target_username my_fb_email my_fb_password"
    print "Example get_location.py user.name user@gmail.com password"
    sys.exit()

user = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

def get_graphID_user(s, username):
    """Get the Facebook graph api id from a user"""
    r = s.get("https://m.facebook.com/{user}".format(user=username))
    match = re.search(r'photo.php\?fbid=\d*&amp;id=(\d*)&', r.text)
    if match:
        graph_id = match.group(1)
        return graph_id
    else:
        return False

def get_public_data(s, graphID, key):
    """Get the public information from the Facebook graph api"""
    r = s.get("http://graph.facebook.com/?id={graphid}".format(graphid=graphID))
    return r.json()[key]

# Create session, and set the User-Agent
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"

# Retrieve the right parameters for the login
data = requests.get("https://m.facebook.com/").text
params = {'lsd': None, 'm_ts': None, 'pxr': None, 'li': None, 'width': None, 'ajax': None, 'version': None, 'gps': None, 'charset_test': None}
for p in params.keys():
    match = re.search(r'name="place_holder" value="(.*?)"'.replace("place_holder", p), data)
    if match:
        params[p] = match.group(1)

# Set the important parameters
params['email'] = username
params['pass'] = password
params['login'] = 'Log In'

# Login
r = s.post(r"https://m.facebook.com/login.php?refsrc=https%3A%2F%2Fm.facebook.com%2F&refid=8", data=params)

# If the login failed, exit
if '/recover/initiate/' in r.text:
    print "[!]Login unsuccessful."
    sys.exit()
print "[+]Login successful"

# Retrieve the id for the target graph ID, and the target country 
user_id = get_graphID_user(s, user)
user_locale = get_public_data(s, user_id, "locale")
print "\t[+]Found {user} ID: {graphid}".format(user=user, graphid=user_id)
print "\t[+]Found {user} locale: {locale}".format(user=user, locale=user_locale)

# Retrieving the albums
print "[+]Locating photos"
r = s.get("https://m.facebook.com/{user}?v=photos".format(user=user))
albums = re.findall(r"/{user}/albums/\d*/".format(user=user), r.text)


link_ids = []
possible_like_targets = []
for album_link in albums:

    # Get the photos of an album
    album_r = s.get("https://m.facebook.com{album}".format(album=album_link))

    # Get the title of the album
    match = re.search("<title>(.*)</title>", album_r.text)
    if match:
        print "[+]Album found: {title}".format(title=match.group(1)) 

    # Get the photo ids 
    photo_ids = re.findall(r"/photo.php\?fbid=(\d*)&amp;id={graphid}".format(graphid=user_id), album_r.text)
    print "\t[+]Containing {n} photo's".format(n=len(photo_ids))

    
    for photo_id in photo_ids:
        print "\t[+]Photo {photo_id}".format(photo_id=photo_id)

        # Get the usernames of everyone that liked the photo 
        likes_r = s.get("https://m.facebook.com/browse/likes/?id={link_id}".format(link_id=photo_id))
        target_names = re.findall(r'<a href="\/([\w\.]*)\?', likes_r.text)
        
        print "\t[+]Photo has {n} likes".format(n=len(target_names))

        
        for target_name in target_names:

            # Because my re-fu is not godlike, an if statement to clean out the false-positives.
            # Also profile.php support needs to be added
            if ".php" in target_name:
                continue
            
            possible_like_targets.append(target_name)

# Only use the usernames that liked more than once
# It improves the changes that they actually know the target, and speeds things up
like_targets = list(set([like_target for like_target in possible_like_targets if possible_like_targets.count(like_target) > 1]))
print "[+]Found {n} targets".format(n=len(like_targets))

places = []
for like_target in like_targets:
    print "[+]Trying target: {target}".format(target=like_target)

    # Get the locale of the like_target
    # If they are not from the same country, don't even bother
    like_target_id = get_graphID_user(s, like_target)
    like_target_locale = get_public_data(s, like_target_id, "locale")

    if like_target_locale == user_locale:

        # Get the info of like_target
        r = s.get("https://m.facebook.com/{user}?v=info&nocollections=1".format(user=like_target))

        data = r.text

        # If there is a hometown and Current City available, retrieve them
        for index_pattern in ("Hometown", "Current City"):
            try:
                index = data.index(index_pattern)
            except ValueError:
                continue

            # Retrieve the city
            match = re.search(r'<a href="\/profile.php\?id=\d*">([\w\s,]*)<\/a>', data[index:])
            if match:
                places.append(match.group(1))

# Get the most common cities
most_common = sorted(places, key=lambda x: places.count(x), reverse = True)[0]
print "-"*20
print "[+]Found city: {city} | {part} out of {whole}".format(city=most_common, part=places.count(most_common), whole=len(places))
