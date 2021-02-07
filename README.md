# Overview
Practical project allowing to monitor the temperature using Rasperry Pi microcomputer and DS18B20 sensors. Here temperature in the fridge is being controlled, but it can be versatile and room temperature could be monitored for instance as well.
Sensors have to be properly connected to Raspberry Pi using breadboard, and python module `w1thermsensor` is used to retrieve the temperature registered by the sensors. Based on that, temperature can be constantly monitored, e-mail notifications can be sent when temperature is unexpectedly low/high, and saved data can be plotted on a graph.


<img src="https://github.com/PrzemyslawKepka/temperature_monitoring/blob/main/hardware.jpg" alt="Raspberry Pi and breadboard setup" width="500"/>

