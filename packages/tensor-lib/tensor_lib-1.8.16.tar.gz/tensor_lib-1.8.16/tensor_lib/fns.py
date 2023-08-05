import tensorflow as tf

def softmax_accuracy(one_hot_labels, output):
	assert(type(output) is tf.Tensor and type(one_hot_labels) is tf.Tensor)
	output_argmax = tf.argmax(output, 1)
	labels_argmax = tf.argmax(one_hot_labels, 1)
	return tf.reduce_mean(tf.cast(tf.equal(output_argmax, labels_argmax), tf.float32))

def elementwise_accuracy(ground_truth, output):
	# check if output is list
	# assert(type(output) is tf.Tensor and type(ground_truth) is tf.Tensor)
	# assert(output.dtype is ground_truth.dtype)
	if type(output) is list:
		output = tf.convert_to_tensor(output)
		ground_truth = tf.convert_to_tensor(ground_truth)
	return tf.reduce_mean(tf.cast(tf.equal(ground_truth, output), tf.float32))

def threshold_accuracy(ground_truth, output):
	assert(type(output) is tf.Tensor and type(ground_truth) is tf.Tensor)
	assert(output.dtype is ground_truth.dtype)
	return tf.reduce_mean(tf.cast(tf.equal(ground_truth, tf.cast(tf.greater_equal(output, 0.6), tf.float32)), tf.float32))

def linear_output(output):
	assert(type(output) is tf.Tensor)
	return output
