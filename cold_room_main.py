from cold_room import ColdRoom
import datetime
from time import sleep


cold_cat = ColdRoom()


while True:
    # checks time and logs according to time of day
    now = datetime.datetime.time(datetime.datetime.now())

    # updates the weekly and monthly logs at midnight
    if datetime.time(hour=0, minute=0) < now < datetime.time(hour=0, minute=1, second=30):
        cold_cat.log_temps(cold_cat.temps_7_days, cold_cat.show_avg_temps(cold_cat.temps_24_hrs))
        cold_cat.log_temps(cold_cat.temps_30_days, cold_cat.show_avg_temps(cold_cat.temps_7_days))
        cold_cat.write_temps('logged_temps.xlsx')

    # updates the daily log every half hour
    elif now.minute == 0 or now.minute == 30:
        cold_cat.log_temps(cold_cat.temps_24_hrs, cold_cat.adjusted_temp())
        cold_cat.write_temps('logged_temps.xlsx')

    else:
        pass

    # proceeds with the temp readout and display actions then waits
    cold_cat.led_temp()
    sleep(60)
