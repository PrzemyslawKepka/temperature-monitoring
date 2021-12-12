from w1thermsensor import W1ThermSensor
from influxdb import InfluxDBClient
from datetime import datetime
import time


client = InfluxDBClient(host='localhost', port=8086, database ='temperature_db')
client.create_database('temperature_db')
client.switch_database('temperature_db')

temp_batch = []
counter = 1
while True:
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
            current_sens = 'fridge_bottom' if sensor.id == '00000b931515' else 'freezer_top'
            print(f"{counter} | {current_sens} | {datetime.now()} | {sensor.get_temperature()}")
            current_data = {
                "measurement": "temperature",
                "tags": {"sensor": current_sens},
                "time": datetime.utcnow(),
                "fields": {"temperature": sensor.get_temperature()}
                }
            temp_batch.append(current_data)
            counter += 1
            time.sleep(1)
            if counter % 10 == 0:
                client.write_points(temp_batch, time_precision='ms')
                print(f'{datetime.now()} | data sent to DB successfully')
                temp_batch.clear()
    except Exception as e:
        print(e)
        client.write_points(temp_batch, time_precision='ms')
