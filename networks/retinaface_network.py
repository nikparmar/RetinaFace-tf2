import tensorflow as tf
from .network_utils import (
    load_weights,
    load_weights_to_network,
    relu,
    pad,
    convolution,
    batch_normalization,
    crop,
    reshape_mxnet_1,
    reshape_mxnet_2,
    upsampling
)

class RetinaFaceNetwork(object):
    """
    RetinaFace network. Can be applied to any input image size without having to be reloaded.
    """
    def __init__(self, weights_path):
        self.weights_dict = load_weights(weights_path)
        self.model = self.load_model()

    def load_model(self):
        """
        Define network structure
        Upload weights in network
        :return: tf.keras.models.Model
        """
        data                            = tf.keras.Input(dtype=tf.float32, shape=(None, None, 3), name='data')
        bn_data                         = batch_normalization(data, variance_epsilon=1.9999999494757503e-05, name='bn_data')
        conv0_pad                       = pad(bn_data, paddings=[[0, 0], [3, 3], [3, 3], [0, 0]])
        conv0                           = convolution(conv0_pad, self.weights_dict, strides=[2, 2], padding='VALID', name='conv0')
        bn0                             = batch_normalization(conv0, variance_epsilon=1.9999999494757503e-05, name='bn0')
        relu0                           = relu(bn0, name='relu0')
        pooling0_pad                    = pad(relu0, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        pooling0                        = tf.keras.layers.MaxPool2D((3, 3), (2, 2), padding='VALID', name='pooling0')(pooling0_pad)
        stage1_unit1_bn1                = batch_normalization(pooling0, variance_epsilon=1.9999999494757503e-05, name='stage1_unit1_bn1')
        stage1_unit1_relu1              = relu(stage1_unit1_bn1, name='stage1_unit1_relu1')
        stage1_unit1_conv1              = convolution(stage1_unit1_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit1_conv1')
        stage1_unit1_sc                 = convolution(stage1_unit1_relu1, self.weights_dict, strides=[1, 1], padding='VALID', name='stage1_unit1_sc')
        stage1_unit1_bn2                = batch_normalization(stage1_unit1_conv1, variance_epsilon=1.9999999494757503e-05,name='stage1_unit1_bn2')
        stage1_unit1_relu2              = relu(stage1_unit1_bn2, name='stage1_unit1_relu2')
        stage1_unit1_conv2_pad          = pad(stage1_unit1_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage1_unit1_conv2              = convolution(stage1_unit1_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit1_conv2')
        stage1_unit1_bn3                = batch_normalization(stage1_unit1_conv2, variance_epsilon=1.9999999494757503e-05,name='stage1_unit1_bn3')
        stage1_unit1_relu3              = relu(stage1_unit1_bn3, name='stage1_unit1_relu3')
        stage1_unit1_conv3              = convolution(stage1_unit1_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit1_conv3')
        plus0_v1                        = tf.keras.layers.Add()([stage1_unit1_conv3 , stage1_unit1_sc])
        stage1_unit2_bn1                = batch_normalization(plus0_v1, variance_epsilon=1.9999999494757503e-05, name='stage1_unit2_bn1')
        stage1_unit2_relu1              = relu(stage1_unit2_bn1, name='stage1_unit2_relu1')
        stage1_unit2_conv1              = convolution(stage1_unit2_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit2_conv1')
        stage1_unit2_bn2                = batch_normalization(stage1_unit2_conv1, variance_epsilon=1.9999999494757503e-05,name='stage1_unit2_bn2')
        stage1_unit2_relu2              = relu(stage1_unit2_bn2, name='stage1_unit2_relu2')
        stage1_unit2_conv2_pad          = pad(stage1_unit2_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage1_unit2_conv2              = convolution(stage1_unit2_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID', name='stage1_unit2_conv2')
        stage1_unit2_bn3                = batch_normalization(stage1_unit2_conv2, variance_epsilon=1.9999999494757503e-05,name='stage1_unit2_bn3')
        stage1_unit2_relu3              = relu(stage1_unit2_bn3, name='stage1_unit2_relu3')
        stage1_unit2_conv3              = convolution(stage1_unit2_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit2_conv3')
        plus1_v2                        = tf.keras.layers.Add()([stage1_unit2_conv3 , plus0_v1])
        stage1_unit3_bn1                = batch_normalization(plus1_v2, variance_epsilon=1.9999999494757503e-05, name='stage1_unit3_bn1')
        stage1_unit3_relu1              = relu(stage1_unit3_bn1, name='stage1_unit3_relu1')
        stage1_unit3_conv1              = convolution(stage1_unit3_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit3_conv1')
        stage1_unit3_bn2                = batch_normalization(stage1_unit3_conv1, variance_epsilon=1.9999999494757503e-05,name='stage1_unit3_bn2')
        stage1_unit3_relu2              = relu(stage1_unit3_bn2, name='stage1_unit3_relu2')
        stage1_unit3_conv2_pad          = pad(stage1_unit3_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage1_unit3_conv2              = convolution(stage1_unit3_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit3_conv2')
        stage1_unit3_bn3                = batch_normalization(stage1_unit3_conv2, variance_epsilon=1.9999999494757503e-05,name='stage1_unit3_bn3')
        stage1_unit3_relu3              = relu(stage1_unit3_bn3, name='stage1_unit3_relu3')
        stage1_unit3_conv3              = convolution(stage1_unit3_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage1_unit3_conv3')
        plus2                           = tf.keras.layers.Add()([stage1_unit3_conv3 , plus1_v2])
        stage2_unit1_bn1                = batch_normalization(plus2, variance_epsilon=1.9999999494757503e-05, name='stage2_unit1_bn1')
        stage2_unit1_relu1              = relu(stage2_unit1_bn1, name='stage2_unit1_relu1')
        stage2_unit1_conv1              = convolution(stage2_unit1_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit1_conv1')
        stage2_unit1_sc                 = convolution(stage2_unit1_relu1, self.weights_dict, strides=[2, 2], padding='VALID', name='stage2_unit1_sc')
        stage2_unit1_bn2                = batch_normalization(stage2_unit1_conv1, variance_epsilon=1.9999999494757503e-05,name='stage2_unit1_bn2')
        stage2_unit1_relu2              = relu(stage2_unit1_bn2, name='stage2_unit1_relu2')
        stage2_unit1_conv2_pad          = pad(stage2_unit1_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage2_unit1_conv2              = convolution(stage2_unit1_conv2_pad, self.weights_dict, strides=[2, 2], padding='VALID',name='stage2_unit1_conv2')
        stage2_unit1_bn3                = batch_normalization(stage2_unit1_conv2, variance_epsilon=1.9999999494757503e-05,name='stage2_unit1_bn3')
        stage2_unit1_relu3              = relu(stage2_unit1_bn3, name='stage2_unit1_relu3')
        stage2_unit1_conv3              = convolution(stage2_unit1_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit1_conv3')
        plus3                           = tf.keras.layers.Add()([stage2_unit1_conv3 , stage2_unit1_sc])
        stage2_unit2_bn1                = batch_normalization(plus3, variance_epsilon=1.9999999494757503e-05, name='stage2_unit2_bn1')
        stage2_unit2_relu1              = relu(stage2_unit2_bn1, name='stage2_unit2_relu1')
        stage2_unit2_conv1              = convolution(stage2_unit2_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit2_conv1')
        stage2_unit2_bn2                = batch_normalization(stage2_unit2_conv1, variance_epsilon=1.9999999494757503e-05,name='stage2_unit2_bn2')
        stage2_unit2_relu2              = relu(stage2_unit2_bn2, name='stage2_unit2_relu2')
        stage2_unit2_conv2_pad          = pad(stage2_unit2_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage2_unit2_conv2              = convolution(stage2_unit2_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit2_conv2')
        stage2_unit2_bn3                = batch_normalization(stage2_unit2_conv2, variance_epsilon=1.9999999494757503e-05,name='stage2_unit2_bn3')
        stage2_unit2_relu3              = relu(stage2_unit2_bn3, name='stage2_unit2_relu3')
        stage2_unit2_conv3              = convolution(stage2_unit2_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit2_conv3')
        plus4                           = tf.keras.layers.Add()([stage2_unit2_conv3 , plus3])
        stage2_unit3_bn1                = batch_normalization(plus4, variance_epsilon=1.9999999494757503e-05, name='stage2_unit3_bn1')
        stage2_unit3_relu1              = relu(stage2_unit3_bn1, name='stage2_unit3_relu1')
        stage2_unit3_conv1              = convolution(stage2_unit3_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit3_conv1')
        stage2_unit3_bn2                = batch_normalization(stage2_unit3_conv1, variance_epsilon=1.9999999494757503e-05,name='stage2_unit3_bn2')
        stage2_unit3_relu2              = relu(stage2_unit3_bn2, name='stage2_unit3_relu2')
        stage2_unit3_conv2_pad          = pad(stage2_unit3_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage2_unit3_conv2              = convolution(stage2_unit3_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit3_conv2')
        stage2_unit3_bn3                = batch_normalization(stage2_unit3_conv2, variance_epsilon=1.9999999494757503e-05,name='stage2_unit3_bn3')
        stage2_unit3_relu3              = relu(stage2_unit3_bn3, name='stage2_unit3_relu3')
        stage2_unit3_conv3              = convolution(stage2_unit3_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit3_conv3')
        plus5                           = tf.keras.layers.Add()([stage2_unit3_conv3 , plus4])
        stage2_unit4_bn1                = batch_normalization(plus5, variance_epsilon=1.9999999494757503e-05, name='stage2_unit4_bn1')
        stage2_unit4_relu1              = relu(stage2_unit4_bn1, name='stage2_unit4_relu1')
        stage2_unit4_conv1              = convolution(stage2_unit4_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit4_conv1')
        stage2_unit4_bn2                = batch_normalization(stage2_unit4_conv1, variance_epsilon=1.9999999494757503e-05,name='stage2_unit4_bn2')
        stage2_unit4_relu2              = relu(stage2_unit4_bn2, name='stage2_unit4_relu2')
        stage2_unit4_conv2_pad          = pad(stage2_unit4_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage2_unit4_conv2              = convolution(stage2_unit4_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit4_conv2')
        stage2_unit4_bn3                = batch_normalization(stage2_unit4_conv2, variance_epsilon=1.9999999494757503e-05,name='stage2_unit4_bn3')
        stage2_unit4_relu3              = relu(stage2_unit4_bn3, name='stage2_unit4_relu3')
        stage2_unit4_conv3              = convolution(stage2_unit4_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage2_unit4_conv3')
        plus6                           = tf.keras.layers.Add()([stage2_unit4_conv3 , plus5])
        stage3_unit1_bn1                = batch_normalization(plus6, variance_epsilon=1.9999999494757503e-05, name='stage3_unit1_bn1')
        stage3_unit1_relu1              = relu(stage3_unit1_bn1, name='stage3_unit1_relu1')
        stage3_unit1_conv1              = convolution(stage3_unit1_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit1_conv1')
        stage3_unit1_sc                 = convolution(stage3_unit1_relu1, self.weights_dict, strides=[2, 2], padding='VALID', name='stage3_unit1_sc')
        stage3_unit1_bn2                = batch_normalization(stage3_unit1_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit1_bn2')
        stage3_unit1_relu2              = relu(stage3_unit1_bn2, name='stage3_unit1_relu2')
        stage3_unit1_conv2_pad          = pad(stage3_unit1_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit1_conv2              = convolution(stage3_unit1_conv2_pad, self.weights_dict, strides=[2, 2], padding='VALID',name='stage3_unit1_conv2')
        ssh_m1_red_conv                 = convolution(stage3_unit1_relu2, self.weights_dict, strides=[1, 1], padding='VALID', name='ssh_m1_red_conv')
        stage3_unit1_bn3                = batch_normalization(stage3_unit1_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit1_bn3')
        ssh_m1_red_conv_bn              = batch_normalization(ssh_m1_red_conv, variance_epsilon=1.9999999494757503e-05,name='ssh_m1_red_conv_bn')
        stage3_unit1_relu3              = relu(stage3_unit1_bn3, name='stage3_unit1_relu3')
        ssh_m1_red_conv_relu            = relu(ssh_m1_red_conv_bn, name='ssh_m1_red_conv_relu')
        stage3_unit1_conv3              = convolution(stage3_unit1_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit1_conv3')
        plus7                           = tf.keras.layers.Add()([stage3_unit1_conv3 , stage3_unit1_sc])
        stage3_unit2_bn1                = batch_normalization(plus7, variance_epsilon=1.9999999494757503e-05, name='stage3_unit2_bn1')
        stage3_unit2_relu1              = relu(stage3_unit2_bn1, name='stage3_unit2_relu1')
        stage3_unit2_conv1              = convolution(stage3_unit2_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit2_conv1')
        stage3_unit2_bn2                = batch_normalization(stage3_unit2_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit2_bn2')
        stage3_unit2_relu2              = relu(stage3_unit2_bn2, name='stage3_unit2_relu2')
        stage3_unit2_conv2_pad          = pad(stage3_unit2_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit2_conv2              = convolution(stage3_unit2_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit2_conv2')
        stage3_unit2_bn3                = batch_normalization(stage3_unit2_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit2_bn3')
        stage3_unit2_relu3              = relu(stage3_unit2_bn3, name='stage3_unit2_relu3')
        stage3_unit2_conv3              = convolution(stage3_unit2_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit2_conv3')
        plus8                           = tf.keras.layers.Add()([stage3_unit2_conv3 , plus7])
        stage3_unit3_bn1                = batch_normalization(plus8, variance_epsilon=1.9999999494757503e-05, name='stage3_unit3_bn1')
        stage3_unit3_relu1              = relu(stage3_unit3_bn1, name='stage3_unit3_relu1')
        stage3_unit3_conv1              = convolution(stage3_unit3_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit3_conv1')
        stage3_unit3_bn2                = batch_normalization(stage3_unit3_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit3_bn2')
        stage3_unit3_relu2              = relu(stage3_unit3_bn2, name='stage3_unit3_relu2')
        stage3_unit3_conv2_pad          = pad(stage3_unit3_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit3_conv2              = convolution(stage3_unit3_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit3_conv2')
        stage3_unit3_bn3                = batch_normalization(stage3_unit3_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit3_bn3')
        stage3_unit3_relu3              = relu(stage3_unit3_bn3, name='stage3_unit3_relu3')
        stage3_unit3_conv3              = convolution(stage3_unit3_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit3_conv3')
        plus9                           = tf.keras.layers.Add()([stage3_unit3_conv3 , plus8])
        stage3_unit4_bn1                = batch_normalization(plus9, variance_epsilon=1.9999999494757503e-05, name='stage3_unit4_bn1')
        stage3_unit4_relu1              = relu(stage3_unit4_bn1, name='stage3_unit4_relu1')
        stage3_unit4_conv1              = convolution(stage3_unit4_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit4_conv1')
        stage3_unit4_bn2                = batch_normalization(stage3_unit4_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit4_bn2')
        stage3_unit4_relu2              = relu(stage3_unit4_bn2, name='stage3_unit4_relu2')
        stage3_unit4_conv2_pad          = pad(stage3_unit4_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit4_conv2              = convolution(stage3_unit4_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit4_conv2')
        stage3_unit4_bn3                = batch_normalization(stage3_unit4_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit4_bn3')
        stage3_unit4_relu3              = relu(stage3_unit4_bn3, name='stage3_unit4_relu3')
        stage3_unit4_conv3              = convolution(stage3_unit4_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit4_conv3')
        plus10                          = tf.keras.layers.Add()([stage3_unit4_conv3 , plus9])
        stage3_unit5_bn1                = batch_normalization(plus10, variance_epsilon=1.9999999494757503e-05, name='stage3_unit5_bn1')
        stage3_unit5_relu1              = relu(stage3_unit5_bn1, name='stage3_unit5_relu1')
        stage3_unit5_conv1              = convolution(stage3_unit5_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit5_conv1')
        stage3_unit5_bn2                = batch_normalization(stage3_unit5_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit5_bn2')
        stage3_unit5_relu2              = relu(stage3_unit5_bn2, name='stage3_unit5_relu2')
        stage3_unit5_conv2_pad          = pad(stage3_unit5_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit5_conv2              = convolution(stage3_unit5_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit5_conv2')
        stage3_unit5_bn3                = batch_normalization(stage3_unit5_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit5_bn3')
        stage3_unit5_relu3              = relu(stage3_unit5_bn3, name='stage3_unit5_relu3')
        stage3_unit5_conv3              = convolution(stage3_unit5_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit5_conv3')
        plus11                          = tf.keras.layers.Add()([stage3_unit5_conv3 , plus10])
        stage3_unit6_bn1                = batch_normalization(plus11, variance_epsilon=1.9999999494757503e-05, name='stage3_unit6_bn1')
        stage3_unit6_relu1              = relu(stage3_unit6_bn1, name='stage3_unit6_relu1')
        stage3_unit6_conv1              = convolution(stage3_unit6_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit6_conv1')
        stage3_unit6_bn2                = batch_normalization(stage3_unit6_conv1, variance_epsilon=1.9999999494757503e-05,name='stage3_unit6_bn2')
        stage3_unit6_relu2              = relu(stage3_unit6_bn2, name='stage3_unit6_relu2')
        stage3_unit6_conv2_pad          = pad(stage3_unit6_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage3_unit6_conv2              = convolution(stage3_unit6_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit6_conv2')
        stage3_unit6_bn3                = batch_normalization(stage3_unit6_conv2, variance_epsilon=1.9999999494757503e-05,name='stage3_unit6_bn3')
        stage3_unit6_relu3              = relu(stage3_unit6_bn3, name='stage3_unit6_relu3')
        stage3_unit6_conv3              = convolution(stage3_unit6_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage3_unit6_conv3')
        plus12                          = tf.keras.layers.Add()([stage3_unit6_conv3 , plus11])
        stage4_unit1_bn1                = batch_normalization(plus12, variance_epsilon=1.9999999494757503e-05, name='stage4_unit1_bn1')
        stage4_unit1_relu1              = relu(stage4_unit1_bn1, name='stage4_unit1_relu1')
        stage4_unit1_conv1              = convolution(stage4_unit1_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit1_conv1')
        stage4_unit1_sc                 = convolution(stage4_unit1_relu1, self.weights_dict, strides=[2, 2], padding='VALID', name='stage4_unit1_sc')
        stage4_unit1_bn2                = batch_normalization(stage4_unit1_conv1, variance_epsilon=1.9999999494757503e-05,name='stage4_unit1_bn2')
        stage4_unit1_relu2              = relu(stage4_unit1_bn2, name='stage4_unit1_relu2')
        stage4_unit1_conv2_pad          = pad(stage4_unit1_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage4_unit1_conv2              = convolution(stage4_unit1_conv2_pad, self.weights_dict, strides=[2, 2], padding='VALID',name='stage4_unit1_conv2')
        ssh_c2_lateral                  = convolution(stage4_unit1_relu2, self.weights_dict, strides=[1, 1], padding='VALID', name='ssh_c2_lateral')
        stage4_unit1_bn3                = batch_normalization(stage4_unit1_conv2, variance_epsilon=1.9999999494757503e-05,name='stage4_unit1_bn3')
        ssh_c2_lateral_bn               = batch_normalization(ssh_c2_lateral, variance_epsilon=1.9999999494757503e-05,name='ssh_c2_lateral_bn')
        stage4_unit1_relu3              = relu(stage4_unit1_bn3, name='stage4_unit1_relu3')
        ssh_c2_lateral_relu             = relu(ssh_c2_lateral_bn, name='ssh_c2_lateral_relu')
        stage4_unit1_conv3              = convolution(stage4_unit1_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit1_conv3')
        plus13                          = tf.keras.layers.Add()([stage4_unit1_conv3 , stage4_unit1_sc])
        stage4_unit2_bn1                = batch_normalization(plus13, variance_epsilon=1.9999999494757503e-05, name='stage4_unit2_bn1')
        stage4_unit2_relu1              = relu(stage4_unit2_bn1, name='stage4_unit2_relu1')
        stage4_unit2_conv1              = convolution(stage4_unit2_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit2_conv1')
        stage4_unit2_bn2                = batch_normalization(stage4_unit2_conv1, variance_epsilon=1.9999999494757503e-05,name='stage4_unit2_bn2')
        stage4_unit2_relu2              = relu(stage4_unit2_bn2, name='stage4_unit2_relu2')
        stage4_unit2_conv2_pad          = pad(stage4_unit2_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage4_unit2_conv2              = convolution(stage4_unit2_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit2_conv2')
        stage4_unit2_bn3                = batch_normalization(stage4_unit2_conv2, variance_epsilon=1.9999999494757503e-05,name='stage4_unit2_bn3')
        stage4_unit2_relu3              = relu(stage4_unit2_bn3, name='stage4_unit2_relu3')
        stage4_unit2_conv3              = convolution(stage4_unit2_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit2_conv3')
        plus14                          = tf.keras.layers.Add()([stage4_unit2_conv3 , plus13])
        stage4_unit3_bn1                = batch_normalization(plus14, variance_epsilon=1.9999999494757503e-05, name='stage4_unit3_bn1')
        stage4_unit3_relu1              = relu(stage4_unit3_bn1, name='stage4_unit3_relu1')
        stage4_unit3_conv1              = convolution(stage4_unit3_relu1, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit3_conv1')
        stage4_unit3_bn2                = batch_normalization(stage4_unit3_conv1, variance_epsilon=1.9999999494757503e-05,name='stage4_unit3_bn2')
        stage4_unit3_relu2              = relu(stage4_unit3_bn2, name='stage4_unit3_relu2')
        stage4_unit3_conv2_pad          = pad(stage4_unit3_relu2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        stage4_unit3_conv2              = convolution(stage4_unit3_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit3_conv2')
        stage4_unit3_bn3                = batch_normalization(stage4_unit3_conv2, variance_epsilon=1.9999999494757503e-05,name='stage4_unit3_bn3')
        stage4_unit3_relu3              = relu(stage4_unit3_bn3, name='stage4_unit3_relu3')
        stage4_unit3_conv3              = convolution(stage4_unit3_relu3, self.weights_dict, strides=[1, 1], padding='VALID',name='stage4_unit3_conv3')
        plus15                          = tf.keras.layers.Add()([stage4_unit3_conv3 , plus14])
        bn1                             = batch_normalization(plus15, variance_epsilon=1.9999999494757503e-05, name='bn1')
        relu1                           = relu(bn1, name='relu1')
        ssh_c3_lateral                  = convolution(relu1, self.weights_dict, strides=[1, 1], padding='VALID', name='ssh_c3_lateral')
        ssh_c3_lateral_bn               = batch_normalization(ssh_c3_lateral, variance_epsilon=1.9999999494757503e-05,name='ssh_c3_lateral_bn')
        ssh_c3_lateral_relu             = relu(ssh_c3_lateral_bn, name='ssh_c3_lateral_relu')
        ssh_m3_det_conv1_pad            = pad(ssh_c3_lateral_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m3_det_conv1                = convolution(ssh_m3_det_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m3_det_conv1')
        ssh_m3_det_context_conv1_pad    = pad(ssh_c3_lateral_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m3_det_context_conv1        = convolution(ssh_m3_det_context_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m3_det_context_conv1')
        ssh_c3_up                       = upsampling(ssh_c3_lateral_relu, (2, 2), "ssh_c3_up")
        ssh_m3_det_conv1_bn             = batch_normalization(ssh_m3_det_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m3_det_conv1_bn')
        ssh_m3_det_context_conv1_bn     = batch_normalization(ssh_m3_det_context_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m3_det_context_conv1_bn')
        crop0                           = crop(ssh_c3_up, ssh_c2_lateral_relu, "crop0")
        ssh_m3_det_context_conv1_relu   = relu(ssh_m3_det_context_conv1_bn, name='ssh_m3_det_context_conv1_relu')
        plus0_v2                        = tf.keras.layers.Add()([ssh_c2_lateral_relu , crop0])
        ssh_m3_det_context_conv2_pad    = pad(ssh_m3_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m3_det_context_conv2        = convolution(ssh_m3_det_context_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m3_det_context_conv2')
        ssh_m3_det_context_conv3_1_pad  = pad(ssh_m3_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m3_det_context_conv3_1      = convolution(ssh_m3_det_context_conv3_1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m3_det_context_conv3_1')
        ssh_c2_aggr_pad                 = pad(plus0_v2, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_c2_aggr                     = convolution(ssh_c2_aggr_pad, self.weights_dict, strides=[1, 1], padding='VALID', name='ssh_c2_aggr')
        ssh_m3_det_context_conv2_bn     = batch_normalization(ssh_m3_det_context_conv2, variance_epsilon=1.9999999494757503e-05,name='ssh_m3_det_context_conv2_bn')
        ssh_m3_det_context_conv3_1_bn   = batch_normalization(ssh_m3_det_context_conv3_1,variance_epsilon=1.9999999494757503e-05,name='ssh_m3_det_context_conv3_1_bn')
        ssh_c2_aggr_bn                  = batch_normalization(ssh_c2_aggr, variance_epsilon=1.9999999494757503e-05, name='ssh_c2_aggr_bn')
        ssh_m3_det_context_conv3_1_relu = relu(ssh_m3_det_context_conv3_1_bn, name='ssh_m3_det_context_conv3_1_relu')
        ssh_c2_aggr_relu                = relu(ssh_c2_aggr_bn, name='ssh_c2_aggr_relu')
        ssh_m3_det_context_conv3_2_pad  = pad(ssh_m3_det_context_conv3_1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m3_det_context_conv3_2      = convolution(ssh_m3_det_context_conv3_2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m3_det_context_conv3_2')
        ssh_m2_det_conv1_pad            = pad(ssh_c2_aggr_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m2_det_conv1                = convolution(ssh_m2_det_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m2_det_conv1')
        ssh_m2_det_context_conv1_pad    = pad(ssh_c2_aggr_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m2_det_context_conv1        = convolution(ssh_m2_det_context_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m2_det_context_conv1')
        ssh_m2_red_up                   = upsampling(ssh_c2_aggr_relu, (2, 2), "ssh_m2_red_up")
        ssh_m3_det_context_conv3_2_bn   = batch_normalization(ssh_m3_det_context_conv3_2,variance_epsilon=1.9999999494757503e-05,name='ssh_m3_det_context_conv3_2_bn')
        ssh_m2_det_conv1_bn             = batch_normalization(ssh_m2_det_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m2_det_conv1_bn')
        ssh_m2_det_context_conv1_bn     = batch_normalization(ssh_m2_det_context_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m2_det_context_conv1_bn')
        crop1                           = crop(ssh_m2_red_up, ssh_m1_red_conv_relu, "crop1")
        ssh_m3_det_concat               = tf.keras.layers.concatenate([ssh_m3_det_conv1_bn, ssh_m3_det_context_conv2_bn, ssh_m3_det_context_conv3_2_bn], 3, name='ssh_m3_det_concat')
        ssh_m2_det_context_conv1_relu   = relu(ssh_m2_det_context_conv1_bn, name='ssh_m2_det_context_conv1_relu')
        plus1_v1                        = tf.keras.layers.Add()([ssh_m1_red_conv_relu , crop1])
        ssh_m3_det_concat_relu          = relu(ssh_m3_det_concat, name='ssh_m3_det_concat_relu')
        ssh_m2_det_context_conv2_pad    = pad(ssh_m2_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m2_det_context_conv2        = convolution(ssh_m2_det_context_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m2_det_context_conv2')
        ssh_m2_det_context_conv3_1_pad  = pad(ssh_m2_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m2_det_context_conv3_1      = convolution(ssh_m2_det_context_conv3_1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m2_det_context_conv3_1')
        ssh_c1_aggr_pad                 = pad(plus1_v1, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_c1_aggr                     = convolution(ssh_c1_aggr_pad, self.weights_dict, strides=[1, 1], padding='VALID', name='ssh_c1_aggr')
        face_rpn_cls_score_stride32     = convolution(ssh_m3_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_cls_score_stride32')
        face_rpn_cls_score_reshape_stride32 = reshape_mxnet_1(face_rpn_cls_score_stride32, "face_rpn_cls_score_reshape_stride32")
        face_rpn_bbox_pred_stride32     = convolution(ssh_m3_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_bbox_pred_stride32')
        face_rpn_landmark_pred_stride32 = convolution(ssh_m3_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_landmark_pred_stride32')
        ssh_m2_det_context_conv2_bn     = batch_normalization(ssh_m2_det_context_conv2, variance_epsilon=1.9999999494757503e-05,name='ssh_m2_det_context_conv2_bn')
        ssh_m2_det_context_conv3_1_bn   = batch_normalization(ssh_m2_det_context_conv3_1,variance_epsilon=1.9999999494757503e-05,name='ssh_m2_det_context_conv3_1_bn')
        ssh_c1_aggr_bn                  = batch_normalization(ssh_c1_aggr, variance_epsilon=1.9999999494757503e-05, name='ssh_c1_aggr_bn')
        ssh_m2_det_context_conv3_1_relu = relu(ssh_m2_det_context_conv3_1_bn, name='ssh_m2_det_context_conv3_1_relu')
        ssh_c1_aggr_relu                = relu(ssh_c1_aggr_bn, name='ssh_c1_aggr_relu')
        face_rpn_cls_prob_stride32      = tf.keras.layers.Softmax(name = 'face_rpn_cls_prob_stride32')(face_rpn_cls_score_reshape_stride32)
        face_rpn_cls_prob_reshape_stride32 = reshape_mxnet_2(face_rpn_cls_prob_stride32, "face_rpn_cls_prob_reshape_stride32")
        ssh_m2_det_context_conv3_2_pad  = pad(ssh_m2_det_context_conv3_1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m2_det_context_conv3_2      = convolution(ssh_m2_det_context_conv3_2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m2_det_context_conv3_2')
        ssh_m1_det_conv1_pad            = pad(ssh_c1_aggr_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m1_det_conv1                = convolution(ssh_m1_det_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m1_det_conv1')
        ssh_m1_det_context_conv1_pad    = pad(ssh_c1_aggr_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m1_det_context_conv1        = convolution(ssh_m1_det_context_conv1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m1_det_context_conv1')
        ssh_m2_det_context_conv3_2_bn   = batch_normalization(ssh_m2_det_context_conv3_2,variance_epsilon=1.9999999494757503e-05,name='ssh_m2_det_context_conv3_2_bn')
        ssh_m1_det_conv1_bn             = batch_normalization(ssh_m1_det_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m1_det_conv1_bn')
        ssh_m1_det_context_conv1_bn     = batch_normalization(ssh_m1_det_context_conv1, variance_epsilon=1.9999999494757503e-05,name='ssh_m1_det_context_conv1_bn')
        ssh_m2_det_concat               = tf.keras.layers.concatenate([ssh_m2_det_conv1_bn, ssh_m2_det_context_conv2_bn, ssh_m2_det_context_conv3_2_bn], 3, name='ssh_m2_det_concat')
        ssh_m1_det_context_conv1_relu   = relu(ssh_m1_det_context_conv1_bn, name='ssh_m1_det_context_conv1_relu')
        ssh_m2_det_concat_relu          = relu(ssh_m2_det_concat, name='ssh_m2_det_concat_relu')
        ssh_m1_det_context_conv2_pad    = pad(ssh_m1_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m1_det_context_conv2        = convolution(ssh_m1_det_context_conv2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m1_det_context_conv2')
        ssh_m1_det_context_conv3_1_pad  = pad(ssh_m1_det_context_conv1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m1_det_context_conv3_1      = convolution(ssh_m1_det_context_conv3_1_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m1_det_context_conv3_1')
        face_rpn_cls_score_stride16     = convolution(ssh_m2_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_cls_score_stride16')
        face_rpn_cls_score_reshape_stride16 = self.reshape_mxnet_1(face_rpn_cls_score_stride16, "face_rpn_cls_score_reshape_stride16")
        face_rpn_bbox_pred_stride16     = convolution(ssh_m2_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_bbox_pred_stride16')
        face_rpn_landmark_pred_stride16 = convolution(ssh_m2_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_landmark_pred_stride16')
        ssh_m1_det_context_conv2_bn     = batch_normalization(ssh_m1_det_context_conv2, variance_epsilon=1.9999999494757503e-05,name='ssh_m1_det_context_conv2_bn')
        ssh_m1_det_context_conv3_1_bn   = batch_normalization(ssh_m1_det_context_conv3_1,variance_epsilon=1.9999999494757503e-05,name='ssh_m1_det_context_conv3_1_bn')
        ssh_m1_det_context_conv3_1_relu = relu(ssh_m1_det_context_conv3_1_bn, name='ssh_m1_det_context_conv3_1_relu')
        face_rpn_cls_prob_stride16      = tf.keras.layers.Softmax(name = 'face_rpn_cls_prob_stride16')(face_rpn_cls_score_reshape_stride16)
        face_rpn_cls_prob_reshape_stride16 = self.reshape_mxnet_2(face_rpn_cls_prob_stride16, "face_rpn_cls_prob_reshape_stride16")
        ssh_m1_det_context_conv3_2_pad  = pad(ssh_m1_det_context_conv3_1_relu, paddings=[[0, 0], [1, 1], [1, 1], [0, 0]])
        ssh_m1_det_context_conv3_2      = convolution(ssh_m1_det_context_conv3_2_pad, self.weights_dict, strides=[1, 1], padding='VALID',name='ssh_m1_det_context_conv3_2')
        ssh_m1_det_context_conv3_2_bn   = batch_normalization(ssh_m1_det_context_conv3_2,variance_epsilon=1.9999999494757503e-05,name='ssh_m1_det_context_conv3_2_bn')
        ssh_m1_det_concat               = tf.keras.layers.concatenate([ssh_m1_det_conv1_bn, ssh_m1_det_context_conv2_bn, ssh_m1_det_context_conv3_2_bn], 3, name='ssh_m1_det_concat')
        ssh_m1_det_concat_relu          = relu(ssh_m1_det_concat, name='ssh_m1_det_concat_relu')
        face_rpn_cls_score_stride8      = convolution(ssh_m1_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_cls_score_stride8')
        face_rpn_cls_score_reshape_stride8 = self.reshape_mxnet_1(face_rpn_cls_score_stride8, "face_rpn_cls_score_reshape_stride8")
        face_rpn_bbox_pred_stride8      = convolution(ssh_m1_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_bbox_pred_stride8')
        face_rpn_landmark_pred_stride8  = convolution(ssh_m1_det_concat_relu, self.weights_dict, strides=[1, 1], padding='VALID',name='face_rpn_landmark_pred_stride8')
        face_rpn_cls_prob_stride8       = tf.keras.layers.Softmax(name = 'face_rpn_cls_prob_stride8')(face_rpn_cls_score_reshape_stride8)
        face_rpn_cls_prob_reshape_stride8 = self.reshape_mxnet_2(face_rpn_cls_prob_stride8, "face_rpn_cls_prob_reshape_stride8")

        model = tf.keras.models.Model(inputs=data,
                                      outputs=[face_rpn_cls_prob_reshape_stride32,
                                               face_rpn_bbox_pred_stride32,
                                               face_rpn_landmark_pred_stride32,
                                               face_rpn_cls_prob_reshape_stride16,
                                               face_rpn_bbox_pred_stride16,
                                               face_rpn_landmark_pred_stride16,
                                               face_rpn_cls_prob_reshape_stride8,
                                               face_rpn_bbox_pred_stride8,
                                               face_rpn_landmark_pred_stride8
                                               ])

        return load_weights_to_network(model, self.weights_dict)