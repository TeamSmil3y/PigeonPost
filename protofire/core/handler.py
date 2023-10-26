import sockets
from utils.logger import create_log
log = create_log('HANDLER', 'cyan')

def handle_request(client_socket:sockets.socket, client_address:tuple):
	log(4, )