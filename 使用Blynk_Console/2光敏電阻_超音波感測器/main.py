BLYNK_AUTH_TOKEN = "自已的token"

from tools import connect,reconnect
import urequests as requests
from machine import Pin,ADC,Timer
import utime

adc_light = ADC(Pin(28))
trigger = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)
connect()

def ultra()->float:      #建立一個函式
   utime.sleep_us(2)  #暫停兩微秒，確保上一個設定低電位已經完成
   trigger.high()
   utime.sleep_us(10)  #拉高電位後，等待10微秒後，立即設定為低電位
   trigger.low()    
   while echo.value() == 0:         #建立一個while迴圈檢查回波引腳是否值為0，紀錄當時時間
       signaloff = utime.ticks_us()   
   while echo.value() == 1:         #建立一個while迴圈檢查回波引腳是否值為1，紀錄當時時間
       signalon = utime.ticks_us()  
   timepassed = signalon - signaloff    #計算發送與接收時間差
   distance = (timepassed * 0.0343) / 2  #聲波行進時間 x 聲速(343.2 m/s，即每微秒0.0343公分)，來回距離再除以2  
   return distance
   
def lightSensor()->float:
    light_value = adc_light.read_u16()
    return light_value


   
def callback1(t:Timer):
    distance = ultra()
    light_value = lightSensor()
    
    #不要使用https呼叫,沒有傳出值
    #更新V0->distance
    #更新V1->light
    print(distance)
    print(light_value)
    
    url = f'https://blynk.cloud/external/api/batch/update?token={BLYNK_AUTH_TOKEN}&v0={distance}&v1={light_value}'
    try:        
        response = requests.get(url)
        print("text")
        print("送出資料")
    except:
        reconnect()
    else:
        print("server接收") #但要檢查status_code,是否回應成功        
        if response.status_code == 200:
            print("成功傳送,status_code==200")
        else:
            print("server回應有問題")
            print(f'status_code:{response.status_code}')
           
        
        response.close()
        
time1 = Timer()
time1.init(period=5000,callback=callback1)