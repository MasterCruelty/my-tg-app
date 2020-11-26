import utils_config

def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)
