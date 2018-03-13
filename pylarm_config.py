musicfile = "/path/to/alarm.mp3"    # musicfile for the alarm
host = ''                           # hostname or IP to bind
port = 25276                        # port for the service
token = b'_token123456'             # token (in binary!)
tijdAan = 7                         # hour to start alarms
tijdUit = 10                        # last hour for alarms
dagAan = 0                          # first day of alarms
dagUit = 4                          # last dat of alarms
# In this configurations, alarms may be initiated from 7.00 AM to 10.59 AM,
# from monday till friday.
