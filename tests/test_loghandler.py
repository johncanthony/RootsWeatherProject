from LogHandler.logHandler import LogHandler
import logging as log
from logging.handlers import TimedRotatingFileHandler
import unittest


class TestLogHandler(unittest.TestCase):
    def test_logHandler(self):
        # Create an instance of LogHandler

        log_handler = LogHandler(service_name='test')
        log_handler.bootstrap()

        # Assert Default getenv() values are set
        self.assertEqual(log_handler.service_name, 'test')
        self.assertEqual(log_handler.dir, './')

        # Assert the appropriate default level and log file name are set
        self.assertEqual(log.getLogger().level, log.INFO)
        testLogHandler = [handler.baseFilename for handler in log.getLogger().handlers if isinstance(handler, TimedRotatingFileHandler)]
        self.assertIn('test-service.log', testLogHandler[0])


if __name__ == '__main__':
    unittest.main()
