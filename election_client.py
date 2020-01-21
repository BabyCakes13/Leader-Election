#!/usr/bin/env python3

import socket
import time
import sys
import logging


class LeaderElectionClient:
    TCP_PORT = 5001  # change port based on other implemented features
    BUFFER_SIZE = 1024
    HEARTBEAT_INCREMENT = 1

    def __init__(self, attribute=0):
        self.attribute = attribute  # TODO find a good attribute
        self.server_list = sys.argv[1:]  # get the servers which the client needs to connect to

        logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s', level=logging.INFO)

    def start_client(self):
        self.set_connection()

        while 1:
            time.sleep(100)

    def set_connection(self):

        for server in self.server_list:
            logging.debug("INITIALISING CONNECTION TO " + str(server))
            try:
                self.send_message(server=server)
            except ConnectionRefusedError:
                print("CONNECTION REFUSED")

    def send_message(self, server):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server, self.TCP_PORT))
            s.send(int.to_bytes(self.attribute, byteorder="little", length=8))
            s.close()

        except ConnectionAbortedError:
            print("CONNECTION ABORTED.")

    def check_leader(self, attributes):
        if all(self.attribute >= attribute for attribute in attributes):
            # TODO this is the leader
            logging.info("THE LEADER FOUND " + str(self.attribute))
        else:
            print("Not the largest.")
        # TODO implement leader chose and message transmission here


if __name__ == "__main__":
    client = LeaderElectionClient()
    # client.start_client()
