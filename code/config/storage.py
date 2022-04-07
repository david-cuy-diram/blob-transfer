import os

import Environment as env

config = {
    'local': {
        'initial_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "local")
    },
    'blob': {
        "default": env.STORAGE_CONNECTION_STRING,
        "connection_string": env.STORAGE_CONNECTION_STRING,
        "other_config": {

        }
    }
}