#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WormGPT - Complete Implementation
A self-contained transformer-based language model without external API dependencies
"""

import os
import sys
import math
import random
import re
import json
import time
import argparse
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional, Union, Callable
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import base64

# Deep learning components from scratch
class Tensor:
    """Custom tensor implementation for mathematical operations"""
    
    def __init__(self, data: List[List[float]], requires_grad: bool = False):
        self.data = np.array(data, dtype=np.float32)
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self._backward = lambda: None
        self._ctx = None
    
    def __repr__(self):
        return f"Tensor({self.data.shape}, requires_grad={self.requires_grad})"
    
    def zero_grad(self):
        if self.grad is not None:
            self.grad.fill(0)
    
    def backward(self):
        if self.requires_grad:
            topo = []
            visited = set()
            
            def build_topo(v):
                if v not in visited:
                    visited.add(v)
                    if hasattr(v, '_ctx') and v._ctx:
                        for child in v._ctx.children:
                            build_topo(child)
                    topo.append(v)
            
            build_topo(self)
            self.grad = np.ones_like(self.data)
            for v in reversed(topo):
                v._backward()
    
    @property
    def shape(self):
        return self.data.shape
    
    def numpy(self):
        return self.data
    
    def item(self):
        return self.data.item()
    
    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad
            if other.requires_grad:
                other.grad = other.grad + out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + other.data * out.grad
            if other.requires_grad:
                other.grad = other.grad + self.data * out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def __matmul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data @ other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad @ other.data.T
            if other.requires_grad:
                other.grad = other.grad + self.data.T @ out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def __pow__(self, exp):
        out = Tensor(self.data ** exp, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + (exp * (self.data ** (exp - 1))) * out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def __neg__(self):
        return self * -1
    
    def __radd__(self, other):
        return self + other
    
    def __rmul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return (-self) + other
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    def __rtruediv__(self, other):
        return other * (self ** -1)
    
    def sum(self, axis=None):
        out = Tensor(np.sum(self.data, axis=axis), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if axis is None:
                    self.grad = self.grad + np.ones_like(self.data) * out.grad
                else:
                    expand_shape = list(self.data.shape)
                    expand_shape[axis] = 1
                    self.grad = self.grad + np.ones_like(self.data) * np.reshape(out.grad, expand_shape)
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def mean(self, axis=None):
        out = Tensor(np.mean(self.data, axis=axis), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if axis is None:
                    self.grad = self.grad + (np.ones_like(self.data) / self.data.size) * out.grad
                else:
                    expand_shape = list(self.data.shape)
                    expand_shape[axis] = 1
                    self.grad = self.grad + (np.ones_like(self.data) / self.data.shape[axis]) * np.reshape(out.grad, expand_shape)
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def transpose(self):
        out = Tensor(self.data.T, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad.T
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def reshape(self, *shape):
        out = Tensor(self.data.reshape(*shape), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + out.grad.reshape(self.data.shape)
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def softmax(self, axis=-1):
        exp_data = np.exp(self.data - np.max(self.data, axis=axis, keepdims=True))
        out_data = exp_data / np.sum(exp_data, axis=axis, keepdims=True)
        out = Tensor(out_data, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                s = out_data
                grad = out.grad
                if axis == -1 or axis == len(self.data.shape) - 1:
                    jacobian = np.diagflat(s) - np.outer(s, s)
                    self.grad = self.grad + jacobian @ grad
                else:
                    # For other axes, we'd need a more complex implementation
                    # Simplified version for this example
                    self.grad = self.grad + grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def relu(self):
        out_data = np.maximum(0, self.data)
        out = Tensor(out_data, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                self.grad = self.grad + (self.data > 0) * out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def gelu(self):
        # GELU approximation: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
        x = self.data
        out_data = 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))
        out = Tensor(out_data, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                # Simplified gradient for GELU
                grad = 0.5 * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3))) + \
                       0.5 * x * (1 - np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3))**2) * \
                       np.sqrt(2 / np.pi) * (1 + 0.134145 * x**2)
                self.grad = self.grad + grad * out.grad
        
        out._backward = _backward
        out._ctx = self
        return out
    
    def layer_norm(self, eps=1e-5):
        x = self.data
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        out_data = (x - mean) / np.sqrt(var + eps)
        out = Tensor(out_data, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                # Simplified gradient for layer norm
                N = x.shape[-1]
                grad = out.grad
                x_grad = (1.0 / N) * (1.0 / np.sqrt(var + eps)) * (N * grad - np.sum(grad, axis=-1, keepdims=True) - 
                            (x - mean) * (1.0 / (var + eps)) * np.sum