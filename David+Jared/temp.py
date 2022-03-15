import time
def timer():
   now = time.localtime(time.time())
   return now[5]


run = input("Start? > ")
minutes = 0
while run == "start":
   current_sec = timer()
   #print current_sec
   if current_sec == 59:
      minutes = minutes + 1
      print(">>>>>>>>>>>>>>>>>>>>>", minutes)