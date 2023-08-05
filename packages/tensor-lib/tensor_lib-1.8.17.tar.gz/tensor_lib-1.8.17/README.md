# TensorLib 
[![pipeline status](http://petel-home.ddns.net/gitlab/hkust-fyp/tensor_lib/badges/master/pipeline.svg)](http://petel-home.ddns.net/gitlab/hkust-fyp/tensor_lib/commits/master)  
Simplified version of tensorflow without changing internal structure of Tensorflow

## Requirements
Python
- Tensorflow
- Numpy

## Installation
```
$ sudo pip install tensor-lib
```

## TODOs
- Layer
    - Types
        - Convlutional
            - [x] Convolutional
            - [x] Deconvolutional
        - [x] RNN (Testing)
            - [ ] LSTM
            - [ ] GRU
        - Pooling
            - [x] Max Pooling
            - [x] Avg Pooling
            - [x] L2 Pooling
            - [x] UpSampling
            - [ ] Unpooling
        - Noise
            - [x] Gaussian
            - [x] Mask
        - Fully Connected
            - [x] Auto flatten
            - [x] Auto transpose the reused weight from another layer
        - Coordinate
            - [x] Spatial Softmax
            - [x] Top-K
        - Operation
            - [x] Reshape
            - [x] Transpose
            - [x] Concat
        - [x] Lambda
        
    - Attributes
        - Normalization
            - [x] Batch Normalization
            - [x] Local Contrast Normalization
        - [x] Dropout
        - [x] Weight sharing
        - [ ] Tensorboard support

- Model
    - [x] Support multiple output layers
    - [x] Customize output function
    - [x] Customize accuracy function
    - [x] Model training
    - [x] Update loss, accuracy on Tensorboard
    - [x] Continue last save
    - [x] Support generator as input
    - [x] Cusomize loss function
    - [x] Support layer as ground truth for unsupervised learning
