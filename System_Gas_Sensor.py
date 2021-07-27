from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
from utime import sleep
import network, time, urequests

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect('SOUS', 'S@rit@282230.')         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True


sensorG = ADC(Pin(39))
sensorG.width(ADC.WIDTH_10BIT)
sensorG.atten(ADC.ATTN_11DB)
file = open("test.txt", "w")

ancho = 128
alto = 64

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
led_onboard = Pin(4, Pin.OUT)
led_onboard2 = Pin(2, Pin.OUT)

if conectaWifi ("nombre", "clave"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    url = "https://maker.ifttt.com/trigger/sensorGas/with/key/dd7ijFVTN282jwqL3Tc9o?"
    url2 = "https://maker.ifttt.com/trigger/alarm_1/with/key/dd7ijFVTN282jwqL3Tc9o?"
    url3 = "https://maker.ifttt.com/trigger/alarm_2/with/key/dd7ijFVTN282jwqL3Tc9o?"

print(i2c.scan())
 
oled.text('Welcome to the', 0, 0)
oled.text('Areandina', 0, 10)
oled.text('Methane Gas', 0, 20)
oled.text('Level Control', 0, 30)
oled.show()
sleep(2)
 

while True:
        
        sleep(2)
        lectura = sensorG.read()
        file.write(str( "Gas level =  {} % ".format(lectura)))
        file.flush()
        oled.fill(0)
        oled.text("Gas level: ",0,10)
        oled.text(str(lectura),0,20)
        oled.show()
    
        print("Gas level: ",lectura)
        sleep(0.25)
        if(lectura > 700):
            #Alarma de gas con luz
            led_onboard.value(1) #Prende o apaga
            led_onboard2.value(0)
            respuesta = urequests.get(url+"&value1="+str(lectura))
            print(respuesta.text)
            print (respuesta.status_code)
            respuesta.close ()
            time.sleep (12)
            respuesta2 = urequests.get(url2+"&value1="+str(lectura))
            print(respuesta2.text)
            print (respuesta2.status_code)
            respuesta2.close ()
            time.sleep (12)
            respuesta3 = urequests.get(url3+"&value1="+str(lectura))
            print(respuesta3.text)
            print (respuesta3.status_code)
            respuesta3.close ()
            time.sleep (12)
            
            
        else:
            led_onboard.value(0)
            led_onboard2.value(1) #prende o apaga
            respuesta = urequests.get(url+"&value1="+str(lectura))
            print(respuesta.text)
            print (respuesta.status_code)
            respuesta.close ()
            time.sleep (12)
 
  
    
   
 
else:
       print ("Imposible conectar")
       miRed.active (False)
       
      
 

