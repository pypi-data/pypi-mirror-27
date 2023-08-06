__version__ = '1.0.0'
__author__ = 'instome'
__license__ = 'MIT'

__all__ = ["WeAppRobot"]

try:
    from weapprobot.robot import WeAppRobot
except ImportError:  # pragma: no cover
    pass  # pragma: no cover
