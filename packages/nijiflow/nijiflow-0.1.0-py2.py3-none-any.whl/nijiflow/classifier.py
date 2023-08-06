# Copyright 2017 Hazuki Tachibana
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow as tf

_MODEL_NAME = 'nijinet_v1_1.0_224.graphdef.pb'
_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', _MODEL_NAME)


class Classifier(object):
    def __init__(self):
        with tf.Graph().as_default() as graph:
            with open(_MODEL_PATH, 'rb') as f:
                graph_def = tf.GraphDef.FromString(f.read())
            tf.import_graph_def(graph_def, name='')
        self._graph = graph
        self._input_tensor = graph.get_operation_by_name('input').outputs[0]
        self._output_tensor = (
            graph.get_operation_by_name('MobilenetV1/Predictions/Reshape_1')
            .outputs[0])
        self._image_size = (self._input_tensor.shape[1].value,
                            self._input_tensor.shape[2].value)

    def classify(self, image_paths):
        batch = self._load_images(image_paths)
        with tf.Session(graph=self._graph) as session:
            results = session.run(self._output_tensor, {
                self._input_tensor: batch
            })
        return results[:, 1].tolist()

    def _load_images(self, image_paths):
        with tf.Graph().as_default():
            image_readers = []
            for image_path in image_paths:
                raw_reader = tf.image.decode_image(
                    tf.read_file(image_path), channels=3)
                normalizer = tf.cast(raw_reader, tf.float32) / 255 * 2 - 1
                dim_expander = tf.expand_dims(normalizer, 0)
                resizer = tf.image.resize_bilinear(dim_expander,
                                                   self._image_size)
                image_readers.append(resizer)
            batch_reader = tf.concat(image_readers, axis=0)
            with tf.Session() as session:
                batch = session.run(batch_reader)
        return batch
