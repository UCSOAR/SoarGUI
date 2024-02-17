from concurrent.futures import ThreadPoolExecutor
import enum
import queue
import serial           # You'll need to run `pip install pyserial`
from cobs import cobs   # pip install cobs
from Codec import Codec
import SoarLib.CoreProto_pb2 as ProtoCore
import SoarLib.TelemetryMessage_pb2 as ProtoTele
import SoarLib.ControlMessage_pb2 as ProtoCtr
import Ethernet_handler as EtHan
import Telemetry_Objects as TelO
import Protobuf_parser as ProtoParse
import google.protobuf.message as Message
import json

from CommonLogger import CommonLogger

MIN_SERIAL_MESSAGE_LENGTH = 6

UART_SERIAL_PORT = "/dev/ttyS0"
RADIO_SERIAL_PORT = "/dev/ttyUSB0"

UART_BAUDRATE = 115200
RADIO_BAUDRATE = 115200 #NOTE: might need to change this (57600 ???)

class SerialDevices(enum):
    UART = 1
    RADIO = 2

class SerialHandler():
    def __init__(self):#TODO: write description and types
        CommonLogger.logger.info("SerialHandler initializing")
        self.serial_executor = ThreadPoolExecutor(max_workers=2)
        self.serial_stop = False
        
    def _radio_rx_thread(self):#TODO: write description and types
        self.radio_serial = serial.Serial(port=RADIO_SERIAL_PORT, baudrate=UART_BAUDRATE, bytesize=8, parity=serial.PARITY_NONE, timeout=None, stopbits=serial.STOPBITS_ONE)
        while not self.serial_stop:
            message = self.radio_serial.read_until(expected = b'\x00', size = None)
            self._handle_serial_message(SerialDevices.RADIO, message)

    def _uart_rx_thread(self):#TODO: write description and types
        self.uart_serial = serial.Serial(port=UART_SERIAL_PORT, baudrate=UART_BAUDRATE, bytesize=8, parity=serial.PARITY_NONE, timeout=None, stopbits=serial.STOPBITS_ONE)
        while not self.serial_stop:
            message = self.radio_serial.read_until(expected = b'\x00', size = None)
            self._handle_serial_message(SerialDevices.RADIO, message)

    def start(self):#TODO: write description and types
        self.uart_thread_task = self.serial_executor.submit(self._uart_rx_thread)
        self.radio_thread_task = self.serial_executor.submit(self._radio_rx_thread)

    def stop(self):#TODO: write description and types
        self.serial_stop = True
        self.uart_thread_task.result()
        self.radio_thread_task.result()

    def _handle_serial_message(self, source: SerialDevices, message: bytes):#TODO: write description and types
        if len(message) < MIN_SERIAL_MESSAGE_LENGTH:
            CommonLogger.logger.warn(f"Message from {source.name} too short: {message}")
            return
        
        # Decode, remove 0x00 byte
        try:
            msgId, data = Codec.Decode(message[:-1], len(message) - 1)
        except cobs.DecodeError:
            CommonLogger.logger.warn("Invalid cobs message")
            return
        
        # Process message according to ID
        if msgId == ProtoCore.MessageID.MSG_TELEMETRY:#TODO: check if message id is still the same
            process_telemetry_message(data)
        elif msgId == ProtoCore.MessageID.MSG_CONTROL:#TODO: check if message id is still the same
            process_control_message(data)
        else:
            CommonLogger.logger.warn("Received invalid MessageID")

    def send_serial_message(self, message, message_ID, target):#TODO: write description and types
        CommonLogger.logger.info(f"Sending message {message_ID} to {target.name}")

        buf = message.SerializeToString()
        encBuf = Codec.Encode(buf, len(buf), message_ID)

        if target ==  ProtoCore.NODE_DMB or target ==  ProtoCore.NODE_PBB:#TODO: Check if the nodes are still the same
            self.radio_serial.write(encBuf)
        if target ==  ProtoCore.NODE_RCU or target ==  ProtoCore.NODE_SOB:#TODO: Check if nodes are still the same
            self.uart_serial.write(encBuf)

    def process_telemetry_message(data):
        received_message = ProtoTele.TelemetryMessage()
        try:
            received_message.ParseFromString(data)
        except Message.DecodeError:
            CommonLogger.logger.warn("Unable to decode telemetry message: {data}")
            return
        
        if received_message.target == ProtoCore.NODE_RCU:
            telemetry_message_type = received_message.WhichOneof('message')
            CommonLogger.logger.debug("Telemetry message received: \n\t{telemetry_message_type}\n\t{received_message}")







            print('========')
            print(message_type)
            print(received_message)
            print('========')












# telemetry message
def process_telemetry_message(data):
    received_message = ProtoTele.TelemetryMessage()
    try:
        received_message.ParseFromString(data)
    except Message.DecodeError:
        print("cannot decode telemetry message")
        return

    if received_message.target == ProtoCore.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        print('========')
        print(message_type)
        print(received_message)
        print('========')

        if(message_type != None):
            topic, jsnStr = ProtoParse.TELE_FUNCTION_DICTIONARY[message_type](received_message)
            EtHan.soar_publish(topic, jsnStr)
            return
        else:
            print("received invalid telemetry message type")
            EtHan.soar_publish("TELE_PI_ERROR", json.dumps({"error": "Invalid telemetry message type"}))

# control message 
def process_control_message(data):
    received_message = ProtoCtr.ControlMessage()

    try:
        received_message.ParseFromString(data)
    except message.DecodeError:
        print("cannot decode control message")
        return

    #print(received_message)

    if received_message.target == ProtoCore.NODE_RCU:
        message_type = received_message.WhichOneof('message')
        if message_type == 'sys_state':
            #print(received_message.sys_state)
            if received_message.source == ProtoCore.NODE_DMB:
                TelO.tele_dmb_obj.current_state = ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state]
                EtHan.soar_publish("CONTROL_SYS_STATE", json.dumps({"dmb_state": str(TelO.tele_dmb_obj.current_state)}))

                #print(ProtoParse.PROTO_STATE_TO_STRING[received_message.sys_state.rocket_state])
        elif message_type == 'hb':
            print('hb: ', received_message.source)
        elif message_type == 'ping':
            if received_message.source == ProtoCore.NODE_DMB and received_message.ping.ping_response_sequence_num == DMB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from DMB received"}')
            elif received_message.source == ProtoCore.NODE_PBB and received_message.ping.ping_response_sequence_num == PBB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from PBB received"}')
            elif received_message.source == ProtoCore.NODE_SOB and received_message.ping.ping_response_sequence_num == SOB_SEQ_NUM:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "ping from SOB received"}')
            else:
                EtHan.soar_publish("TELE_PI_ERROR", '{"ping_status" : "unknown ping received"}')
            print('we were pinged: ', received_message.source)
        elif message_type == 'ack':
            print('oh hey, we ack: ', received_message.source)
        elif message_type == 'nack':
            #add resend of message
            print('nack received, this is bad')


# placeholder in case the pi ever receives a command message
#def process_command_message(msg):