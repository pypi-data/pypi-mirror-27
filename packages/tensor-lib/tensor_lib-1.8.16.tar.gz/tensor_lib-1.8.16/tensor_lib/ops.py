import tensorflow as tf

def reLU(input):
	return tf.maximum(0.1 * input, input)