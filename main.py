#!/usr/bin/env python3

# TODO: fix socks proxies

import asyncio
import init_django # @TODO: fix this shit

from proxy_py import settings
from processor import Processor
from server.proxy_provider_server import ProxyProviderServer
from program_killer import ProgrammKiller
import collectors_list

proxies = []

killer = ProgrammKiller()

# TODO: fix closing of program when it's waiting for finish coroutines
if __name__ == "__main__":
    proxy_processor = Processor()
    for CollectorType in collectors_list.collectorTypes:
        proxy_processor.add_collector_of_type(CollectorType)

    proxy_provider_server = ProxyProviderServer.get_proxy_provider_server(
        settings.PROXY_PROVIDER_SERVER_ADDRESS['HOST'],
        settings.PROXY_PROVIDER_SERVER_ADDRESS['PORT'],
        proxy_processor,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(proxy_provider_server.start(loop))

    try:
        loop.run_until_complete(proxy_processor.exec(killer, loop))
        # proxy_processor.exec(killer, loop)
    except Exception as ex:
        print("Some shit happened: {}".format(ex))
