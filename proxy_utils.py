import async_requests


TIMEOUT = 10


# TODO: add multiple checks with several sites
async def check_proxy(proxy):
    try:
        res = await async_requests.get(
            'https://pikagraphs.d3d.info/OK/',
            proxy=proxy.to_url(),
            timeout=TIMEOUT,
            headers={'User-Agent': get_random_user_agent()},
        )
        if res.status == 200 and res.text == "OK":
            return True
    except Exception:
        return False
    return False


# method gets proxy in any of the supported formats
# and return proxy protocols
# supported raw proxy formats:
# ip:port
# domain:port
# user:pass@ip:port
# user:pass@domain:port
async def detect_raw_proxy_protocols(raw_proxy):
    result = []

    protocols = ['http', 'socks5', 'socks4']

    for protocol in protocols:
        # TODO: add other test sites
        try:
            res = await async_requests.get(
                'https://pikagraphs.d3d.info/OK/',
                proxy="{}://{}".format(protocol, raw_proxy),
                timeout=TIMEOUT,
                headers={'User-Agent': get_random_user_agent()},
            )

            if res.status == 200 and res.text == "OK":
                result.append(protocol)

        except Exception as ex:
            pass

    return result


def get_random_user_agent():
    # TODO: do it
    return 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'
