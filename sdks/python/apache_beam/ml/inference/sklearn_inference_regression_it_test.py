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

"""End-to-End test for Sklearn Inference using the Japanese housing regression
sample code."""

import logging
import unittest
import uuid

import pytest

from apache_beam.examples.inference import sklearn_japanese_housing_regression
from apache_beam.io.filesystems import FileSystems
from apache_beam.testing.test_pipeline import TestPipeline


def file_lines_sorted(filepath):
  with FileSystems().open(filepath) as f:
    lines = f.readlines()
  lines = [l.decode('utf-8').strip('\n') for l in lines]
  return sorted(lines)


@pytest.mark.skip
@pytest.mark.uses_sklearn
@pytest.mark.it_postcommit
class SklearnInferenceRegression(unittest.TestCase):
  def test_sklearn_regression(self):
    test_pipeline = TestPipeline(is_integration_test=False)
    input_file = 'gs://apache-beam-ml/testing/inputs/japanese_housing_test_data.csv'  # pylint: disable=line-too-long
    output_file_dir = 'gs://temp-storage-for-end-to-end-tests'
    output_file = '/'.join([output_file_dir, str(uuid.uuid4()), 'result.txt'])
    model_path = 'gs://apache-beam-ml/models/japanese_housing/'
    extra_opts = {
        'input': input_file,
        'output': output_file,
        'model_path': model_path,
    }
    sklearn_japanese_housing_regression.run(
        test_pipeline.get_full_options_as_args(**extra_opts),
        save_main_session=False)
    self.assertEqual(FileSystems().exists(output_file), True)

    expected_output_filepath = 'gs://apache-beam-ml/testing/expected_outputs/japanese_housing_subset.txt'  # pylint: disable=line-too-long
    expected = file_lines_sorted(expected_output_filepath)
    actual = file_lines_sorted(output_file)
    self.assertListEqual(expected, actual)


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  unittest.main()