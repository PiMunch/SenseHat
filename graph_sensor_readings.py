import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import ScalarFormatter
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()
pressure_list = []
temp_list = []
humidity_list = []
x = []
a = 0

#SET-UP GRAPH
plt.ion()
fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(12,8), sharex=True, sharey=False)

#TITLES
fig.suptitle('Sensor Readings', fontsize='x-large')
#ax1.set_title('Pressure', fontsize='medium')
#ax2.set_title('Temperature', fontsize='medium')
#ax3.set_title('Humidity', fontsize='medium')

#PRESSURE
ax1.autoscale()
ax1.grid(True)
ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax1.set_ylabel('Pressure\n(mbar)')
#ax1.set_xlabel('Time (sec)')

#TEMPERATURE
ax2.autoscale()
ax2.grid(True)
ax2.set_ylabel('Temperature\n(°C)')
#ax2.set_xlabel('Time (sec)')

#HUMIDITY
ax3.autoscale()
ax3.grid(True)
ax3.set_ylabel('Humidity\n(%)')
ax3.set_xlabel('Time (sec)')

fig.subplots_adjust(wspace=0.7, hspace=0.3)
fig.canvas.draw()

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

while True:
    pressure = sense.get_pressure()
    pressure_list.append(pressure)
    
    # attempt to calculate ambient temperature
    # based on dgaust in https://www.raspberrypi.org/forums/viewtopic.php?f=104&t=111457
    cpuTemp=int(float(getCPUtemperature()))
    ambient = sense.get_temperature_from_pressure()
    calctemp = ambient - ((cpuTemp - ambient) / 1.5)
    temp_list.append(calctemp)

    humidity = sense.get_humidity()
    humidity_list.append(humidity)

    print(a, pressure, calctemp, humidity)
    print(x)
    print(pressure_list)

    x.append(a)
    a = a + 1
    sleep(1)
    
    if len(pressure_list) > 15 and len(temp_list) > 15 and len(humidity_list) > 15:
        pressure_list.pop(0)
        temp_list.pop(0)
        humidity_list.pop(0)
        x.pop(0)

    ax1.plot(x, pressure_list, color='red')
    ax2.plot(x, temp_list, color='green')
    ax3.plot(x, humidity_list, color='blue')
    
    fig.canvas.draw()