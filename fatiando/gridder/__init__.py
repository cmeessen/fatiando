"""
Create and operate on grids and profiles.
"""
from .slicing import inside, cut
from .interpolation import interp, interp_at, profile
from .padding import pad_array, unpad_array, pad_coords
from .point_generation import regular, scatter, circular_scatter
from .utils import spacing