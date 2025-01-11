import os
import yaml

configs = yaml.safe_load(open('./configs/train.yaml'))


# data path configuration
def get_data_path():
    data_path = configs['data_path']
    data_fom = os.path.join(data_path, configs['data_fom'])
    data_trans = os.path.join(data_path, configs['data_trans'])
    # expanduser expands the path to the user home directory
    data_path = os.path.expanduser(data_path)
    data_fom = os.path.expanduser(data_fom)
    data_trans = os.path.expanduser(data_trans)
    return data_fom, data_trans

# main function
if __name__ == '__main__':
    data_fom, data_trans = get_data_path()
    print(data_fom)
    print(data_trans)
