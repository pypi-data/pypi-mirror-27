from . import name_manager
from . import weight_manager
from . import ops
from . import util
import tensorflow as tf
import numpy as np

class Layer:
  def __init__(self):
    self.layer = None

  def update_layer(self, layer):
    if type(layer) is list or type(layer) is tuple:
      for _layer in layer:
        assert(type(_layer) is tf.Tensor)
    else:
      assert(type(layer) is tf.Tensor)
    self.layer = layer
    return self

  def get_layer(self):
    return self.layer

  def get_weight(self):
    return self.weight

  def update_input(self, input):
    assert(Layer in type(input).__bases__ or type(input) is Layer)
    self.is_training = input.get_is_training()
    return input.get_layer()

  def get_is_training(self):
    return self.is_training

  def batch_norm(self):
    assert(type(self.layer) is tf.Tensor)
    self.layer = tf.contrib.layers.batch_norm(self.layer, is_training=self.is_training, scope=self.name)
    return self

  # def attention(self):
    # TODO: continue here

  def local_contrast_norm(self, radius, epsilon=1e-8, include_divisor=True):
    assert(type(self.layer) is tf.Tensor)
    with tf.variable_scope(self.name):
      self.layer = util.local_contrast_norm(self.layer, radius, epsilon, include_divisor)
      return self

  def dropout(self, keep_prob=0.5):
    assert(type(self.layer) is tf.Tensor)
    with tf.variable_scope(self.name):
      self.layer = tf.layers.dropout(self.layer, keep_prob, training=self.is_training, name=name_manager.get_layer_name('drop'))
      return self

class Conv(Layer):
  def __init__(self, kernel_size, num_filter, activation_fn=ops.reLU, strides=(1, 1), padding='SAME', use_bias=True, reuse_weight_layer=None, weight_mean=0.0, weight_stddev=1.0, bias_mean=0.0, bias_stddev=1.0, name=None):
    super(Conv, self).__init__()
    self.kernel_size = util.to_list(kernel_size)
    self.num_filter = num_filter
    self.activation_fn = activation_fn
    strides = util.to_list(strides)
    self.strides = [1] + list(strides) + [1]
    self.padding = padding
    self.use_bias = use_bias
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('conv')
    self.weight = None
    if reuse_weight_layer is not None:
      self.weight = reuse_weight_layer.get_weight()[:1]
    self.weight_mean = weight_mean
    self.weight_stddev = weight_stddev
    self.bias_mean = bias_mean
    self.bias_stddev = bias_stddev
  def __call__(self, input):
    input = super(Conv, self).update_input(input)
    with tf.variable_scope(self.name):
      if self.weight is None:
        W, b = weight_manager.create_weight_bias(self.kernel_size + [input.get_shape().as_list()[-1], self.num_filter], self.weight_mean, self.weight_stddev, self.bias_mean, self.bias_stddev)
        self.weight = [W, b]
      else:
        self.weight.append(weight_manager.create_bias_variable([self.num_filter], self.bias_mean, self.bias_stddev))
      x = tf.nn.conv2d(input, self.weight[0], strides=self.strides, padding=self.padding)
      if self.use_bias:
        x = tf.nn.bias_add(x, self.weight[1])
      if self.activation_fn is not None:
        x = self.activation_fn(x)
      super(Conv, self).update_layer(x)
      return self

class DeConv(Layer):
  def __init__(self, kernel_size, num_filter, output_shape=None, activation_fn=tf.nn.sigmoid, strides=(1, 1), padding='SAME', use_bias=True, reuse_weight_layer=None, weight_mean=0.0, weight_stddev=1.0, bias_mean=0.0, bias_stddev=1.0, name=None):
    super(DeConv, self).__init__()
    self.kernel_size = util.to_list(kernel_size)
    self.num_filter = num_filter
    self.output_shape = output_shape
    if output_shape is not None:
      assert(len(output_shape) == 2)
    self.activation_fn = activation_fn
    strides = util.to_list(strides)
    self.strides = [1] + list(strides) + [1]
    self.padding = padding
    self.use_bias = use_bias
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('deconv')
    self.weight = None
    if reuse_weight_layer is not None:
      self.weight = reuse_weight_layer.get_weight()[:1]
    self.weight_mean = weight_mean
    self.weight_stddev = weight_stddev
    self.bias_mean = bias_mean
    self.bias_stddev = bias_stddev
  def __call__(self, input):
    input = super(DeConv, self).update_input(input)
    with tf.variable_scope(self.name):
      input_shape = input.get_shape().as_list()
      if self.weight is None:
        W = weight_manager.create_weight_variable(self.kernel_size + [self.num_filter, input_shape[-1]], self.weight_mean, self.weight_stddev)
        b = weight_manager.create_bias_variable(self.num_filter, self.bias_mean, self.bias_stddev)
        self.weight = [W, b]
      else:
        self.weight.append(weight_manager.create_bias_variable(self.num_filter, self.bias_mean, self.bias_stddev))
      if self.output_shape is None:
        input_shape = [x for x in input_shape]
        dim0 = input_shape[0]
        if dim0 is None:
          dim0 = tf.shape(input)[0]
        self.output_shape = [dim0, input_shape[1] * self.strides[1], input_shape[2] * self.strides[2], self.num_filter]
        self.output_shape = tf.stack(self.output_shape)
      else:
        self.output_shape = [input_shape[0]] + self.output_shape + [self.num_filter]
      x = tf.nn.conv2d_transpose(input, self.weight[0], self.output_shape, strides=self.strides, padding=self.padding)
      x = tf.reshape(x, self.output_shape)
      if self.use_bias:
        x = tf.nn.bias_add(x, self.weight[1])
      if self.activation_fn is not None:
        x = self.activation_fn(x)
      super(DeConv, self).update_layer(x)
      return self

