
from ._obj_from_dict import ObjFromDict

from .request_rotb_curves import RequestRotbCurves
from .response_rotb_curves import ResponseRotbCurves

from .request_rotb_compute_strategy_components import RequestRotbComputeStrategyComponents
from .response_rotb_compute_strategy_components import ResponseRotbComputeStrategyComponents
from .slice_rotb_compute_strategy_components import SliceRotbComputeStrategyComponents


DIC_ENDPOINT = {
    'v1_curves': {
        
        'request': RequestRotbCurves,
        'response': ResponseRotbCurves,
    },
    'v1_compute_strategy_components': {
        'request': RequestRotbComputeStrategyComponents,
        'response': ResponseRotbComputeStrategyComponents,
        'slice': SliceRotbComputeStrategyComponents,
        
    },
    # to add new endpoint here after creating the corresponding
    # Request Response and optionally Slice objects
}

ENDPOINTS = ObjFromDict(DIC_ENDPOINT)
