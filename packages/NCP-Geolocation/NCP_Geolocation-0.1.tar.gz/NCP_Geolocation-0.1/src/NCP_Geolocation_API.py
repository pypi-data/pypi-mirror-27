import requests, hmac, hashlib, base64
import time, operator
from datetime import datetime
import random
from urllib.parse import quote


class NCP_Geolocation_API:

    def __init__(self, oauth_consumer_key, secret_key):
        self.oauth_consumer_key = oauth_consumer_key
        self.secret_key = secret_key
        self.oauth_nonce = str(random.randrange(1, 98385302039483772298912))
        self.base_url = "https://api.ncloud.com/geolocation/"

    def get_geolocation(self, ip):
        oauth_timestamp = str(time.mktime(datetime.today().timetuple())).replace(".0", "")
        params = self.make_param(ip=ip, oauth_timestamp=oauth_timestamp)
        params_str = ""
        for key, item in sorted(params.items(), key=operator.itemgetter(0)):
            params_str = params_str + str(key) + "=" + str(item) + "&"
        params_str = params_str[0: len(params_str) - 1]

        str1 = "GET&"
        str2 = self.convert(self.base_url) + "&"
        str3 = self.convert(params_str)

        signature = self.make_digest(str1 + str2 + str3, self.secret_key)
        signature = signature.replace("_", "/").replace("-", "+")

        params["oauth_signature"] = signature
        complete_url = requests.get(self.base_url, params=params)
        return complete_url.content.decode("utf-8")

    def make_param(self, ip, oauth_timestamp):
        params = {
            "action": "getLocation",
            "ip": ip,
            "oauth_consumer_key": self.oauth_consumer_key,
            "oauth_nonce": self.oauth_nonce,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": oauth_timestamp,
            "oauth_version": "1.0",
            "responseFormatType": "json",
        }
        return params

    def convert(self, s):
        return ("" + quote(s, safe='')).replace("%2A", "*").replace("%20", "+").replace("~", "%7E")

    def make_digest(self, message, key):
        key = bytes(key + "&", 'UTF-8')
        message = bytes(message, 'UTF-8')
        digester = hmac.new(key, message, hashlib.sha1)
        signature1 = digester.digest()
        signature2 = base64.urlsafe_b64encode(signature1)
        return str(signature2, 'UTF-8')

# Sample Usage
if __name__ == "__main__":
    ncp_geolocation = NCP_Geolocation_API(oauth_consumer_key="$oauth_consumer_key", secret_key="$secret_key")
    print(ncp_geolocation.get_geolocation("125.209.222.142"))
