import requests
import urllib.parse
from abc import ABCMeta, abstractmethod

class DaikinDevice(object):

    def __init__(self,ip_addr):
        self.ip_addr = ip_addr
        self.readBasicInfo()
    
    @property
    @abstractmethod
    def type(self):
        pass
    
    def readBasicInfo(self):
        endpoint = "/common/basic_info"
        res = DaikinWifiRequest(self.ip_addr, endpoint).send()
        if res.get("ret") == "OK":
            self.name = res.get("name")
            self.power_stat = int(res.get("pow"))
            self.mac_addr = res.get("mac")
            self.led_stat = int(res.get("led"))
            
    def rebootAp(self):
        endpoint = "/common/reboot"
        DaikinWifiRequest(self.ip_addr, endpoint).send()
        
    def switchLed(self, to=None):
        endpoint = "/common/set_led"
        self.readBasicInfo()
        if to:
            led = to
        else:
            led = ~self.led_stat+2
        params = {"led":led}
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readBasicInfo()

class DaikinAirConditioner(DaikinDevice):
    
    type = "aircon"
    
    def __init__(self, *args, **kwargs):
        super(DaikinAirConditioner, self).__init__(*args, **kwargs)
        self.readControlInfo()
        self.readSensor()
        
    def setParam(self, key, value):
        self.readControlInfo()
        params = {
                "pow": self.power_stat,
                "mode":self.mode_set,
                "stemp":self.temp_set,
                "shum":self.humidity_set
                }
        params[key] = value
        return params
        
    def readStatus(self):
        self.readControlInfo()
        self.readSensor()
        stats = {
                "pow": self.power_stat,
                "mode":self.mode_set,
                "stemp":self.temp_set,
                "shum":self.humidity_set,
                "htemp":self.room_temp,
                "otemp":self.outside_temp
        }
        return stats
    
    def switch(self, to=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        if to:
            pow = to
        else:
            pow = ~self.power_stat+2
        params = self.setParam("pow", pow)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()
        
    def setMode(self, mode=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        print(self.mode_set)
        if mode in range(0, 8):
            smode = mode
        else:
            smode = (int(self.mode_set)+1) % 8
        params = self.setParam("mode",smode)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()
        print(self.mode_set)
        
    def setTemp(self, temp):
        endpoint = "/%s/set_control_info" % self.type
        params = self.setParam("stemp",temp)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()
    
    def readSensor(self):
        endpoint = "/%s/get_sensor_info" % self.type
        res = DaikinWifiRequest(self.ip_addr, endpoint).send()
        if res.get("ret") == "OK":
            self.room_temp = float(res.get("htemp"))
            self.outside_temp = float(res.get("otemp"))
    
    def readControlInfo(self):
        endpoint = "/%s/get_control_info" % self.type
        res = DaikinWifiRequest(self.ip_addr, endpoint).send()
        if res.get("ret") == "OK":
            self.mode_set = res.get("mode")
            try:
                self.temp_set = float(res.get("stemp"))
            except ValueError as e:
                self.temp_set = res.get("stemp")
            self.humidity_set = int(res.get("shum"))
            self.power_stat = int(res.get("pow"))

class DaikinAirPurifier(DaikinDevice):
    
    type = "cleaner"
    
    def __init__(self, *args, **kwargs):
        super(DaikinAirPurifier, self).__init__(*args, **kwargs)
        self.readControlInfo()
        self.readSensor()

    def readStatus(self):
        self.readControlInfo()
        self.readSensor()
        stats = {
                "pow": self.power_stat,
                "mode":self.mode_set,
                "airvol":self.airvol_set,
                "humd":self.humidity_set,
                "htemp":self.room_temp,
                "hhum":self.room_humidity,
                "pm25":self.room_pm2_5_lvl,
                "dust":self.room_dust_lvl,
                "odor":self.room_odor_lvl
        }
        return stats

    def setParam(self, key, value):
        self.readControlInfo()
        params = {
                "pow": self.power_stat,
                "mode":self.mode_set,
                "airvol":self.airvol_set,
                "humd":self.humidity_set
                }
        params[key] = value
        return params

    def switch(self, to=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        if to:
            pow = to
        else:
            pow = ~self.power_stat+2
        params = self.setParam("pow",pow)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()
        
    def setMode(self, mode=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        if mode in range(0, 6):
            smode = mode
        else:
            smode = (int(self.mode_set)+1) % 6
        params = self.setParam("mode",smode)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()
        
    def setAirVol(self, airvol=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        if airvol in range(0, 5):
            sairvol = airvol
        else:
            sairvol=(int(self.airvol_set)+1) % 6
        if sairvol == 4:
            sairvol = 5
        params = self.setParam("airvol",sairvol)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()

    def setHumidity(self, humd=None):
        endpoint = "/%s/set_control_info" % self.type
        self.readControlInfo()
        if humd in range(0, 5):
            shumd = humd
        else:
            shumd = (int(self.humidity_set+1)) % 5
        params = self.setParam("humd",shumd)
        res = DaikinWifiRequest(self.ip_addr, endpoint, params).send()
        self.readControlInfo()

    def readControlInfo(self):
        endpoint = "/%s/get_control_info" % self.type
        res = DaikinWifiRequest(self.ip_addr, endpoint).send()
        if res.get("ret") == "OK":
            self.mode_set = res.get("mode")
            self.airvol_set = int(res.get("airvol"))
            self.humidity_set = int(res.get("humd"))
            self.power_stat = int(res.get("pow"))
        
    def readSensor(self):
        endpoint = "/%s/get_sensor_info" % self.type
        res = DaikinWifiRequest(self.ip_addr, endpoint).send()
        if res.get("ret") == "OK":
            self.room_temp = float(res.get("htemp"))
            self.room_humidity = int(res.get("hhum"))
            self.room_pm2_5_lvl = int(res.get("pm25"))
            self.room_dust_lvl = int(res.get("dust"))
            self.room_odor_lvl = int(res.get("odor"))

class DaikinWifiRequest:
    
    def __init__(self, ip_addr, endpoint, params=None):
        self.url = "http://%s%s" % (ip_addr,endpoint)
        self.params = params
    
    def send(self):
        res = requests.get(self.url, params=self.params).text
        res = urllib.parse.unquote(res)
        return dict(u.split("=") for u in res.split(","))