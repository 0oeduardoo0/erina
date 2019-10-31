#!/bin/bash

if [ "$1" = "status" ]; then
   x=$(pgrep -f 'python bot.py')
   if [ "$x" = "" ]; then
      echo "bot running... FAIL"
   else
      echo "bot running at PID $x"
      ps -fea | grep bot.py
   fi

   wget -q --spider http://google.com

   if [ $? -eq 0 ]; then
       echo "internet connection... \t\t\tOK"
   else
       echo "internet connection... \t\t\tFAIL"
   fi
fi

if [ "$1" = "stop" -o "$1" = "restart" ]; then
   echo "stoping bot service..."
   kill -9 $(pgrep -f 'python bot.py') &> /dev/null
fi

if [ "$1" = "start" -o "$1" = "restart" ]; then
   echo "starting bot service..."
   python bot.py &
fi

if [ "$1" = "cron" ]; then

   c=$(cat _data/logs/cronjob.log)

   exec 3>&1 4>&2
   trap 'exec 2>&4 1>&3' 0 1 2 3
   exec 1>_data/logs/cronjob.log 2>&1

   echo "$c"
   echo "\n\nrunning cron-job at $(date)"

   wget -q --spider http://google.com

   if [ $? -eq 0 ]; then
       echo "internet connection... \t\t\tOK"

       x=$(pgrep -f 'python bot.py')

       if [ "$x" = "" ]; then
          echo "bot service... \t\t\tFAIL"
          echo "trying to restart bot service..."
          python bot.py &
       else
          echo "bot service... \t\t\t\tOK"
       fi

   else
       echo "internet connection... \t\t\tFAIL"
       kill -9 $(pgrep -f 'python bot.py') &> /dev/null
   fi

   python cronjob.py
fi
