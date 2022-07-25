import socket
import time
import urllib3
import os,re
import socketserver
import threading
import queue
import logging
import logging.config
import yaml
from datetime import datetime
from lib.util.info import File, Tcp_Server
from lib.util.sys_log import logging_config_init,logging_start


class decode_data(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self,name='uploader')
        logging.info('uploader start')
        self.data = queue
        self.http = urllib3.PoolManager(maxsize=1000, block=True)
        self.run()
        
    def run(self):
        while True:
            read_online = self.data.get()
            logging.info(read_online)
            read_online = read_online.split('$')
            header = read_online[0].replace('ST,','').split(',')
            if len(header) != 2: continue
            Serial_No = header[0]
            data_ver = header[1]
            if data_ver == 'HB':
                logging.info(f'{Serial_No} is alive')
                continue
            data = read_online[1].replace(',ED','').replace('NAN','null').split(',')
            logging.info(f'{Serial_No} data :{data}')
            data_str = ','.join(data)
            r = self.http.request(                
                    'POST',
                    f"{Tcp_Server.api_server['server_url']}/{data_ver}/{Serial_No}",
                    fields={'data': data_str}
            )

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True,
                 queue=None):
        self.queue = queue
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                           bind_and_activate=bind_and_activate)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.queue = server.queue
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        BUFSIZE = 1024
        buffer = b''
        logging.info('Connect from: {0}:{1}'.format(self.client_address[0],self.client_address[1]))
        while(True):
            recive_data = self.request.recv(BUFSIZE)
            if len(recive_data) == 0: # connection closed
                logging.info('client closed connection.')
                break
            data = buffer + recive_data
            logging.debug(data)
            data = data.decode('utf-8','ignore').strip().split('\r\n')
            if data[-1][-2:] =='ED':
                buffer = b''
                put_data = data
            else:
                if re.match(r'AT.+|.+AT.+|.+AT',data[-1]):
                    buffer = b''
                else:
                    buffer = data[-1].encode()
                put_data = data[:-1]
            if len(put_data) != 0:
                for i,idata in enumerate(put_data):
                    if idata[0:2] =='ST':
                        self.queue.put(idata)
                    else:
                        pass
                
    def finish(self):
        logging.info("client {0}:{1} disconnect!".format(self.client_address[0],self.client_address[1]))

def connect():
    ex_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(ex_path,'config','logging.yaml')
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.load(f)
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    HOST = socket.gethostname()
    HOST = "192.168.2.38"
    PORT = 4001
    dummy_data = queue.Queue(maxsize=300)
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler, queue=dummy_data)
    server_thread = threading.Thread(target=server.serve_forever,name='socket')
    # server_thread.daemon = True
    server_thread.start()
    uploader = threading.Thread(target=decode_data, args=(dummy_data,),name='uploader')
    uploader.start()
    logging.info(threading.enumerate())
    logging.info('Server is starting up...')
    logging.info('Host: {0}, listen to port: {1}'.format(HOST,PORT))
            
if __name__=='__main__':
    ex_path = os.path.dirname(os.path.abspath(__file__))
    logging_config_init(ex_path)
    logging_start(ex_path)
    connect()