import tensorflow as tf
import numpy as np

def to_list(value, length=2):
	ret_list = value
	if type(value) is tuple:
		ret_list = list(value)
	elif type(value) is not list:
		ret_list = [value] * length
	return ret_list

def gaussian_filter(kernel_shape):
	x = np.zeros(kernel_shape)

	def gauss(x, y, sigma=2.0):
		Z = np.sqrt(2 * np.pi * sigma ** 2)
		return  1. / Z * np.exp(-(x ** 2 + y ** 2) / (2. * sigma ** 2))

	mid = np.floor(kernel_shape[0] / 2.)
	for kernel_idx in range(0, kernel_shape[2]):
		for i in range(0, kernel_shape[0]):
			for j in range(0, kernel_shape[1]):
				x[i, j, kernel_idx, 0] = gauss(i - mid, j - mid)
	return x / np.sum(x)

def local_contrast_norm(input, radius, epsilon=1e-8, include_divisor=True):
	origin_input_shape = input.shape
	input_shape = [x.value for x in list(origin_input_shape)]
	shape_len = len(input_shape)
	assert(shape_len > 1)
	if shape_len == 2:
		input_shape = [1] + input_shape + [1]
		input = tf.reshape(input, input_shape)
	elif shape_len == 3:
		input_shape += [1]
		input = tf.reshape(input, input_shape)
	filter_shape = (radius, radius, input_shape[-1], 1)
	mid = int(np.floor(filter_shape[0] / 2.))
	filters = tf.constant(gaussian_filter(filter_shape), dtype=tf.float32)
	padded_input = tf.pad(input, [[0, 0], [mid, mid], [mid, mid], [0, 0]], 'SYMMETRIC')
	weighted_avg = tf.nn.conv2d(padded_input, filters, [1] * 4, 'SAME')
	# print(tf.tile(tf.pad(weighted_avg[:, mid:-mid, mid:-mid, :], [[0, 0], [mid, mid], [mid, mid], [0, 0]], 'CONSTANT'), [1, 1, 1, input_shape[-1]]))
	subtractive_result = input - weighted_avg[:, mid:-mid, mid:-mid, :]#tf.tile(tf.pad(weighted_avg[:, mid:-mid, mid:-mid, :], [[0, 0], [mid, mid], [mid, mid], [0, 0]], 'CONSTANT'), [1, 1, 1, input_shape[-1]])
	if include_divisor:
		var = tf.nn.conv2d(tf.square(subtractive_result), filters,	[1] * 4, 'SAME')
		denom = tf.sqrt(var)
		per_img_mean = tf.reduce_mean(denom, axis=[1, 2], keep_dims=True)
		divisor = tf.maximum(tf.maximum(per_img_mean, denom), epsilon)
		subtractive_result /= divisor
