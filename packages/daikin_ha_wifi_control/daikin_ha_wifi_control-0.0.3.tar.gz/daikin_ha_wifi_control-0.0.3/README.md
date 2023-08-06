# daikin_ha_wifi_control
Control Daikin Air Conditioners/Air Purifiers from within your LAN.

If you're already able to control your Daikin AC or air purifier using the DaikinAPP (not the SkiFi app), this interface should work well with your AC/AP. Tested with BRP072A44 adapter, and MCK70U air purifier.

Example of instantiation

  ```
  from DaikinInterface import DaikinAirConditioner

  aircon = DaikinAirConditioner("192.168.0.151")
  aircon.switch()
  aircon.setMode(4)
  aircon.setTemp(28)
  ```

#### AC Modes

|Code|Mode|
|:---:|:---:|
|0/1/7|Auto|
|2|Dry|
|3|Cool|
|4|Heat|
|6|Fan|

#### AP Modes

|Code|Mode|Humidity|AirVol|
|:---:|:---:|:---:|:---:|
|0|AutoFan|Off|AutoFan|
|1|Smart|Low|Quiet|
|2|Econo|Mid|Low|
|3|Pollen|High|Standard|
|4|Moist|X|X|
|5|Ciculator|X|Turbo|