class MaxPooling(Layer):
  def __init__(self, pool_size, strides=None, padding='VALID', name=None):
    super(MaxPooling, self).__init__()
    self.pool_size = util.to_list(pool_size)
    self.strides = strides
    if self.strides is None:
      self.strides = self.pool_size
    else:
      self.strides = util.to_list(self.strides)
    self.padding = padding
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('max_pool')
  def __call__(self, input):
    input = super(MaxPooling, self).update_input(input)
    with tf.variable_scope(self.name):
      x = tf.layers.max_pooling2d(input, self.pool_size, self.strides, self.padding, name=self.name)
      super(MaxPooling, self).update_layer(x)
      return self

class L2Pooling(Layer):
  def __init__(self, pool_size, strides=None, padding='VALID', name=None):
    super(L2Pooling, self).__init__()
    self.pool_size = util.to_list(pool_size)
    self.strides = strides
    if self.strides is None:
      self.strides = self.pool_size
    else:
      self.strides = util.to_list(self.strides)
    self.padding = padding
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('l2_pool')
  def __call__(self, input):
    input = super(L2Pooling, self).update_input(input)
    with tf.variable_scope(self.name):
      pool_area = self.pool_size[0] * self.pool_size[1]
      x = tf.sqrt(tf.nn.avg_pool(tf.square(input), [1] + self.pool_size + [1], [1] + self.strides + [1], self.padding) * pool_area)
      super(L2Pooling, self).update_layer(x)
      return self

class AvgPooling(Layer):
  def __init__(self, pool_size, strides=None, padding='VALID', name=None):
    super(AvgPooling, self).__init__()
    self.pool_size = util.to_list(pool_size)
    self.strides = strides
    if self.strides is None:
      self.strides = self.pool_size
    else:
      self.strides = util.to_list(self.strides)
    self.padding = padding
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('l2_pool')
  def __call__(self, input):
    input = super(AvgPooling, self).update_input(input)
    with tf.variable_scope(self.name):
      x = tf.nn.avg_pool(input, [1] + self.pool_size + [1], [1] + self.strides + [1], self.padding)
      super(AvgPooling, self).update_layer(x)
      return self

class RNN(Layer):
  def __init__(self, num_hidden_unit, cell_type='lstm', cell_args=None, is_bidirectional=False, name=None):
    self.num_hidden_unit = num_hidden_unit
    if type(cell_type) is str:
      self.cell_type = {
        'lstm': tf.contrib.rnn.BasicLSTMCell,
        'rnn': tf.contrib.rnn.BasicRNNCell,
        'gru': tf.contrib.rnn.GRUCell
      }[cell_type]
    elif type(cell_type) is type:
        self.cell_type = cell_type
    self.cell_args = cell_args
    self.is_bidirectional = is_bidirectional
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('rnn')
  def __call__(self, input):
    input = super(RNN, self).update_input(input)
    with tf.variable_scope(self.name):
      cells = []
      def create_cell():
        if self.cell_args is None:
          x = self.cell_type(self.num_hidden_unit)
        else:
          self.cell_args['num_units'] = self.num_hidden_unit
          x = self.cell_type(**self.cell_args)
        return x
      if self.is_bidirectional:
        for i in range(2):
          cells.append(create_cell())
        self.output, self.state = tf.nn.bidirectional_dynamic_rnn(cells[0], cells[1], input, dtype=tf.float32)
      else:
        cell = create_cell()
        self.output = self.state = tf.nn.dynamic_rnn(cell, input, dtype=tf.float32)
      super(RNN, self).update_layer(self.output)
      return self.output
  def get_state(self):
    return self.state

