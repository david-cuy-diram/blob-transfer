import os
import json
import uuid
import logging
import tempfile
from enum import Enum
from typing import List
from azure.storage.blob import ContainerClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError

from ...config.storage import config

class AzConnectionMethods(Enum):
    CONN_STRING = 'connection_string'

class AzBlobStorage:
    def __init__(self, config_name, container) -> None:
        self.container = container
        self.__conn_method = config_name
        if config_name == AzConnectionMethods.CONN_STRING.value:
            conn_str = config['blob'][config_name]
            self.client = ContainerClient.from_connection_string(conn_str=conn_str, container_name=self.container)
        else:
            raise Exception("Connection method not allowed")
    
    def get_client(self) -> ContainerClient:
        if self.__conn_method == AzConnectionMethods.CONN_STRING.value:
            conn_str = config['blob'][self.__conn_method]
            return ContainerClient.from_connection_string(conn_str=conn_str, container_name=self.container)
        else:
            raise Exception("Connection method not allowed")

    def list_files(self, path: str = "") -> List[str]:
        client = self.get_client()

        blob_list = client.list_blobs(name_starts_with=path)
        return list(map(lambda b: b.name, blob_list))
    
    def get(self, path: str, decoder_name='utf-8') -> str:
        client = self.get_client()

        blob_client = client.get_blob_client(path)
        if not blob_client.exists():
            raise ResourceNotFoundError('File in blob container does not exist')
        
        stream = blob_client.download_blob()
        content = stream.readall()
        return content.decode(decoder_name)
    
    def put(self, path: str, content: bytes) -> bool:
        temp_file_name = f"{tempfile.gettempdir()}/{str(uuid.uuid4())}"
        logging.info(temp_file_name)

        with open(temp_file_name, "w") as temp_file:
            temp_file.write(content)
        
        blob_client = self.get_client().get_blob_client(path)
        write_status = False
        with open(temp_file_name, "r") as data:
            content = data.read().encode('utf-8')
            try:
                blob_client.upload_blob(content)
                write_status = True
            except ResourceExistsError as e:
                logging.exception("RESOURCE ERROR")
                write_status = False
            except TypeError as e:
                logging.exception("TYPE ERROR")
                write_status = False
            except Exception as e:
                logging.exception("Error general")
                write_status = False
            finally:
                logging.info("DELETING FILE")
        
        return write_status
    
    def delete(self, path: str) -> dict:
        
        blob_client = self.get_client().get_blob_client(path)
        try:
            blob_client.delete_blob()
        except ResourceNotFoundError as e:
            logging.exception("RESOURCE ERROR")
            return False
        except Exception as e:
            logging.exception("Error general al borrar")
            return False
        
        return True