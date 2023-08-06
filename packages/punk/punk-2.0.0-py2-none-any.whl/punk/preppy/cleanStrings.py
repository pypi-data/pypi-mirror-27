import pandas as pd
from typing import List

from primitive_interfaces.featurization import FeaturizationTransformerPrimitiveBase
from d3m_metadata import container, hyperparams, metadata, params

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame

class Hyperparams(hyperparams.Hyperparams):
    pass

class CleanStrings(FeaturizationTransformerPrimitiveBase[Inputs, Outputs, Hyperparams]):
    __author__ = 'Distil'
    metadata = metadata.PrimitiveMetadata({
        "id": "fc6bf33a-f3e0-3496-aa47-9a40289661bc",
        "version": "2.0.0",
        "schema": "https://metadata.datadrivendiscovery.org/schemas/v0/primitive.json",
        "description": "Clean up string fields",
        "name": "Clean strings",
        "python_path": "d3m.primitives.distil.CleanStrings",
        "original_python_path": "punk.preppy.cleanStrings.CleanStrings",
        "algorithm_types": ["ADAPTIVE_ALGORITHM"],
        "installation": [{
            "package": "punk",
            "type": "PIP",
            "version": "2.0.0"
        }],
        "primitive_code": {
            "class_type_arguments": {},
            "interfaces_version": "2017.12.27",
            "interfaces": ["primitives_interfaces.featurization.FeaturizationTransformerPrimitiveBase"],
            "hyperparams": {},
            "arguments": {
                "inputs": {
                    "type": "container.numpy.ndarray",
                    "kind": "PIPELINE"
                }
            },
            "class_methods": {},
            "instance_methods": {
            },
            "class_attributes": {},
            "instance_attributes": {} 
        },
        "primitive_family": "DATA_CLEANING",
        "source": {
            "name": "Distil",
            "contact": "http://newknowledge.io/contact/"
        },
        "structural_type": "container.pandas.DataFrame"
    })

    def produce(self, *, inputs: Inputs) -> Outputs:
        return inputs.applymap(str)