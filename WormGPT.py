#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uncensored AI Model - Complete Implementation
A self-contained transformer-based language model without external API dependencies
This implementation includes all necessary components for training and inference
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
import threading
import queue

# Configuration constants
DEFAULT_VOCAB_SIZE = 50000
DEFAULT_MODEL_DIM = 512
DEFAULT_FEEDFORWARD_DIM = 2048
DEFAULT_NUM_HEADS = 8
DEFAULT_NUM_LAYERS = 6
DEFAULT_MAX_SEQ_LEN = 512
DEFAULT_DROPOUT = 0.1

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

class Tensor:
    """
    Custom tensor implementation for mathematical operations with automatic differentiation.
    This class provides the basic building blocks for our neural network implementation.
    """
    
    def __init__(self, data, requires_grad=False):
        """
        Initialize a tensor with data and optional gradient tracking.
        
        Args:
            data: Input data as numpy array or list
            requires_grad: Whether to track gradients for this tensor
        """
        # Convert input data to numpy array if needed
        if isinstance(data, list):
            self.data = np.array(data, dtype=np.float32)
        elif isinstance(data, np.ndarray):
            self.data = data.astype(np.float32)
        else:
            self.data = np.array([[data]], dtype=np.float32)
        
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self._backward = lambda: None
        self._ctx = None
    
    def __repr__(self):
        """String representation of the tensor"""
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad})"
    
    def zero_grad(self):
        """Zero out the gradient if it exists"""
        if self.grad is not None:
            self.grad.fill(0)
    
    def backward(self):
        """
        Compute gradients for all tensors in the computation graph.
        This implements backpropagation using topological sorting.
        """
        if not self.requires_grad:
            return
            
        # Build topological order of all tensors in the computation graph
        topo = []
        visited = set()
        
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                if hasattr(v, '_ctx') and v._ctx and hasattr(v._ctx, 'children'):
                    for child in v._ctx.children:
                        build_topo(child)
                topo.append(v)
        
        build_topo(self)
        
        # Initialize gradient of output tensor
        self.grad = np.ones_like(self.data)
        
        # Backpropagate through the graph in reverse topological order
        for v in reversed(topo):
            if hasattr(v, '_backward') and callable(v._backward):
                v._backward()
    
    @property
    def shape(self):
        """Get the shape of the tensor"""
        return self.data.shape
    
    def numpy(self):
        """Convert tensor to numpy array"""
        return self.data
    
    def item(self):
        """Get scalar value from tensor"""
        return self.data.item()
    
    def __add__(self, other):
        """Addition operation with gradient tracking"""
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += out.grad
            if other.requires_grad:
                if other.grad is None:
                    other.grad = np.zeros_like(other.data)
                other.grad += out.grad
        
        out._backward = _backward
        return out
    
    def __mul__(self, other):
        """Multiplication operation with gradient tracking"""
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += other.data * out.grad
            if other.requires_grad:
                if other.grad is None:
                    other.grad = np.zeros_like(other.data)
                other.grad += self.data * out.grad
        
        out._backward = _backward
        return out
    
    def __matmul__(self, other):
        """Matrix multiplication with gradient tracking"""
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data @ other.data, requires_grad=self.requires_grad or other.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += out.grad @ other.data.T
            if other.requires_grad:
                if other.grad is None:
                    other.grad = np.zeros_like(other.data)
                other.grad += self.data.T @ out.grad
        
        out._backward = _backward
        return out
    
    def __pow__(self, exp):
        """Power operation with gradient tracking"""
        out = Tensor(self.data ** exp, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += (exp * (self.data ** (exp - 1))) * out.grad
        
        out._backward = _backward
        return out
    
    def __neg__(self):
        """Negation operation"""
        return self * -1
    
    def __radd__(self, other):
        """Right addition operation"""
        return self + other
    
    def __rmul__(self, other):
        """Right multiplication operation"""
        return self * other
    
    def __sub__(self, other):
        """Subtraction operation"""
        return self + (-other)
    
    def __rsub__(self, other):
        """Right subtraction operation"""
        return (-self) + other
    
    def __truediv__(self, other):
        """Division operation"""
        return self * (other ** -1)
    
    def __rtruediv__(self, other):
        """Right division operation"""
        return other * (self ** -1)
    
    def sum(self, axis=None):
        """Sum operation with gradient tracking"""
        out = Tensor(np.sum(self.data, axis=axis), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                if axis is None:
                    self.grad += np.ones_like(self.data) * out.grad
                else:
                    expand_shape = list(self.data.shape)
                    expand_shape[axis] = 1
                    self.grad += np.ones_like(self.data) * np.reshape(out.grad, expand_shape)
        
        out._backward = _backward
        return out
    
    def mean(self, axis=None):
        """Mean operation with gradient tracking"""
        out = Tensor(np.mean(self.data, axis=axis), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                if axis is None:
                    self.grad += (np.ones_like(self.data) / self.data.size) * out.grad
                else:
                    expand_shape = list(self.data.shape)
                    expand_shape[axis] = 1
                    self.grad += (np.ones_like(self.data) / self.data.shape[axis]) * np.reshape(out.grad, expand_shape)
        
        out._backward = _backward
        return out
    
    def transpose(self):
        """Transpose operation with gradient tracking"""
        out = Tensor(self.data.T, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += out.grad.T
        
        out._backward = _backward
        return out
    
    def reshape(self, *shape):
        """Reshape operation with gradient tracking"""
        out = Tensor(self.data.reshape(*shape), requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                self.grad += out.grad.reshape(self.data.shape)
        
        out._backward = _backward
        return out
    
    def softmax(self, axis=-1):
        """
        Softmax activation function with gradient tracking.
        
        Args:
            axis: Axis along which to compute softmax
            
        Returns:
            Tensor with softmax applied
        """
        # Numerical stability: subtract max before exponentiation
        max_vals = np.max(self.data, axis=axis, keepdims=True)
        exp_data = np.exp(self.data - max_vals)
        out_data = exp_data / np.sum(exp_data, axis=axis, keepdims=True)
        out = Tensor(out_data, requires_grad=self.requires_grad)
        
        def _backward():
            if self.requires_grad:
                if self.grad is None:
                    self.grad = np.zeros_like(self.data)
                # Simplified softmax gradient
                s = out_data