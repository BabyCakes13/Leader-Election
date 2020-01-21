#!/usr/bin/env python3


import logging
import socket
import time


class LeaderElectionServer:
    """
    Class which handles the server instance.
    """
    TCP_IP = ''
    TCP_PORT = 5001
    BUFFER_SIZE = 1024
    TIMEOUT = 10
    HEARTBEAT_DISCONNECT_TIME = 3

    def __init__(self):
        """
        Constructor of the class, which sets up the socket to listen to the clients.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.TCP_IP, self.TCP_PORT))
        self.socket.listen(5)
        self.socket.settimeout(self.TIMEOUT)

        self.connections = {}  # timestamps where key:address, value:timestamp

        logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=logging.DEBUG)

    def start_server(self):
        """
        Function which sets up the connection so it listens continuously for new clients, while also always checking that
        there was no one disconnected.
        :return: None
        """
        while 1:
            try:
                self.set_connection()
            except socket.timeout:
                pass
            # self.check_heartbeats()

    def set_connection(self):
        connection, addrport = self.socket.accept()
        connection.settimeout(self.TIMEOUT)
        address = addrport[0]

        if address not in self.connections:
            self.connections[address] = time.time()
            logging.info("FIRST CONNECTION: " + str(address) + " ( " + str(self.connections[address]) + ").")
            logging.info("ALL CONNECTIONS: " + str(self.connections.keys()))

        logging.debug("Timestamps: " + str(self.connections.keys()))

        while 1:
            print("START CONNECTION")
            data = self.receive_data(connection=connection)
            if not data:
                break
            received_heartbeat = int.from_bytes(data, byteorder="little")

            logging.info("MESSAGE ARRIVED: " + str(received_heartbeat))
            self.handle_reconnect(address=address)

        connection.close()

    def receive_data(self, connection):
        """
        Function which handles data receiving, checks its validity and handles timeout.
        :param connection: The connection to the server.
        :return: The heartbeat.
        """

        data = None
        try:
            data = connection.recv(self.BUFFER_SIZE)
        except socket.timeout:
            logging.critical("TIMEOUT:receive data from client. (", self.TIMEOUT, " seconds.)")
        return data

    def handle_reconnect(self, address):
        """
        Function which checks if the address reconnected to the server after a crash.
        :param address: The address which is checked for reconnect.
        :return: None
        """
        try:
            if address not in self.connections.keys():
                self.connections[address] = time.time()
                logging.info("RECONNECTED:" + str(address) + " at time: " + str(self.connections[address]))
        except KeyError:
            logging.debug("No key with address:" + str(address))

    def check_leaders(self, attributes):
        pass


if __name__ == "__main__":
    server = LeaderElectionServer()
    server.start_server()
