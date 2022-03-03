#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Any
from typing import Iterable
import unittest

import apache_beam as beam
import apache_beam.ml.inference.base as base
from apache_beam.metrics.metric import MetricsFilter
from apache_beam.ml.inference.api import PredictionResult
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.testing.test_pipeline import TestPipeline


class MockModel:
  def predict(self, example: int):
    return example + 1


class MockInferenceRunner(base.InferenceRunner):
  def run_inference(self, batch: Any, model: Any) -> Iterable[PredictionResult]:
    for example in batch:
      yield model.predict(example)


class MockModelLoader(base.ModelLoader):
  def load_model(self):
    return MockModel()


class ExtractInferences(beam.DoFn):
  def process(self, prediction_result):
    yield prediction_result.inference


class BaseTest(unittest.TestCase):
  def setup(self):
    pass

  def test_run_inference_impl_simple_examples(self):
    with TestPipeline() as pipeline:
      examples = [1, 5, 3, 10]
      expected = [
          PredictionResult(example, example + 1) for example in examples
      ]
      pcoll = pipeline | 'start' >> beam.Create(examples)
      actual = pcoll | base.RunInferenceImpl(
          MockModelLoader(), MockInferenceRunner())
      assert_that(actual, equal_to(expected), label='assert:inferences')

  def test_run_inference_impl_with_keyed_examples(self):
    with TestPipeline() as pipeline:
      examples = [1, 5, 3, 10]
      keyed_examples = [(i, example) for i, example in enumerate(examples)]
      expected = [(i, PredictionResult(example, example + 1)) for i,
                  example in enumerate(examples)]
      pcoll = pipeline | 'start' >> beam.Create(keyed_examples)
      actual = pcoll | base.RunInferenceImpl(
          MockModelLoader(), MockInferenceRunner())
      assert_that(actual, equal_to(expected), label='assert:inferences')

  def test_num_inferences_metrics_counted(self):
    pipeline = TestPipeline()
    examples = [1, 5, 3, 10]
    pcoll = pipeline | 'start' >> beam.Create(examples)
    actual = pcoll | base.RunInferenceImpl(
        MockModelLoader(), MockInferenceRunner())
    res = pipeline.run()
    res.wait_until_finish()

    metric_results = (
        res.metrics().query(MetricsFilter().with_name('num_inferences')))
    num_inferences_counter = metric_results['counters'][0]
    self.assertEqual(num_inferences_counter.committed, 4)
