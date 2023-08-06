import applauncher.kernel
import inject
from sqlalchemy_bundle import EntityManager
import threading
import zope.event
from obscure_api import obscure


class Resource(object):
    @staticmethod
    def get_entity_manager():
        return inject.instance(EntityManager)

    @property
    def session(self):
        em = inject.instance(EntityManager)
        return em.s


class ObscureBundle(object):
    def __init__(self):
        self.config_mapping = {
            "obscure": {
                "port": 3003,
                "host": "0.0.0.0",
                "key": None,
                "jwt_secret": None
            }
        }

        zope.event.subscribers.append(self.kernel_ready)

    @inject.params(config=applauncher.kernel.Configuration)
    def start_sever(self, config):
        c = config.obscure
        s = obscure.Server(key=c.key, jwt_secret=c.jwt_secret)
        s.run(host=c.host, port=c.port)

    def kernel_ready(self, event):
        if isinstance(event, applauncher.kernel.KernelReadyEvent):
            t = threading.Thread(target=self.start_sever)
            t.start()