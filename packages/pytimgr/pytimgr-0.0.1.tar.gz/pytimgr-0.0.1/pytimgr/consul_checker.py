import asyncio
import consul.aio

class ConsulChecker:
  def __init__(self):
    self.loop = asyncio.get_event_loop()
    self.c = c = consul.aio.Consul(consistency='consistent', host="127.0.0.1", port=8500, loop=self.loop)

  def check():
    @asyncio.coroutine
    def checker():
      services = yield from self.c.agent.services()
      if services['consul']:
        print("Found Consul!")
      else:
        print("Did not find Consul!")
    # Git'er done, champ!
    loop.run_until_complete(checker())