class TopK(Layer):
  def __init__(self, K, last_n_dims=1, transpose=None, name=None):
    self.K = K
    self.transpose = transpose
    self.name = name
    if name is None:
      self.name = name_manager.get_layer_name('topK')
    self.last_n_dims = last_n_dims
  def __call__(self, input):
    input = super(TopK, self).update_input(input)
    with tf.variable_scope(self.name):
      if self.transpose is not None:
        input = tf.transpose(input, self.transpose)
      input_shape = input.get_shape().as_list()
      shape_pool = 1
      for i in input_shape[-self.last_n_dims:]:
        shape_pool *= i
      new_input_shape = [x if x is not None else -1 for x in input_shape][:-self.last_n_dims] + [shape_pool]
      input = tf.nn.l2_normalize(tf.reshape(input, tf.stack(new_input_shape)), -1)
      top_k_value, top_k_indice = tf.nn.top_k(input, self.K)
      top_k_value.set_shape(input_shape[:-self.last_n_dims] + [self.K])
      self.top_k_value = top_k_value
      coors = None
      last_result = tf.expand_dims(top_k_indice, -1)
      for i in range(-self.last_n_dims, 0):
        shape_pool //= input_shape[i]
        if coors is None:
          coors = tf.div(last_result, shape_pool)
        else:
          coors = tf.concat([coors, tf.div(last_result, shape_pool)], -1)
        last_result = tf.mod(last_result, shape_pool)
      coors = tf.cast(coors, tf.int32)
      super(TopK, self).update_layer(coors)
      return self
  def get_value(self):
    return self.top_k_value

class SpatialSoftmax(Layer):
  def __init__(self, name=None, temperature=None):
    super(SpatialSoftmax, self).__init__()
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('spatial_softmax')
    self.temperature = temperature
  def __call__(self, input):
    input = super(SpatialSoftmax, self).update_input(input)
    with tf.variable_scope(self.name):
      # Create tensors for x and y coordinate values, scaled to range [-1, 1].
      shape = tf.shape(input)
      static_shape = input.shape
      height, width, num_channels = shape[1], shape[2], static_shape[3]
      pos_x, pos_y = tf.meshgrid(tf.lin_space(-1., 1., num=height),
                      tf.lin_space(-1., 1., num=width),
                      indexing='ij')
      pos_x = tf.reshape(pos_x, [height * width])
      pos_y = tf.reshape(pos_y, [height * width])
      if self.temperature is None:
        self.temperature = tf.get_variable('temperature', shape=(), dtype=tf.float32, initializer=tf.ones_initializer())
      features = tf.reshape(tf.transpose(input, [0, 3, 1, 2]), [-1, height * width])
      softmax_attention = tf.nn.softmax(features/self.temperature)
      expected_x = tf.reduce_sum(pos_x * softmax_attention, [1], keep_dims=True)
      expected_y = tf.reduce_sum(pos_y * softmax_attention, [1], keep_dims=True)
      expected_xy = tf.concat([expected_x, expected_y], 1)
      feature_keypoints = tf.reshape(expected_xy, [-1, num_channels.value * 2])
      feature_keypoints.set_shape([None, num_channels.value * 2])
      super(SpatialSoftmax, self).update_layer(feature_keypoints)
      return self

class Fc(Layer):
  def __init__(self, out_units, activation_fn=ops.reLU, reuse_weight_layer=None, weight_mean=0.0, weight_stddev=1.0, bias_mean=0.0, bias_stddev=1.0, name=None):
    super(Fc, self).__init__()
    self.out_units = out_units
    self.activation_fn = activation_fn
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('fc')
    self.weight = None
    if reuse_weight_layer is not None:
      self.weight = reuse_weight_layer.get_weight()[:1]
    self.weight_mean = weight_mean
    self.weight_stddev = weight_stddev
    self.bias_mean = bias_mean
    self.bias_stddev = bias_stddev
  def __call__(self, input):
    input = super(Fc, self).update_input(input)
    with tf.variable_scope(self.name):
      total_in_units = 1
      input_shape = input.get_shape().as_list()
      for dim in input_shape[1:]:
        total_in_units *= dim
      shape = [total_in_units, self.out_units]
      if total_in_units != input_shape[1]:
        input_shape = [-1, total_in_units]
        input = tf.reshape(input, input_shape)
      if self.weight is None:
        W, b = weight_manager.create_weight_bias(shape, self.weight_mean, self.weight_stddev, self.bias_mean, self.bias_stddev)
        self.weight = [W, b]
      else:
        if self.weight[0].get_shape().as_list()[0] != total_in_units:
          self.weight[0] = tf.transpose(self.weight[0])
        self.weight.append(weight_manager.create_bias_variable([self.out_units], self.bias_mean, self.bias_stddev))
      x = tf.matmul(input, self.weight[0]) + self.weight[1]
      if self.activation_fn is not None:
        x = self.activation_fn(x)
      super(Fc, self).update_layer(x)
      return self

