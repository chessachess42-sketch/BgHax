#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uncensored AI Model - Complete Working Implementation
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

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

class SimpleTensor:
    """
    Simplified tensor implementation that actually works.
    This class provides the basic building blocks for our neural network.
    """
    
    def __init__(self, data, requires_grad=False):
        """Initialize a tensor with data and optional gradient tracking."""
        if isinstance(data, list):
            self.data = np.array(data, dtype=np.float32)
        elif isinstance(data, np.ndarray):
            self.data = data.astype(np.float32)
        else:
            self.data = np.array([[data]], dtype=np.float32)
        
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data) if requires_grad else None
    
    def __repr__(self):
        return f"SimpleTensor(shape={self.data.shape}, requires_grad={self.requires_grad})"
    
    def zero_grad(self):
        """Zero out the gradient if it exists."""
        if self.grad is not None:
            self.grad.fill(0)
    
    @property
    def shape(self):
        """Get the shape of the tensor."""
        return self.data.shape
    
    def numpy(self):
        """Convert tensor to numpy array."""
        return self.data
    
    def item(self):
        """Get scalar value from tensor."""
        return self.data.item()
    
    def __add__(self, other):
        """Addition operation."""
        other = other if isinstance(other, SimpleTensor) else SimpleTensor(other)
        out_data = self.data + other.data
        return SimpleTensor(out_data)
    
    def __mul__(self, other):
        """Multiplication operation."""
        other = other if isinstance(other, SimpleTensor) else SimpleTensor(other)
        out_data = self.data * other.data
        return SimpleTensor(out_data)
    
    def __matmul__(self, other):
        """Matrix multiplication."""
        other = other if isinstance(other, SimpleTensor) else SimpleTensor(other)
        out_data = self.data @ other.data
        return SimpleTensor(out_data)
    
    def __pow__(self, exp):
        """Power operation."""
        out_data = self.data ** exp
        return SimpleTensor(out_data)
    
    def __neg__(self):
        """Negation operation."""
        return SimpleTensor(-self.data)
    
    def __radd__(self, other):
        """Right addition operation."""
        return self + other
    
    def __rmul__(self, other):
        """Right multiplication operation."""
        return self * other
    
    def __sub__(self, other):
        """Subtraction operation."""
        return self + (-other)
    
    def __rsub__(self, other):
        """Right subtraction operation."""
        return (-self) + other
    
    def __truediv__(self, other):
        """Division operation."""
        other = other if isinstance(other, SimpleTensor) else SimpleTensor(other)
        out_data = self.data / other.data
        return SimpleTensor(out_data)
    
    def __rtruediv__(self, other):
        """Right division operation."""
        other = other if isinstance(other, SimpleTensor) else SimpleTensor(other)
        out_data = other.data / self.data
        return SimpleTensor(out_data)
    
    def sum(self, axis=None):
        """Sum operation."""
        out_data = np.sum(self.data, axis=axis)
        return SimpleTensor(out_data)
    
    def mean(self, axis=None):
        """Mean operation."""
        out_data = np.mean(self.data, axis=axis)
        return SimpleTensor(out_data)
    
    def transpose(self):
        """Transpose operation."""
        out_data = self.data.T
        return SimpleTensor(out_data)
    
    def reshape(self, *shape):
        """Reshape operation."""
        out_data = self.data.reshape(*shape)
        return SimpleTensor(out_data)
    
    def softmax(self, axis=-1):
        """Softmax activation function."""
        # Numerical stability: subtract max before exponentiation
        max_vals = np.max(self.data, axis=axis, keepdims=True)
        exp_data = np.exp(self.data - max_vals)
        out_data = exp_data / np.sum(exp_data, axis=axis, keepdims=True)
        return SimpleTensor(out_data)
    
    def relu(self):
        """ReLU activation function."""
        out_data = np.maximum(0, self.data)
        return SimpleTensor(out_data)
    
    def gelu(self):
        """GELU activation function approximation."""
        x = self.data
        out_data = 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))
        return SimpleTensor(out_data)
    
    def layer_norm(self, eps=1e-5):
        """Layer normalization."""
        x = self.data
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        out_data = (x - mean) / np.sqrt(var + eps)
        return SimpleTensor(out_data)
    
    def dropout(self, p=0.1, training=True):
        """Dropout regularization."""
        if not training:
            return SimpleTensor(self.data)
        mask = (np.random.random(self.data.shape) > p).astype(np.float32) / (1 - p)
        out_data = self.data * mask
        return SimpleTensor(out_data)
    
    def sigmoid(self):
        """Sigmoid activation function."""
        out_data = 1 / (1 + np.exp(-self.data))
        return SimpleTensor(out_data)
    
    def tanh(self):
        """Tanh activation function."""
        out_data = np.tanh(self.data)
        return SimpleTensor(out_data)
    
    def embedding_lookup(self, indices):
        """Lookup embeddings by indices."""
        if len(self.data.shape) != 2:
            raise ValueError("Embedding matrix must be 2D")
        out_data = self.data[indices]
        return SimpleTensor(out_data)
    
    def argmax(self, axis=-1):
        """Argmax operation."""
        return np.argmax(self.data, axis=axis)
    
    def topk(self, k, axis=-1):
        """Top-k operation."""
        if axis == -1:
            indices = np.argpartition(self.data, -k, axis=axis)[-k:]
            values = np.take_along_axis(self.data, indices, axis=axis)
            # Sort in descending order
            sorted_indices = np.argsort(-values, axis=axis)
            indices = np.take_along_axis(indices, sorted_indices, axis=axis)
            values = np.take_along_axis(values, sorted_indices, axis=axis)
            return values, indices
        else:
            raise ValueError("Only axis=-1 is supported for topk")

class Module:
    """Base class for all neural network modules."""
    
    def __init__(self):
        self.training = True
        self.parameters = []
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    def forward(self, *args, **kwargs):
        raise NotImplementedError
    
    def train(self):
        """Set the module in training mode."""
        self.training = True
        for module in self.__dict__.values():
            if isinstance(module, Module):
                module.train()
    
    def eval(self):
        """Set the module in evaluation mode."""
        self.training = False
        for module in self.__dict__.values():
            if isinstance(module, Module):
                module.eval()
    
    def save(self, path):
        """Save the module state."""
        state = {}
        for name, module in self.__dict__.items():
            if isinstance(module, Module):
                state[name] = module.save_dict()
        with open(path, 'wb') as f:
            pickle.dump(state, f)
    
    def load(self, path):
        """Load the module state."""
        with open(path, 'rb') as f:
            state = pickle.load(f)
        for name, module_state in state.items():
            if name in self.__dict__ and isinstance(self.__dict__[name], Module):
                self.__dict__[name].load_dict(module_state)
    
    def save_dict(self):
        """Return the state dictionary of the module."""
        state = {}
        for name, value in self.__dict__.items():
            if isinstance(value, SimpleTensor):
                state[name] = value.data
            elif isinstance(value, Module):
                state[name] = value.save_dict()
        return state
    
    def load_dict(self, state):
        """Load the module from a state dictionary."""
        for name, value in state.items():
            if name in self.__dict__:
                if isinstance(self.__dict__[name], SimpleTensor):
                    self.__dict__[name].data = value
                elif isinstance(self.__dict__[name], Module):
                    self.__dict__[name].load_dict(value)

class Linear(Module):
    """Linear (fully connected) layer."""
    
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        # Initialize weights with Xavier initialization