from __future__ import with_statement
#from sys import platform as _platform
from ast import literal_eval
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import LoggingEventHandler 

import watchdog
import psutil
import datetime
import time
import sys
import time
import logging
#import os
#import webbrowser






def main():
 while 1:
  try:
    OP = input("\nWhich mode would you like to open?\n Press M for monitor mode\n Press H for manual mode\n Press Q to quit\n For this main menu press Ctrl+C after entering input.\n\n After quitting the tool (pressing Q) you will be transferred to a file protection mechanism - please press Ctrl+c twice to exit all\n")
    if OP=='Q':
        break
    if OP == 'M':
        monitorMode()
    elif OP == 'H':
        while 1:
         try:
          date1 = input("\nPlease enter first date to sample by this pattern:  YYYY-DY-MM (HH:MM:SS)\n While MON is a three letters word, starting with capital letter and HH is hours in 24 hours display\n")
          date2 = input("\nPlease enter second date to sample by this pattern:  YYYY-DY-MM (HH:MM:SS)\n While MON is a three letters word, starting with capital letter and HH is hours in 24 hours display\n")
          datetime.datetime.strptime(date1, "%Y-%d-%b (%H:%M:%S)")
          datetime.datetime.strptime(date2, "%Y-%d-%b (%H:%M:%S)")
          break
         except (ValueError):
                continue
         except (KeyboardInterrupt):
               break
               main()
        manualMode(date1, date2)
  except (KeyboardInterrupt, EOFError):
            break
            print("\nYou are already in main menu")

            main()
            break
  #print("\nYou are already in main menu")
 # break





def getFromDict(s):
    date = literal_eval(s)
    key = next(iter(date.keys()))
    val = next(iter(date.values()))
    return {datetime.datetime.strptime(key, "%Y-%d-%b (%H:%M:%S)"): val}

def diff(start, end):
    diff = []
    try:
     oldList = next(iter(start.values()))
     newList = next(iter(end.values()))
    except:
        return []
    for proc in oldList:
        if proc not in newList:
            diff.append(str(oldList[proc])+ " is no longer running")
    for proc in newList:
        if proc not in oldList:
            diff.append(str(newList[proc])+ " was created")
    return diff

def writeDiff(diff):
    f=open('Status_Log.txt', 'a')
    for line in diff:
        f.write(line+"\n")
    f.close()

def services():
    procList={}
    for proc in psutil.process_iter():
        processName = proc.name()
        processID = proc.pid
        procList.update({processID: processName})
    return procList


def writeServices(procList):
    f=open("serviceList.txt","a")
    f.write(str(procList)+"\n")
    f.close()


def monitorMode():
    while 1:
     try:
      x = int(input("How often whould you like to sample running services (in seconds)?\n"))
      break
     except:
      continue
    count=0
    while 1:
     try:
      d = datetime.datetime.now()
      date = d.strftime("%Y-%d-%b (%H:%M:%S)")
      proc=services()
      thisProc={date:proc}
      writeServices(thisProc)
      if count==0:
         count+=1
      else:
         differ=diff(prev,thisProc)
         for l in differ:
             print(l)
         writeDiff(differ)
      prev=thisProc
      time.sleep(x)
     except (KeyboardInterrupt):
         break
         main()


def manualMode(date1,date2):
  try:
   lines=[]
   date1sample={}
   date2sample={}
   with open('serviceList.txt','r') as file:
    log = file.readline()
    prevS = getFromDict(log)
    prevT = next(iter(prevS.keys()))
    log = file.readline()
    s = getFromDict(log)
    curr = next(iter(s.keys()))
    start=datetime.datetime.strptime(date1,"%Y-%d-%b (%H:%M:%S)")
    end=datetime.datetime.strptime(date2,"%Y-%d-%b (%H:%M:%S)")
    while log:
       if prevT <= start <= curr:
           date1sample = prevS
       if prevT <= end <= curr:
           date2sample = s
       prevS = s
       prevT = curr
       log = file.readline()
       if log:
           s = getFromDict(log)
           curr = next(iter(s.keys()))
    diff_list = diff(date1sample, date2sample)
    if diff_list==[]:
        print("\nNo differences or no match for these dates, please try again")
    else:
     differ='\n'.join(diff_list)
     print (differ)
  except (KeyboardInterrupt):
      main()


main()



if __name__ == "__main__":
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Set format for displaying path
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # Initialize logging event handler
    event_handler = LoggingEventHandler()

    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        observer.stop()
    observer.join()



