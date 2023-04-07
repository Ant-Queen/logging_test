import os
import time
import logging
import logging.handlers
import multiprocessing
import threading
 
def GetParentDirectory(filePath):
    return os.path.sep.join(filePath.split(os.path.sep)[:-1])
 
def Mkdirs(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
 
def CreateLogger(loggerName):
    # Create Logger
    logger = logging.getLogger(loggerName)
    if len(logger.handlers) > 0:
        return logger
 
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
 
    # Create Handlers
    logPath = os.path.join(os.path.realpath(""), "logs", loggerName + ".log")
    Mkdirs(GetParentDirectory(logPath))
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    rotatingHandler = logging.handlers.TimedRotatingFileHandler(logPath, when='M', backupCount=10)
    rotatingHandler.setLevel(logging.DEBUG)
    rotatingHandler.setFormatter(formatter)
 
    # Add handlers to logger
    logger.addHandler(streamHandler)
    logger.addHandler(rotatingHandler)
    return logger
 
def LoggingTest(pid):
    subLogger = CreateLogger("Process_%d" % (pid))
    count = 0
    while True:
        subLogger.info("Log : 0x%08x" % count)
        time.sleep(5)
        count += 1
 
def main():
    PROC_COUNT = 10
    mainLogger = CreateLogger("Main-Process")
 
    mainLogger.info("Start Creating Process")
    procList = []
    for i in range(PROC_COUNT):
        procList.append(threading.Thread(target=LoggingTest, args=(i,)))
        procList[i].start()
        time.sleep(0.5)
    mainLogger.info("End Creating Process")
 
    count = 0
    while True:
        mainLogger.info("Main-Log : 0x%08x" % count)
        time.sleep(5)
        count += 1
 
if __name__ == '__main__':
    main()
