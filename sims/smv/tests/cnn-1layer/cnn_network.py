#!/usr/bin/env python

"""Example for creating the CIFAR10-CNN network."""

import numpy as np
import smaug as sg

def generate_random_data(shape):
  r = np.random.RandomState(1234)
  return (r.rand(*shape) * 0.005).astype(np.float16)

def create_cnn_model():
  with sg.Graph(name="cnn_smv", backend="SMV",
                mem_policy=sg.AllDma) as graph:
    input_tensor = sg.Tensor(
        data_layout=sg.NHWC, tensor_data=generate_random_data((1, 32, 32, 64)))
    conv0_tensor = sg.Tensor(
        data_layout=sg.NHWC, tensor_data=generate_random_data((108, 3, 3, 64)))
    bn0_mean_tensor = sg.Tensor(
        data_layout=sg.NC, tensor_data=generate_random_data((1, 32)))
    bn0_var_tensor = sg.Tensor(
        data_layout=sg.NC, tensor_data=generate_random_data((1, 32)))
    bn0_gamma_tensor = sg.Tensor(
        data_layout=sg.NC, tensor_data=generate_random_data((1, 32)))
    bn0_beta_tensor = sg.Tensor(
        data_layout=sg.NC, tensor_data=generate_random_data((1, 32)))


    act = sg.input_data(input_tensor)
    act = sg.nn.convolution(
        act, conv0_tensor, stride=[1, 1], padding="same", activation="relu")
    # act = sg.nn.batch_norm(
    #     act, bn0_mean_tensor, bn0_var_tensor, bn0_gamma_tensor, bn0_beta_tensor)
    return graph

if __name__ != "main":
  graph = create_cnn_model()
  graph.print_summary()
  graph.write_graph()
