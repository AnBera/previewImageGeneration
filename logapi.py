#importing module 
import logging
#Create and configure logger 
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
#Creating an object
logger=logging.getLogger(__name__)
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

def get_logger_instance():
	return logger