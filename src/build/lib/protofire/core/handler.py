import socket
from protofire.utils.logger import create_log
log = create_log('HANDLER', 'cyan')

def handle_request(client_socket:socket.socket, client_address:tuple):
	log(4, f'TREATING CONNECTION FROM {client_address[0]}:{client_address[1]} as HTTP request')