# Copyright (c) 2018 Intel Corporation
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
import os
from collections import UserString
from typing import List

try:
    import pkg_resources
except ImportError:
    # When running from pex use vendored library from pex.
    from pex.vendor._vendored.setuptools import pkg_resources

from wca.runners import detection
from wca.runners import allocation
from wca.runners import measurement
from wca.runners.measurement import TaskLabelRegexGenerator
from wca.extra import static_allocator, aep_detector
from wca import config
from wca import detectors
from wca import allocators
from wca import mesos
from wca import kubernetes
from wca import storage
from wca import storage_http
from wca.extra import static_node
from wca import security
from wca.metrics import DefaultTaskDerivedMetricsGeneratorFactory
from wca.perf_pmu import DefaultPlatformDerivedMetricsGeneratorsFactory


class Env(UserString):
    """Env class allows using environment variables as values in wca config"""

    def __init__(self, name: str):
        seq = os.environ.get(name, "")
        super().__init__(seq)


def register_components(extra_components: List[str]):
    config.register(detection.DetectionRunner)
    config.register(allocation.AllocationRunner)
    config.register(measurement.MeasurementRunner)
    config.register(mesos.MesosNode)
    config.register(kubernetes.KubernetesNode)
    config.register(storage.LogStorage)
    config.register(storage.KafkaStorage)
    config.register(storage.FilterStorage)
    config.register(storage_http.HTTPStorage)
    config.register(detectors.NOPAnomalyDetector)
    config.register(allocators.NOPAllocator)
    config.register(allocators.AllocationConfiguration)
    config.register(kubernetes.CgroupDriverType)
    config.register(static_node.StaticNode)
    config.register(static_allocator.StaticAllocator)
    config.register(security.SSL)
    config.register(TaskLabelRegexGenerator)
    config.register(aep_detector.AEPDetector)
    config.register(DefaultTaskDerivedMetricsGeneratorFactory)
    config.register(DefaultPlatformDerivedMetricsGeneratorsFactory)
    config.register(Env)

    for component in extra_components:
        # Load external class ignored its requirements.
        ep = pkg_resources.EntryPoint.parse('external_cls=%s' % component)
        cls = ep.resolve()
        config.register(cls)
