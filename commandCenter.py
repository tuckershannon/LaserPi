
"""
laserPi by Tucker Shannon 2018
thingiverse 3d print files:
https://www.thingiverse.com/thing:2965798
youTube tutorial:
https://www.youtube.com/watch?v=Ll1u_rkKWxM&t=2s
"""


import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
import sys
sys.path.insert(0, '/home/pi/')
import weatherReport
import timeReport
import analogReport
import laserMessage

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = sys.argv[2]
ADAFRUIT_IO_USERNAME = sys.argv[1]  # See https://accounts.adafruit.com
                                                    # to find your username.

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'laser'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    if payload == '0':
        weatherReport.main(sys.argv[3])
    elif payload == '1':
        analogReport.main()
        print "yes"
    elif payload == '2':
        timeReport.main()
    else:
        laserMessage.main(payload)
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
while True:
    try:
        client.connect()
        break
    except:
       print('connection error')


# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()
