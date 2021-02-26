import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_logDir = Path(__file__).parent.parent.absolute() / 'logs'

if not _logDir.exists():
    _logDir.mkdir(parents=True)

VerifyLogger = logging.getLogger("verify")

_consoleHandler = logging.StreamHandler()
_fileHandler = TimedRotatingFileHandler(
    _logDir / 'verify_server.log', when='D', backupCount=7
)

_formater = logging.Formatter(
    '%(asctime)s-%(levelname)s-%(funcName)s: %(message)s'
)

_consoleHandler.setFormatter(_formater)
_fileHandler.setFormatter(_formater)

VerifyLogger.addHandler(_consoleHandler)
VerifyLogger.addHandler(_fileHandler)

VerifyLogger.setLevel(logging.INFO)
VerifyLogger.setLevel(logging.DEBUG)
