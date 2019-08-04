#importing module 
import logging
from datetime import datetime
#Create and configure logger 
log_file_name = datetime.now().strftime('image_generation_logfile_%H_%M_%d_%m_%Y.log')
logging.basicConfig(filename=log_file_name, 
                    format='%(asctime)s %(message)s', 
                    filemode='a')
#Creating an object
logger=logging.getLogger(__name__)
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

def get_logger_instance():
	return logger