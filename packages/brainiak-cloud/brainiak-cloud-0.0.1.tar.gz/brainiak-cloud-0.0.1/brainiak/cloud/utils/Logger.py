import sys
import logging

class Logger:
    class __Logger:
        def __init__(self, **opts):
            if not 'level' in opts:
                opts['level'] = logging.INFO
            if not 'format' in opts:
                opts['format'] = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            if not 'stream' in opts:
                opts['stream'] = sys.stderr

            logging.basicConfig(**opts)
            self.logger = logging.getLogger(__name__)

    instance = None

    def __init__(self, **opts):
        if not Logger.instance:
            Logger.instance = Logger.__Logger(**opts)

    def info(self, log):
        Logger.instance.logger.info(log)

    def debug(self, log):
        Logger.instance.logger.debug(log)
