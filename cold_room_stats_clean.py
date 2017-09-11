import datetime
from sense_hat import SenseHat
from time import sleep
from twilio.rest import Client



sense = SenseHat()


def adjusted_temp():
    # gets the temperature from the 3 sense hat sensors
    thermometer_temp = sense.get_temperature() * 9 / 5 + 32
    pressure_temp = sense.get_temperature_from_pressure() * 9 / 5 + 32
    humidity_temp = sense.get_temperature_from_humidity() * 9 / 5 + 32
    adjusted_temp = ((thermometer_temp + pressure_temp + humidity_temp)/3)
    return adjusted_temp - adjusted_temp * .25


def pixel_setter(pixel_color, pixel_list):
    # used to create a list of rgb values for the led array
    for i in range(64):
        pixel_list.append(pixel_color)


def show_temp_number(temp_color):
    # scrolls the temperature number
    temperature = int(adjusted_temp())
    sense.show_message(text_string=str(temperature), text_colour=[0, 0, 0], back_colour=temp_color, scroll_speed=.4)


def text_alert():
    # sends the alert text using twilio
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    employee_1_phone = ''
    employee_2_phone = ''
    employee_3_phone = ''
    contact_list = [employee_1_phone, employee_2_phone, employee_3_phone]
    for contact in contact_list:
        if contact != '':
            client.messages.create(
                to=contact,
                from_='',
                body="Server room is over 80F")
    text_sent_time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    text_sent_time = datetime.datetime.strptime(text_sent_time_string, '%Y-%m-%d %H:%M')
    return text_sent_time


def led_temp():
    # reads the temp and updates the led array, calls the alert text function if temps are too high
    full_array = []
    cold = [2, 71, 254]  # blue
    warm = [255, 246, 0]  # orange
    hot = [255, 8, 0]  # red
    done = False
    current_reading = adjusted_temp()

    if current_reading < 75:
        show_temp_number(cold)
        pixel_setter(cold, full_array)
        sense.set_pixels(full_array)

    elif 75 <= current_reading < 80:
        show_temp_number(warm)
        pixel_setter(warm, full_array)
        sense.set_pixels(full_array)

    elif current_reading >= 80:
        show_temp_number(hot)
        pixel_setter(hot, full_array)
        time_sent_alert = text_alert()
        thirty_min_wait = datetime.timedelta(minutes=30)
        sense.set_pixels(full_array)
        while not done:
            # delays everything 30 minutes from the time an alert text was sent to prevent too many texts being sent out
            current_time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            current_time = datetime.datetime.strptime(current_time_string, '%Y-%m-%d %H:%M')
            if current_time < time_sent_alert + thirty_min_wait:
                show_temp_number(hot)
                sleep(60)
            elif current_time >= time_sent_alert + thirty_min_wait:
                done = True


while True:
    led_temp()
    sleep(60)