class UpSampling(Layer):
  def __init__(self, ratio, name=None):
    super(UpSampling, self).__init__()
    self.ratio = util.to_list(ratio)
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('upsampling')
  def __call__(self, input):
    input = super(UpSampling, self).update_input(input)
    with tf.variable_scope(self.name):
      shape = [x if x is not None else -1 for x in input.get_shape().as_list()]
      shape[1] *= self.ratio[0]
      shape[2] *= self.ratio[1]
      x = tf.image.resize_images(input, shape[1:3], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
      x = tf.reshape(x, shape)
      super(UpSampling, self).update_layer(x)
      return self

class Noise(Layer):
  class NoiseType:
    GAUSSIAN = 0
    MASK = 1
  def __init__(self, noise_type, stddev=0.1, name=None):
    super(Noise, self).__init__()
    self.noise_type = noise_type
    self.stddev = stddev
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('noise')
  def __call__(self, input):
    input = super(Noise, self).update_input(input)
    with tf.variable_scope(self.name):
      if self.noise_type == self.NoiseType.GAUSSIAN:
        noise = tf.random_normal(tf.shape(input), mean=0.0, stddev=self.stddev, dtype=tf.float32)
        x = input + noise
      elif self.noise_type == self.NoiseType.MASK:
        x = input * tf.cast(tf.random_uniform(tf.shape(input), minval=0, maxval=2, dtype=tf.int32), tf.float32)
      super(Noise, self).update_layer(x)
      return self

class Reshape(Layer):
  def __init__(self, shape, name=None):
    super(Reshape, self).__init__()
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('reshape')
    self.shape = shape
  def __call__(self, input):
    input = super(Reshape, self).update_input(input)
    with tf.variable_scope(self.name):
      x = tf.reshape(input, self.shape)
      super(Reshape, self).update_layer(x)
      return self

class Transpose(Layer):
  def __init__(self, perm, name=None):
    super(Transpose, self).__init__()
    self.perm = perm
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('transpose')
  def __call__(self, input):
    input = super(Transpose, self).update_input(input)
    with tf.variable_scope(self.name):
      x = tf.transpose(input, self.perm)
      super(Transpose, self).update_layer(x)
      return self

class Concat(Layer):
  def __init__(self, axis, name=None):
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('concat')
    self.axis = axis
  def __call__(self, *input):
    input = [super(Concat, self).update_input(x) for x in input]
    with tf.variable_scope(self.name):
      x = tf.concat(input, self.axis)
      super(Concat, self).update_layer(x)
      return self

class Split(Layer):
  def __init__(self, num_or_size_splits, axis=0, num=None, name=None):
    self.num_or_size_splits = num_or_size_splits
    self.axis = axis
    self.num = num
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('split')
  def __call__(self, input):
    input = super(Split, self).update_input(input)
    with tf.variable_scope(self.name):
      x = tf.split(input, self.num_or_size_splits, self.axis, self.num)
      # super(Split, self).update_layer(tf.convert_to_tensor(x))
      self.layer = []
      for i in range(len(x)):
        new_layer = Layer()
        new_layer.is_training = self.is_training
        new_layer.layer = x[i]
        self.layer.append(new_layer)
      return self
  def __getitem__(self, index):
    return self.layer[index]
  def __setitem__(self, index, value):
    assert('Not supported')

class Lambda(Layer):
  def __init__(self, _lambda, name=None):
    self._lambda = _lambda
    self.name = name
    if self.name is None:
      self.name = name_manager.get_layer_name('lambda')
  def __call__(self, *input):
    input_arg = []
    for input_item in input:
      if not (Layer in type(input_item).__bases__ or type(input_item) is Layer):#or type(input_item) is tf.Tensor):
        tmp_layer = Layer()
        tmp_layer.layer = tf.convert_to_tensor([x.get_layer() for x in input_item])
        tmp_layer.is_training = input_item[0].is_training
      else:
        tmp_layer = input_item
      input_arg.append(super(Lambda, self).update_input(tmp_layer))
    with tf.variable_scope(self.name):
      x = self._lambda(*input_arg)
      super(Lambda, self).update_layer(x)
      return self

class Input(Layer):
  def __init__(self, shape, dtype=tf.float32, name=None):
    self.name = name
    if self.name is None:
      self.name = 'x'
    self.is_training = tf.placeholder(tf.bool, name="is_training")
    super(Input, self).__init__()
    self.placeholder_layer = tf.placeholder(tf.float32, [None] + list(shape), name=self.name)
    self.layer = self.placeholder_layer
