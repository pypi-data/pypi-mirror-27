import pandas as pd
from typing import List

from .clean_list import clean_numbers
from .clean_value import number_cleaner
from primitive_interfaces.featurization import FeaturizationTransformerPrimitiveBase
from d3m_metadata import container, hyperparams, metadata, params

Inputs = container.pandas.DataFrame
Outputs = container.pandas.DataFrame

class Hyperparams(hyperparams.Hyperparams):
    pass

class CleanNumbers(FeaturizationTransformerPrimitiveBase[Inputs, Outputs, Hyperparams]):
    __author__ = 'Distil'
    metadata = metadata.PrimitiveMetadata({
        "id": "6a63181a-15c0-3820-a6bb-e4b5bc94e4d3",
        "version": "2.0.0",
        "schema": "https://metadata.datadrivendiscovery.org/schemas/v0/primitive.json",
        "description": "Clean up number fields",
        "name": "Clean numbers",
        "python_path": "d3m.primitives.distil.CleanNumbers",
        "original_python_path": "punk.preppy.cleanNumbers.CleanNumbers",
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
        return inputs.apply(clean_numbers)