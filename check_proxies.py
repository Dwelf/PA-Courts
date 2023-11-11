import requests

from threading import Thread
import queue
import datetime as dt

Q = queue.Queue()
VALID_PROXIES = []
URL = 'https://ipinfo.io/json'


def test_proxies():
    while Q.not_empty:
        start = dt.datetime.now()
        proxy = Q.get()
        try:
            r = requests.get(URL, proxies={'http': proxy, 'https': proxy})
        except Exception as exp:
            end = dt.datetime.now()
            print(f'{end.strftime("%H:%M:%S")}: [FAILED in {end - start}] {proxy}')
            continue

        if r.status_code == 200:
            VALID_PROXIES.append(proxy)
        end = dt.datetime.now()
        print(f'{end.strftime("%H:%M:%S")}: [CLEARED in {end-start}] {proxy}')


if __name__ == '__main__':
    with open('proxies.txt', 'r') as f:
        proxy_list = f.read().split('\n')
        f.close()

    for proxy in proxy_list:
        Q.put(proxy)

    threads = [Thread(target=test_proxies) for _ in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    with open('tested_proxies.txt', 'w') as f:
        f.write('\n'.join(VALID_PROXIES))
        f.close()
