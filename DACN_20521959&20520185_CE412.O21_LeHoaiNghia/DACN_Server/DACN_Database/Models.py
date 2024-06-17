import datetime
import time
import os
from pymongo import MongoClient
import paho.mqtt.client as paho

# MongoDB connection URI
uri = "mongodb+srv://antgroup0905:0905168232@cluster0.jph72eg.mongodb.net/test?retryWrites=true&w=majority"

# MQTT broker configuration
broker_address = "cf9e09b172424224953dd48c7c8c2a7e.s1.eu.hivemq.cloud"
broker_port = 8883
mqtt_username = "WaterMonitoring"
mqtt_password = "12345678Ab"

# Root CA certificate
root_ca = """
-----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIRAIIQz7DSQONZRGPgu2OCiwAwDQYJKoZIhvcNAQELBQAw
TzELMAkGA1UEBhMCVVMxKTAnBgNVBAoTIEludGVybmV0IFNlY3VyaXR5IFJlc2Vh
cmNoIEdyb3VwMRUwEwYDVQQDEwxJU1JHIFJvb3QgWDEwHhcNMTUwNjA0MTEwNDM4
WhcNMzUwNjA0MTEwNDM4WjBPMQswCQYDVQQGEwJVUzEpMCcGA1UEChMgSW50ZXJu
ZXQgU2VjdXJpdHkgUmVzZWFyY2ggR3JvdXAxFTATBgNVBAMTDElTUkcgUm9vdCBY
MTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAK3oJHP0FDfzm54rVygc
h77ct984kIxuPOZXoHj3dcKi/vVqbvYATyjb3miGbESTtrFj/RQSa78f0uoxmyF+
0TM8ukj13Xnfs7j/EvEhmkvBioZxaUpmZmyPfjxwv60pIgbz5MDmgK7iS4+3mX6U
A5/TR5d8mUgjU+g4rk8Kb4Mu0UlXjIB0ttov0DiNewNwIRt18jA8+o+u3dpjq+sW
T8KOEUt+zwvo/7V3LvSye0rgTBIlDHCNAymg4VMk7BPZ7hm/ELNKjD+Jo2FR3qyH
B5T0Y3HsLuJvW5iB4YlcNHlsdu87kGJ55tukmi8mxdAQ4Q7e2RCOFvu396j3x+UC
B5iPNgiV5+I3lg02dZ77DnKxHZu8A/lJBdiB3QW0KtZB6awBdpUKD9jf1b0SHzUv
KBds0pjBqAlkd25HN7rOrFleaJ1/ctaJxQZBKT5ZPt0m9STJEadao0xAH0ahmbWn
OlFuhjuefXKnEgV4We0+UXgVCwOPjdAvBbI+e0ocS3MFEvzG6uBQE3xDk3SzynTn
jh8BCNAw1FtxNrQHusEwMFxIt4I7mKZ9YIqioymCzLq9gwQbooMDQaHWBfEbwrbw
qHyGO0aoSCqI3Haadr8faqU9GY/rOPNk3sgrDQoo//fb4hVC1CLQJ13hef4Y53CI
rU7m2Ys6xt0nUW7/vGT1M0NPAgMBAAGjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNV
HRMBAf8EBTADAQH/MB0GA1UdDgQWBBR5tFnme7bl5AFzgAiIyBpY9umbbjANBgkq
hkiG9w0BAQsFAAOCAgEAVR9YqbyyqFDQDLHYGmkgJykIrGF1XIpu+ILlaS/V9lZL
ubhzEFnTIZd+50xx+7LSYK05qAvqFyFWhfFQDlnrzuBZ6brJFe+GnY+EgPbk6ZGQ
3BebYhtF8GaV0nxvwuo77x/Py9auJ/GpsMiu/X1+mvoiBOv/2X/qkSsisRcOj/KK
NFtY2PwByVS5uCbMiogziUwthDyC3+6WVwW6LLv3xLfHTjuCvjHIInNzktHCgKQ5
ORAzI4JMPJ+GslWYHb4phowim57iaztXOoJwTdwJx4nLCgdNbOhdjsnvzqvHu7Ur
TkXWStAmzOVyyghqpZXjFaH3pO3JLF+l+/+sKAIuvtd7u+Nxe5AW0wdeRlN8NwdC
jNPElpzVmbUq4JUagEiuTDkHzsxHpFKVK7q4+63SM1N95R1NbdWhscdCb+ZAJzVc
oyi3B43njTOQ5yOf+1CceWxG1bQVs5ZufpsMljq4Ui0/1lvh+wjChP4kqKOJ2qxq
4RgqsahDYVvTH9w7jXbyLeiNdd8XM2w9U/t7y0Ff/9yi0GE44Za4rF2LN9d11TPA
mRGunUHBcnWEvgJBQl9nJEiU0Zsnvgc/ubhPgXRR4Xq37Z0j4r7g1SgEEzwxA57d
emyPxgcYxn/eR44/KJ4EBs+lVDR3veyJm+kXQ99b21/+jh5Xos1AnX5iItreGCc=
-----END CERTIFICATE-----
"""

