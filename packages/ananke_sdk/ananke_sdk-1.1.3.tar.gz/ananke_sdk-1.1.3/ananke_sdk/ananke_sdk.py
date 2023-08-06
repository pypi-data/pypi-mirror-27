import paho.mqtt.client as mqtt
import paho.mqtt.publish as publis
import json



class Ananke:
    client = None
    parameters = {}
    onConnect = None
    onMessage = None
    topic = None
    in_on_connect = None
    in_on_message = None



    def __init__(self):
        pass

    def connect_to_ananke(self, username, password):

        file = open("Ananke_details.txt", "r")
        file = json.load(file)

        client.username_pw_set(username, password)
        client.connect(file['ip'], file['port'], 60)

    # TO dO client.connect given user name password

    def disconnect_from_ananke(self):
        client.disconnect()

    def on_connect(self, client, userdata, flags, rc):

        global username
        global password
        global appId
        global groupId
        global deviceId
        global topic
        global in_on_message


        print("connected with device code " + str(rc))
        if rc == 0:
            in_on_connect(1)
        else:
            in_on_connect(0)

        topic = parameters['appId'] + '/' + parameters['groupId'] + '/' + parameters['deviceId'] + '/SUB'
        client.subscribe(topic)

    def on_message(self, client, userdata, msg):

        global in_on_message
        print "sucess"
        in_on_message(msg.payload)



    def begin(self, onConnect, onMessage, username_, password_, appId_, deviceId_, groupId_):
        global client
        global parameters
        global in_on_connect
        global in_on_message

        parameters = {}
        parameters['username'] = username_
        parameters['password'] = password_
        parameters['appId'] = appId_
        parameters['deviceId'] = deviceId_
        parameters['groupId'] = groupId_
        in_on_message = onMessage
        in_on_connect = onConnect


        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message


        self.connect_to_ananke(parameters['username'], parameters['password'])

        client.loop_start()
        #print "b"
        return 1


    def send_message(self, message):
        global client
        in_message = message
        client.publish(parameters['appId']+'/'+parameters['groupId']+'/'+parameters['deviceId']+'/PUB',in_message)
        print "Message Sent"
