cd /
rm f /cron_fan
rm f /etc/cron.d/cron_fan
rm f /fan.py
wget https://raw.githubusercontent.com/SoushiYamamoto/fancontrol/main/cron_fan
wget https://raw.githubusercontent.com/SoushiYamamoto/fancontrol/main/fan.py
mv /cron_fan /etc/cron.d/
service cron restart
