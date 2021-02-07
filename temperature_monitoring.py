from w1thermsensor import W1ThermSensor
import time
from datetime import datetime, timedelta
import string,random
import pandas as pd
import matplotlib.pyplot as plt
import smtplib


def generate_files():
    '''This function creates dataframe from ingested data and transforms it,
        at the end graph is generated and files are exported.
    '''
    df = pd.DataFrame(list(zip(sensor_name,current_time_list,temp_list)), columns = ['sensor', 'time','temperature'])
    df['time'] = pd.to_datetime(df['time'])
    pivot_to_plot = df.pivot(index='time', columns='sensor', values='temperature')
    pivot_to_plot.loc[:,'freezer_top'] = pivot_to_plot.loc[:,'freezer_top'].ffill()
    pivot_to_plot.loc[:,'fridge_bottom'] = pivot_to_plot.loc[:,'fridge_bottom'].bfill()
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    title = 'Temperature from ' + str(df['time'].astype('datetime64[s]').min()) + ' to ' + str(df['time'].astype('datetime64[s]').max())
    pivot_to_plot.plot(title=title ).get_figure().savefig('temperature_plot_' + dt_string + '.png')
    df.to_csv('temperature data_' + dt_string + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '.csv')
    print(dt_string, " : export to df and CSV done!")

def send_email(subject,body,sensor):
    '''Function for sending e-mails, is returned in two separate functions for sending different messages.
        Accepts arguments with defined body and subject,as well as name of the sensor for which the message is triggered.
        Google SMTP is used to send the e-mail, hence account with valid access is necessary. Google allows to generate
        special password only for this purpose (without giving access to the whole account),
        so only in this example it's just passed directly in the code.
    '''
    email_address = ''
    password = ''
    email_text = f'Subject: {subject}\n\n{body}'
    recipient = ''
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email_address, password)
        server.sendmail(email_address, recipient, email_text.encode("utf8"))
        server.close()
        print(f'{sensor} - email sent!')
    except:
        print(f'{sensor} - email was not sent!')

def temperature_too_high(current_temperature, current_sens):
    '''If temperature for one of the sensors is too high, this function is invoked to generate an e-mail notification.
        Temperatute and sensor name are passed as an arguments, and they are used to generate content of the e-mail.
    '''
    sensor = 'Fridge' if current_sens == 'fridge_bottom' else 'Freezer'
    subject = f'{sensor} temperature is too high! - {round(current_temperature,2)}\u00B0C'
    body = f'Hi,\n\nPlease check the {sensor.lower()}, temperature is too high right now!'
    return send_email(subject,body,sensor)

def script_down(current_sens):
    '''If script suddenly stops working, which might be due to sensors not being properly connected,
        this function is invoked to generate an e-mail notification.
    '''
    sensor = 'fridge' if current_sens == 'fridge_bottom' else 'freezer'
    subject = 'Script for measuring the temperature is down!'
    body = f"Hi,\n\nScript is no longer running, it has stopped while trying to get the temperature for {sensor}. Please check if sensors are properly connected to a breadboard, or if there isn't any other issue occuring."
    return send_email(subject,body,sensor)

#Creating lists to which data is appended during a loop, and these lists are used to create a dataframe 
temp_list,current_time_list,sensor_name = ([] for i in range(3))

'''To do not generate too many e-mail notifications, they can be sent only once within 6 hours.
Firstly these two variables are set to pass the condition at first occurence of too high temperature,
and then variables are updated and only after 6 hours condition will be passed.'''
fridge_notif_sent = datetime.now() - timedelta(hours=6)
freezer_notif_sent = datetime.now() - timedelta(hours=6)

'''Monitoring is set to be working all the time, hence it will stop only when obtaining the temperature won't be possible,
    and then proper notification will be sent. Data extract and a graph can be generated after particular number of occurences
    or at specific time (now set after every 10k occurences), and will be always generated if the script breaks.
'''

counter = 1
while True:
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
            current_temperature = sensor.get_temperature()
            temp_list.append(current_temperature)
            current_time = datetime.now()
            current_time_list.append(current_time)
            current_sens = 'fridge_bottom' if sensor.id == '00000b931515' else 'freezer_top'
            sensor_name.append(current_sens)
            print(f"{counter} | {current_sens} | {current_time} | {current_temperature}")
            if counter % 10000 == 0:
                generate_files()
            if current_sens == 'fridge_bottom' and current_temperature > 10 and datetime.now() > (fridge_notif_sent + timedelta(hours=6)):
                temperature_too_high(current_temperature, current_sens)
                fridge_notif_sent = datetime.now()
            if current_sens == 'freezer_top' and current_temperature > -10 and datetime.now() > (freezer_notif_sent + timedelta(hours=6)):
                temperature_too_high(current_temperature, current_sens)
                freezer_notif_sent = datetime.now()
        counter += 1
        time.sleep(1)
    except:
        #if failed then export and plot what's already gathered, also send notification message
        print(f'Script is no longer running! - stopped on {current_sens}')
        script_down(current_sens)
        generate_files()
        break
        
