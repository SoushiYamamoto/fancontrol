cd /
rm f /cron_fan
rm f /etc/cron.d/cron_fan
rm f /fan.py
wget https://github.com/SoushiYamamoto/fancontrol/blob/main/cron_fan
wget https://github.com/SoushiYamamoto/fancontrol/blob/main/fan.py
mv /cron_fan /etc/cron.d/
service cron restart