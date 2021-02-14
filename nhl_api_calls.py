import requests

url = "http://statsapi.web.nhl.com/api/v1/{}"


def make_call(endpoint, customdate=""):
    payload = {'date': customdate} if customdate else ""
    r = requests.get(url.format(endpoint), params=payload)
    if r.status_code == 200:
        return r.json()
    else:
        with open("log.txt", "a") as f:
            f.write(today + ": " + "nhl_api_calls module: Response status code not 200\n")
            f.write(r.text)
        raise ValueError("nhl_api_calls module: Response status code not 200")


if __name__ == "__main__":
    pass
