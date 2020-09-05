import logging

import container_manager
import webapp

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

container_manager.prepare()
webapp.run()
