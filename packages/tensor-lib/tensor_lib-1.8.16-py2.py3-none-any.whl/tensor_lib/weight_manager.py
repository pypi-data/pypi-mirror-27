import tensorflow as tf

def create_weight_variable(shape, mean=0.0, stddev=1.0, dtype=tf.float32):
    return tf.get_variable("weight", shape, dtype, tf.truncated_normal_initializer(mean, stddev))

def create_bias_variable(shape, mean=0.0, stddev=1.0, dtype=tf.float32):
    return tf.get_variable("bias", shape, dtype, tf.truncated_normal_initializer(mean, stddev))

def create_weight_bias(shape, weight_mean=0.0, weight_stddev=1.0, bias_mean=0.0, bias_stddev=1.0, dtype=tf.float32):
    assert((type(shape) is list or type(shape) is tuple))
    return create_weight_variable(shape, weight_mean, weight_stddev, dtype), create_bias_variable(shape[-1], bias_mean, bias_stddev, dtype)
