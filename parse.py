# parse the url
import re

kasa_re = re.compile(r"^kasa://(?P<host>[a-zA-Z0-9.-]+)(:(?P<port>[0-9]+))?/(?P<field>[a-zA-Z-_]+)?\??(?P<query_params>[^\?]+)?")

class KasaParams():
    def __init__(self, url) -> None:
        match = kasa_re.match(url)
        if match:
            self.host = match.group('host')
            self.port = match.group('port')
            self.field = match.group('field')
        else:
            print("URL does not match expected format:")
            print(url)
            self.host = ""
            self.port = ""
            self.field = ""

# run this to test the parseer
if __name__ == "__main__":
    IP = "remotehost"
    url_1 = "kasa://{}:80/voltage".format(IP)
    url_2 = "kasa://{}:443/current".format(IP)
    url_3 = "kasa://{}/power".format(IP)

    print("host port field")
    print("===============")
    for url in [url_1, url_2, url_3]:
        params:KasaParams = KasaParams(url)
        print(params.host, params.port, params.field)