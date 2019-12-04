import requests
from bs4 import BeautifulSoup
from random import choice


def get_proxy():
    url = 'https://www.sslproxies.org/'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return {'https': choice(list(map(lambda x: x[0]+':'+x[1],
                                     list(zip(map(lambda x: x.text, soup.findAll('td')[::8]),
                                              map(lambda x: x.text, soup.findAll('td')[1::8])))[:100])))}


def proxy_request(request_type, url, **kwargs):
    flag = 0
    response = ''
    while flag < 50:
        try:
            proxy = get_proxy()
            print(f"Using proxy {proxy['https']}")
            response = requests.request(request_type, url, proxies=proxy, timeout=5, **kwargs)
            if response.status_code == 200:
                break
            else:
                print(response.status_code)
                continue
        except Exception as e:
            # print(e)
            pass
        flag += 1
    return response


def main():
    url = "https://www.whatismybrowser.com/detect/ip-address-location"
    response = proxy_request('get', url)

    try:
        print(response.status_code)
        soup = BeautifulSoup(response.content, 'html.parser')
        changed_location = soup.select('#detected_value')[0].text
        print(f"Changed Location: {changed_location}")
    except Exception as e:
        print("No response found!")


if __name__ == "__main__":
    main()
