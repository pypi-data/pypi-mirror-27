from __future__ import print_function
from . import layers
from . import fns

import tensorflow as tf
import numpy as np
import os
import re
import math
import shutil
import types


class Model:
  def __init__(self, input, output, logdir='log', name=None):
    assert(type(input) is layers.Input)
    self.input = input.placeholder_layer
    self.output_is_list = type(output) is list or type(output) is tuple
    if self.output_is_list:
      self.output = [x.get_layer() for x in output]
      self.is_training = output[0].is_training
    else:
      self.output = output.get_layer()
      self.is_training = output.is_training
    self.loss_fn = None
    self.output_fn = None
    self.accuracy_fn = None
    self.name = name
    self.sess = None
    self.merged = None
    self.train_writer = None
    self.saver = None
    self.model_save_path = "save"
    self.is_continue = False
    if self.name is None:
      self.name = 'train'
    self.logdir = logdir
  def __exit__(self):
    if self.sess is not None:
      self.sess.close()
  def add_loss(self, loss):
    assert(self.sess is None)
    assert(type(loss) is tf.Tensor)
    tf.losses.add_loss(loss)
    return self
  def set_loss_fn(self, loss_fn):
    assert(self.sess is None)
    self.loss_fn.append(loss_fn)
    return self
  def add_output_fn(self, output_fn):
    assert(self.sess is None)
    self.output_fn.append(output_fn)
    return self
  def set_accuracy_fn(self, accuracy_fn):
    assert(self.sess is None)
    self.accuracy_fn = accuracy_fn
    return self
  def clear_log(self):
    if os.path.exists(self.logdir + '/' + self.name):
      shutil.rmtree(self.logdir + '/' + self.name)
    return self
  def get_ground_truth_layer(self):
    assert(self.sess is not None and type(self.ground_truth) is tf.Tensor)
    return self.ground_truth
  def compile(self, optimizer=tf.train.AdamOptimizer, optimizer_args={}, ground_truth_layer=None, loss_fn=tf.losses.softmax_cross_entropy, output_fn=tf.nn.softmax, accuracy_fn=fns.softmax_accuracy, model_save_path='save', is_continue=False):
    assert(type(self.input) is tf.Tensor)
    # if self.output_is_list:
    # 	output_shape = [len(self.output)] + self.output[0].get_shape()
    # else:
    # 	output_shape = list(self.output.get_shape())
    # self.loss_fn(self.ground_truth, self.output)

    self.loss_fn = loss_fn
    if type(output_fn) is not list and type(output_fn) is not tuple:
      self.output_fn = [ output_fn ]
    else:
      self.output_fn = output_fn
    self.output_layers = []
    self.accuracy_fn = accuracy_fn
    
    assert(self.accuracy_fn is not None)

    if self.output_is_list:
      assert(len(self.output) == len(self.output_fn))
      for i in range(len(self.output)):
        self.output_layers.append(self.output_fn[i](self.output[i]))
      if ground_truth_layer is None:
        self.ground_truth =	tf.placeholder(self.input.dtype, [len(self.output_layers)] + self.output_layers[0].get_shape().as_list(), 'y_')
        self.fit_fn = self._fit
      else:
        assert(layers.Layer in type(ground_truth_layer).__bases__)
        self.fit_fn = self._fit2
        self.ground_truth = tf.identity(ground_truth_layer.get_layer(), 'y_')
      self.loss_fn(self.ground_truth, self.output_layers)
      self.accuracy = self.accuracy_fn(self.ground_truth, self.output_layer)
    else:
      if type(self.output) is not tf.Tensor:
        assert(len(self.output) == 1)
      assert(len(self.output_fn) == 1)
      self.output_layers.append(self.output_fn[0](self.output))
      if ground_truth_layer is None:
        self.ground_truth = tf.placeholder(self.input.dtype, self.output_layers[0].get_shape().as_list(), 'y_')
        self.fit_fn = self._fit
      else:
        assert(layers.Layer in type(ground_truth_layer).__bases__)
        self.fit_fn = self._fit2
        self.ground_truth = tf.identity(ground_truth_layer.get_layer(), 'y_')
      self.loss_fn(self.ground_truth, self.output_layers[0])
      self.accuracy = self.accuracy_fn(self.ground_truth, self.output_layers[0])

    self.global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name="global_step")

    with tf.variable_scope(self.name):
      update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
      with tf.control_dependencies(update_ops):
        self.optimizer = optimizer(**optimizer_args)
        self.losses = tf.losses.get_total_loss()
        tf.summary.scalar('accuracy', self.accuracy)
        tf.summary.scalar('loss', self.losses)
        self.train_step = self.optimizer.minimize(self.losses, self.global_step)
    
    self.sess = tf.Session()

    with self.sess.as_default():
      self.saver = tf.train.Saver()

      self.merged = tf.summary.merge_all()
      self.train_writer = tf.summary.FileWriter(self.logdir + '/' + self.name, self.sess.graph)
      tf.global_variables_initializer().run()

      if model_save_path is not None and model_save_path != '' and not os.path.exists(model_save_path):
        os.mkdir(model_save_path)
      
      if is_continue:
        try:
          self.saver.restore(self.sess, model_save_path + '/' + self.name)
          self.is_continue = True
        except:
          print('No save file')
          self.is_continue = False
      elif model_save_path is not None and model_save_path != '' and os.path.exists(model_save_path):
        pattern = re.compile('([A-Za-z_]+)\..*')
        try:
          for file_name in os.listdir(model_save_path):
            if pattern.match(file_name).group(1) == self.name:
              os.remove(model_save_path + '/' + file_name)
        except:
          pass
        self.is_continue = False
      self.model_save_path = model_save_path

      return self
  def fit(self, train_data_label_pair_or_generator_count_pair, batch_size=50, epochs=1, shuffle=True, validation_data_label_pair_or_generator_count_pair=None, valid_each_epoch=2, summarize_each_epoch=10, model_save_every_epcoh=10, verbose=True):
    assert(self.sess is not None)
    self.fit_fn(train_data_label_pair_or_generator_count_pair, batch_size, epochs, shuffle, validation_data_label_pair_or_generator_count_pair, valid_each_epoch, summarize_each_epoch, model_save_every_epcoh, verbose)
  def _fit(self, train_data_label_pair_or_generator_count_pair, batch_size=50, epochs=1, shuffle=True, validation_data_label_pair_or_generator_count_pair=None, valid_each_epoch=2, summarize_each_epoch=10, model_save_every_epcoh=10, verbose=True):
    assert(type(epochs) is int and type(batch_size) is int and type(valid_each_epoch) is int and type(summarize_each_epoch) is int)

    indice = []
    def batch_generator(data_label_pair):
      # data_label_pair_shape = np.shape(data_label_pair)
      data_shape = np.shape(data_label_pair[0])
      label_shape = np.shape(data_label_pair[1])
      assert(len(data_label_pair) == 2)
      while True:
        if shuffle:
          indice = np.random.permutation(data_shape[0])
        else:
          indice = xrange(data_shape[0])
        for i in range(data_shape[0] // batch_size):
          target_indice = indice[i * batch_size : (i + 1) * batch_size]
          if len(self.output_fn) > 1:
            yield [data_label_pair[0][j] for j in target_indice], [[data_label_pair[1][k][j] for j in target_indice] for k in len(self.output_fn)]
          else:
            yield [data_label_pair[0][j] for j in target_indice], [data_label_pair[1][j] for j in target_indice]#, (i + 1) == steps

    train_use_generator = False
    valid_use_generator = False
    if isinstance(train_data_label_pair_or_generator_count_pair[0], types.GeneratorType):
      train_batch_generator = train_data_label_pair_or_generator_count_pair[0]
      train_use_generator = True
    else:
      train_batch_generator = batch_generator(train_data_label_pair_or_generator_count_pair)
    if validation_data_label_pair_or_generator_count_pair is not None:
      if isinstance(validation_data_label_pair_or_generator_count_pair[0], types.GeneratorType):
        valid_batch_generator = validation_data_label_pair_or_generator_count_pair[0]
        valid_use_generator = True
      else:
        valid_batch_generator = batch_generator(validation_data_label_pair_or_generator_count_pair)

    try:
      with self.sess.as_default():
        if train_use_generator:
          train_batch_step_count = train_data_label_pair_or_generator_count_pair[1] // batch_size
        else:
          input_batch_size = np.shape(train_data_label_pair_or_generator_count_pair[0])[0]
          if type(input_batch_size) is not int:
            input_batch_size = input_batch_size.value
          train_batch_step_count = input_batch_size // batch_size
        if validation_data_label_pair_or_generator_count_pair is not None:
          if valid_use_generator:
            valid_batch_step_count = validation_data_label_pair_or_generator_count_pair[1] // batch_size
          else:
            valid_batch_size = np.shape(validation_data_label_pair_or_generator_count_pair[0])[0]
            if type(valid_batch_size) is not int:
              valid_batch_size = valid_batch_size.value
            valid_batch_step_count = valid_batch_size // batch_size

        epoch_last_time = self.global_step.eval() // train_batch_step_count
        batch_step_last_time = self.global_step.eval() - epoch_last_time * train_batch_step_count
        for epoch_index in range(epoch_last_time, epochs):
          valid_accuracy = 0.0
          valid_losses = 0.0
          for i in range(batch_step_last_time, train_batch_step_count):
            data, label = next(train_batch_generator)
            # self.train_step.run(feed_dict={self.input: data, self.ground_truth: label, self.is_training: True})
            # real_output, output, losses, accuracy, summary = self.sess.run([self.output, self.output_layers, self.losses, self.accuracy, merged], feed_dict={self.input: data, self.ground_truth: label, self.is_training: True})
            _, losses, accuracy, summary = self.sess.run([self.train_step, self.losses, self.accuracy, self.merged], feed_dict={self.input: data, self.ground_truth: label, self.is_training: True})
            print('\repoch: %5.d, progress: %2.f, loss: %8.5g, accuracy: %5.2g'%(epoch_index+1, (i + 1) / train_batch_step_count * 100, losses, accuracy), end='')

          if epoch_index > 0:
            if epoch_index % summarize_each_epoch == 0:
              self.train_writer.add_summary(summary, self.global_step.eval())
            if epoch_index % valid_each_epoch == 0 and validation_data_label_pair_or_generator_count_pair is not None:
              valid_accuracy = 0.0
              valid_losses = 0.0
              for i in range(valid_batch_step_count):
                data, label = next(valid_batch_generator)
                losses, accuracy = self.sess.run([self.losses, self.accuracy], feed_dict={self.input: data, self.ground_truth: label, self.is_training: False})
                valid_losses += losses
                valid_accuracy = accuracy
              valid_losses /= valid_batch_step_count
              valid_accuracy /= valid_batch_step_count
            if self.model_save_path is not None and self.model_save_path != '' and epoch_index % model_save_every_epcoh == 0:
              self.saver.save(self.sess, self.model_save_path + '/' + self.name)
              print(' - Model saved', end='')
          print()

        if self.model_save_path is not None and self.model_save_path != '':
          self.saver.save(self.sess, self.model_save_path + '/' + self.name)

    except KeyboardInterrupt:
      print('\nInterrupted...\n')

  def _fit2(self, train_data_or_generator_count_pair, batch_size=50, epochs=1, shuffle=True, validation_data_or_generator_count_pair=None, valid_each_epoch=2, summarize_each_epoch=10, model_save_every_epcoh=10, verbose=True):
    assert(type(epochs) is int and type(batch_size) is int and type(valid_each_epoch) is int and type(summarize_each_epoch) is int)

    indice = []
    def batch_generator(data):
      data_shape = np.shape(data[0])
      assert(len(data) == 1)
      while True:
        if shuffle:
          indice = np.random.permutation(data_shape[0])
        else:
          indice = xrange(data_shape[0])
        for i in range(data_shape[0] // batch_size):
          target_indice = indice[i * batch_size : (i + 1) * batch_size]
          if len(self.output_fn) > 1:
            yield [data[0][j] for j in target_indice]
          else:
            yield [data[0][j] for j in target_indice]

    train_use_generator = False
    valid_use_generator = False
    if isinstance(train_data_or_generator_count_pair[0], types.GeneratorType):
      train_batch_generator = train_data_or_generator_count_pair[0]
      train_use_generator = True
    else:
      train_batch_generator = batch_generator(train_data_or_generator_count_pair)
    if validation_data_or_generator_count_pair is not None:
      if isinstance(validation_data_or_generator_count_pair[0], types.GeneratorType):
        valid_batch_generator = validation_data_or_generator_count_pair[0]
        valid_use_generator = True
      else:
        valid_batch_generator = batch_generator(validation_data_or_generator_count_pair)

    try:
      with self.sess.as_default():
        if train_use_generator:
          train_batch_step_count = train_data_or_generator_count_pair[1] // batch_size
        else:
          input_batch_size = np.shape(train_data_or_generator_count_pair[0])[0]
          if type(input_batch_size) is not int:
            input_batch_size = input_batch_size.value
          train_batch_step_count = input_batch_size // batch_size
        if validation_data_or_generator_count_pair is not None:
          if valid_use_generator:
            valid_batch_step_count = validation_data_or_generator_count_pair[1] // batch_size
          else:
            valid_batch_size = np.shape(validation_data_or_generator_count_pair[0])[0]
            if type(valid_batch_size) is not int:
              valid_batch_size = valid_batch_size.value
            valid_batch_step_count = valid_batch_size // batch_size

        epoch_last_time = self.global_step.eval() // train_batch_step_count
        batch_step_last_time = self.global_step.eval() - epoch_last_time * train_batch_step_count
        for epoch_index in range(epoch_last_time, epochs):
          valid_accuracy = 0.0
          valid_losses = 0.0
          train_accuracy = 0.0
          train_losses = 0.0
          for i in range(batch_step_last_time, train_batch_step_count):
            data = next(train_batch_generator)
            # self.train_step.run(feed_dict={self.input: data, self.is_training: True})
            # real_output, output, losses, accuracy, summary = self.sess.run([self.output, self.output_layers, self.losses, self.accuracy, merged], feed_dict={self.input: data, self.is_training: True})
            _, losses, accuracy, summary = self.sess.run([self.train_step, self.losses, self.accuracy, self.merged], feed_dict={self.input: data, self.is_training: True})
            train_accuracy += accuracy
            train_losses += losses
            print('\repoch: %5.d, progress: %2.f, loss: %8.5g, accuracy: %5.2g'%(epoch_index+1, (i + 1) / train_batch_step_count * 100, losses, accuracy), end='')
          print('\repoch: %5.d, progress: 100, loss: %8.5g, accuracy: %5.2g'%(epoch_index+1, train_losses / (train_batch_step_count - batch_step_last_time), train_accuracy / (train_batch_step_count - batch_step_last_time)), end='')
          if epoch_index > 0:
            if epoch_index % summarize_each_epoch == 0:
              self.train_writer.add_summary(summary, self.global_step.eval())
            if epoch_index % valid_each_epoch == 0 and validation_data_or_generator_count_pair is not None:
              valid_accuracy = 0.0
              valid_losses = 0.0
              for i in range(valid_batch_step_count):
                data = next(valid_batch_generator)
                losses, accuracy = self.sess.run([self.losses, self.accuracy], feed_dict={self.input: data, self.is_training: False})
                valid_losses += losses
                valid_accuracy = accuracy
              valid_losses /= valid_batch_step_count
              valid_accuracy /= valid_batch_step_count
            if self.model_save_path is not None and self.model_save_path != '' and epoch_index % model_save_every_epcoh == 0:
              self.saver.save(self.sess, self.model_save_path + '/' + self.name)
              print(' - Model saved', end='')
          print()

        if self.model_save_path is not None and self.model_save_path != '':
          self.saver.save(self.sess, self.model_save_path + '/' + self.name)

    except KeyboardInterrupt:
      print('\nInterrupted...\n')
      
  def train(self, data_label_pair, add_summary=False):
    assert(self.sess is not None)
    with self.sess.as_default():
      if add_summary:
        _, loss, summary = self.sess.run([self.train_step, self.losses, self.merged], feed_dict={self.input: data_label_pair[0], self.ground_truth: data_label_pair[1], self.is_training: True })
        self.train_writer.add_summary(summary, self.global_step.eval())
      else:
        _, loss = self.sess.run([self.train_step, self.losses], feed_dict={self.input: data_label_pair[0], self.ground_truth: data_label_pair[1], self.is_training: True })
      return loss

  def save(self):
    assert(self.saver is not None and self.sess is not None)
    with self.sess.as_default():
      if self.model_save_path is not None and self.model_save_path != '':
        self.saver.save(self.sess, self.model_save_path + '/' + self.name)

  def feedforward(self, data, target_layer=None):
    try:
      assert(self.is_continue and self.sess is not None)
      with self.sess.as_default():
        if target_layer is None:
          output = self.sess.run(self.output_layers, feed_dict={self.input: data, self.is_training: False})
        else:
          assert(type(target_layer) is str)
          target_tensor = self.sess.graph.get_tensor_by_name(target_layer + ':0')
          output = self.sess.run(target_tensor, feed_dict={self.input: data, self.is_training: False})
        # print('Outcome:')
        # print(output)
        return output

    except KeyboardInterrupt:
      print('\nInterrupted...\n')
