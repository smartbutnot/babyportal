
import board
import displayio
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from digitalio import DigitalInOut
import busio
import neopixel
import rgbmatrix
import framebufferio
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from digitalio import DigitalInOut
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import graphics
import json
import time

bit_depth = 6
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine = False

width = base_width * chain_across
height = base_height * tile_down

addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD]
rgb_pins = [
    board.MTX_R1,
    board.MTX_G1,
    board.MTX_B1,
    board.MTX_R2,
    board.MTX_G2,
    board.MTX_B2,
]
clock_pin = board.MTX_CLK
latch_pin = board.MTX_LAT
oe_pin = board.MTX_OE

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
            width=width,
            height=height,
            bit_depth=bit_depth,
            rgb_pins=rgb_pins,
            addr_pins=addr_pins,
            clock_pin=clock_pin,
            latch_pin=latch_pin,
            output_enable_pin=oe_pin,
            tile=tile_down, serpentine=serpentine,
        )
display = framebufferio.FramebufferDisplay(matrix)

try:
    from secrets import secrets
except ImportError:
    print("Problem importing secrets.")
    raise


        
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)

wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

MQTT.set_socket(socket, esp)
mqtt = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],
    username=secrets["user"],
    password=secrets["pass"],
)

boobtotal=10

def connected(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    

def disconnected(client, userdata, rc):
    print("Disconnected from MQTT Broker!")

def message(client, topic, message):
    global boobtotal
    print("Received message: "+message)
    if message != "None":
        if(topic=='baby/wee'):
            graphics.updateDashLabel(message,0)
        elif(topic=='baby/poo'):
            graphics.updateDashLabel(message,1)
        elif(topic=='baby/pumping'):
            graphics.updateDashLabel(message,2)
        elif(topic=='baby/lastnappy'):
            graphics.updateDashLabel(message,3)
        elif(topic=='baby/lastfeed'):
            graphics.updateDashLabel(message,4)
        elif(topic=='baby/nursing'):
            boobtotal=int(message)
            graphics.updateDashLabel('{:02d}:{:02d}'.format(*divmod(boobtotal, 60)),5)
        elif(topic=='baby/nursingleft'):
            #graphics.updateDashLabel(message,6)
            boobleft=int(message)
            boobratio=int(round(((boobleft/boobtotal)*20)))
            graphics.updateGraph(boobratio)
        
    graphics.showDisplay(display)

mqtt.on_connect = connected
mqtt.on_disconnect = disconnected
mqtt.on_message = message

def reconnect():
    print("reconnect loop")
    while True:
        try:
            print("wifi reconnect...")
            wifi.reset()
            wifi.connect()
            print("mqtt reconnect...")
            mqtt.reconnect()
            print("success.")
            break
        except Exception as e:
            print("reconnect ERROR")
            print(e)
            time.sleep(5)


graphics.showDisplay(display)
wifi.connect()
mqtt.connect()

mqtt.subscribe("baby/#")


#reconnect()


while True:
    try:
        mqtt.loop()
    except Exception as e:
        print("ERROR")
        print(e)
        reconnect()
