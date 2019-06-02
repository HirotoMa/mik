import time
import threading

import ICReaderProc
import DBProc

if __name__ == "__main__":
    #from db.DBProc import DBProc
    
    thread_1 = threading.Thread(target=ICReaderProc.ICReaderProc1)
    thread_2 = threading.Thread(target=DBProc.DBProc1)

    thread_1.start()
    thread_2.start()
