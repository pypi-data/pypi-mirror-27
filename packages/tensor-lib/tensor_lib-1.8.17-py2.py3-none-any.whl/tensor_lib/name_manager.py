
global_layer_num_count = 0

def get_layer_name(prefix):
    global global_layer_num_count
    global_layer_num_count += 1
    return prefix + str(global_layer_num_count)

def get_layer_num():
    return global_layer_num_count
