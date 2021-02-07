# Overview
Practical project allowing to monitor the temperature using Rasperry Pi 4B microcomputer and DS18B20 sensors. Here temperature in the fridge is being controlled, but it can be versatile and room temperature could be monitored for instance as well.
Sensors have to be properly connected to Raspberry Pi using breadboard, and python module `w1thermsensor` is used to retrieve the temperature registered by the sensors. Based on that, temperature can be constantly monitored, e-mail notifications can be sent when temperature is unexpectedly low/high, and saved data can be plotted on a graph.

Below hardware setup is shown with sensors located in the fridge and connected to Raspberry Pi through a breadboard.
<img src="https://github.com/PrzemyslawKepka/temperature_monitoring/blob/main/hardware_setup.jpg" alt="Raspberry Pi and breadboard setup">

This image from a generated graph is clearly showing that refrigerator is not working correctly, especially freezer with it's high amplitude.
<img src="https://github.com/PrzemyslawKepka/temperature_monitoring/blob/main/graph.jpg" alt="Graph" width="500"/>

Generated data extract and results printed in Thonny IDE are visible below.
<img src="https://github.com/PrzemyslawKepka/temperature_monitoring/blob/main/data_extract.jpg" alt="Data extract"/>

And here is an e-mail notification that was generated.
<img src="https://github.com/PrzemyslawKepka/temperature_monitoring/blob/main/email_notification.jpg" alt="E-mail notification"/>