# MQTT topics
ph_topic = "sensor_data_topic/pH"
turbidity_topic = "sensor_data_topic/Turbidity"
temperature_topic = "sensor_data_topic/Temperature"

# Connect to MongoDB
client = MongoClient(uri)
db = client.sensor
data_sensor = db.data_sensor

# Initialize sensor values
pH_value = 0.0
turbidity_value = 0.0
temperature_value = 0.0

# Callback functions for receiving data from MQTT broker
def on_message_ph(client, userdata, message):
    global pH_value
    try:
        pH_value = float(message.payload.decode())
    except ValueError:
        print("Error parsing pH data: ", message.payload.decode())

def on_message_turbidity(client, userdata, message):
    global turbidity_value
    try:
        turbidity_value = float(message.payload.decode())
    except ValueError:
        print("Error parsing turbidity data: ", message.payload.decode())

def on_message_temperature(client, userdata, message):
    global temperature_value
    try:
        temperature_value = float(message.payload.decode())
    except ValueError:
        print("Error parsing temperature data: ", message.payload.decode())

client_mqtt = paho.Client()
client_mqtt.username_pw_set(mqtt_username, mqtt_password)

client_mqtt.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=paho.ssl.CERT_REQUIRED,
                    tls_version=paho.ssl.PROTOCOL_TLS, ciphers=None)
client_mqtt.tls_insecure_set(False)

client_mqtt.on_connect = lambda client, userdata, flags, rc: print("Connected to MQTT broker" if rc == 0 else f"Connection failed with code {rc}")

client_mqtt.connect(broker_address, broker_port)

# Set the callback functions for MQTT client
client_mqtt.message_callback_add(ph_topic, on_message_ph)
client_mqtt.message_callback_add(turbidity_topic, on_message_turbidity)
client_mqtt.message_callback_add(temperature_topic, on_message_temperature)

client_mqtt.subscribe([(ph_topic, 0), (turbidity_topic, 0), (temperature_topic, 0)])

# Start the MQTT client loop
client_mqtt.loop_start()

# Loop every 5 seconds
while True:
    try:
        # Get the current timestamp
        timestamp = datetime.datetime.now()

        # Create a new document to insert into MongoDB
        data = {
            "timestamp": timestamp,
            "pH_value": pH_value,
            "turbidity_value": turbidity_value,
            "temperature_value": temperature_value
        }

        # Insert data into MongoDB
        result = data_sensor.insert_one(data)
        document_id = result.inserted_id
        print("Inserted document with id: {}".format(document_id))

        # Print sensor values
        print("pH_value:", pH_value)
        print("turbidity_value:", turbidity_value)
        print("temperature_value:", temperature_value)

        # Wait for 5 seconds
        time.sleep(5)

    except KeyboardInterrupt:
        # Stop MQTT client loop on Ctrl+C
        client_mqtt.loop_stop()
        break