@echo off
echo Stopping any background instances...
python kill_switch.py
echo.
echo Starting Apple Music RPC in DEBUG mode...
echo Keep this window OPEN. You should see "Now Playing" messages.
echo If it stops working, take a screenshot or copy the text here!
echo.
python main.py
pause
