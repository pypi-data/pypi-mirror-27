#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import numpy as np
from cryio import cbfimage, parparser
from . import _crymon


class ReconstructionError(ValueError):
    pass


class HKL(ctypes.Structure):
    _fields_ = [
        ('h', ctypes.c_float),
        ('k', ctypes.c_float),
        ('l', ctypes.c_float),
    ]


class Slice(ctypes.Structure):
    _fields_ = [
        ('p0', HKL),
        ('p1', HKL),
        ('pc', HKL),
        ('thickness', ctypes.c_float),
        ('qmax', ctypes.c_float),
        ('dQ', ctypes.c_float),
        ('downsample', ctypes.c_int),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('z', ctypes.c_int),
        ('lorentz', ctypes.c_int),
        ('scale', ctypes.c_int),
        ('voxels', ctypes.c_int),
    ]


class _Reconstruct(_crymon._ccp4_encode):
    IntType = None

    def __init__(self, inttype: int, s: Slice):
        super().__init__(inttype, s)
        self.par = None

    def add(self, array: np.ndarray, angle: float, increment: float) -> None:
        if not self.par:
            raise ReconstructionError('The par file should be set with "set_par" before adding an array')
        try:
            super().add(np.ascontiguousarray(array, np.float32), angle, increment)
        except ValueError as err:
            raise ReconstructionError(f'{err}: expected ({self.par.inver}, {self.par.inhor}), got {array.shape}')

    def set_par(self, par: parparser.ParParser) -> None:
        super().set_par(par.parstruct)
        self.par = par


class Volume(_Reconstruct):
    IntType = 0

    def __init__(self, s: Slice):
        super().__init__(self.IntType, s)

    def save(self, filename):
        with open(filename, 'wb') as f:
            f.write(bytes(self))


class Layer(_Reconstruct):
    IntType = 1

    def __init__(self, s: Slice):
        super().__init__(self.IntType, s)

    def save(self, filepath: str):
        cbf = cbfimage.CbfImage()
        cbf.array = np.asarray(self, np.int32)
        cbf.save_cbf(filepath)
