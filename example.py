# Example usage
from logger_Davo import *

logger = Logger(min_log_level=LogLevel.INFO)

logger.log("This is a debug message.", LogLevel.DEBUG)
print("this message is printed on main thread, it doesn't wait for the logger thread to finish")
logger.log("This is an info message.", LogLevel.INFO)
print("this message is printed on main thread, it doesn't wait for the logger thread to finish")
logger.log("This is a warning message.", LogLevel.WARNING)
print("this message is printed on main thread, it doesn't wait for the logger thread to finish")
logger.log("This is an error message.", LogLevel.ERROR)
print("this message is printed on main thread, it doesn't wait for the logger thread to finish")

