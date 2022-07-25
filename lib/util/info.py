import os
import yaml
from .util import exist_or_create_dir

class Tcp_Server:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_dir = os.path.join(base_dir,'config')
    with open(os.path.join(config_dir,'config.yaml'),'r', encoding='utf-8') as f:
        config_file = yaml.load(f, Loader=yaml.FullLoader)
    all_config = config_file
    api_server = config_file['api_server']
    def save_new_config(config):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_dir = os.path.join(base_dir,'config')
        with open(os.path.join(config_dir,'config.yaml'),'r', encoding='utf-8') as f:
            old_config_file = yaml.load(f, Loader=yaml.FullLoader)
        old_config_file['config'] = config
        with open(os.path.join(config_dir,'config.yaml'), 'w') as file:
            documents = yaml.dump(old_config_file, file, sort_keys=False)
        print('save config with config')
        

# class upload_SQL_config:
#     base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     config_dir = os.path.join(base_dir,'config')
#     with open(os.path.join(config_dir,'sql_config.yaml'),'r', encoding='utf-8') as f:
#         config_file = yaml.load(f, Loader=yaml.FullLoader)
#     config = config_file['config']

class File:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_dir = os.path.join(base_dir,'config')
    log_dir = os.path.join(base_dir,'log_file')
    fig_dir = os.path.join(base_dir,'fig')
    save_dir = os.path.join(base_dir,'data_file')
    script_dir = os.path.join(base_dir,'script_n_file')
    # with open(os.path.join(config_dir,'filepath.yaml'),'r', encoding='utf-8') as f:
    #     config_file = yaml.load(f, Loader=yaml.FullLoader)
    # data_dir = config_file['data_dir']

    exist_or_create_dir(base_dir)
    exist_or_create_dir(config_dir)
    exist_or_create_dir(log_dir)
    exist_or_create_dir(save_dir)