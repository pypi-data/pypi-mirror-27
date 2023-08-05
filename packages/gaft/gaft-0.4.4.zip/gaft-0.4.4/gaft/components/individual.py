#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log2
from itertools import accumulate
from random import uniform
import logging

from ..mpiutil import mpi


class GAIndividual(object):
    def __init__(self, ranges, encoding='binary', eps=0.001, verbosity=1):
        '''
        Class for individual in population. Random variants will be initialized
        by default.

        NOTE: The decrete precisions for different components in varants may be
              adjusted automatically (possible precision loss) if eps and ranges
              are not appropriate.
              
              Please check it before you put it into GA engine. If you don't want
              to see the warning info, set verbosity to 0 :)

        :param ranges: value ranges for all entries in variants.
        :type ranges: list of range tuples. e.g. [(0, 1), (-1, 1)]

        :param encoding: gene encoding, 'decimal' or 'binary', default is binary.
        :type encoding: str

        :param eps: decrete precisions for binary encoding, default is 0.001.
        :type eps: float or float list with the same length with ranges.

        :param verbosity: The verbosity level of info output.
        :param verbosity: int, 0 or 1(default)
        '''

        self.ranges = ranges
        self.eps = eps
        self.encoding = encoding
        self.verbosity = verbosity

        # Check parameters.
        self._check_parameters()

        # Lengths for all binary sequence in chromsome and adjusted decrete precisions.
        self.lengths, self.precisions = [], []

        for (a, b), eps in zip(self.ranges, self.eps):
            length = int(log2((b - a)/eps))
            precision = (b - a)/(2**length)

            if precision != eps and mpi.is_master and self.verbosity:
                print('Precision loss {} -> {}'.format(eps, precision))

            self.lengths.append(length)
            self.precisions.append(precision)

        # The start and end indices for each gene segment for entries in variants.
        self.gene_indices = self._get_gene_indices()

        # Generate randomly.
        self.variants = self._init_variants()

        # Gene encoding.
        self.chromsome = self.encode()

    def init(self, chromsome=None, variants=None):
        '''
        Initialize the individual by providing chromsome or variants.
        If both chromsome and variants are provided, only the chromsome would
        be used.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of float/int.

        :param variants: the variable vector of the target function.
        :type variants: list of float.
        '''
        if not any([chromsome, variants]):
            msg = 'Chromsome or variants must be supplied for individual initialization'
            raise ValueError(msg)

        if chromsome:
            self.chromsome = chromsome
            self.variants = self.decode()
        else:
            self.variants = variants
            self.chromsome = self.encode()

        return self

    def clone(self):
        '''
        Clone a new individual from current one.
        '''
        indv = self.__class__(self.ranges,
                              encoding=self.encoding,
                              eps=self.eps,
                              verbosity=self.verbosity)
        indv.init(chromsome=self.chromsome)
        return indv

    def _check_parameters(self):
        '''
        Private helper function to check individual parameters.
        '''
        # Check decrete precision.
        if type(self.eps) is float:
            self.eps = [self.eps]*len(self.ranges)
        else:
            # Check eps length.
            if len(self.eps) != len(self.ranges):
                raise ValueError('Lengths of eps and ranges should be the same')
            for eps, (a, b) in zip(self.eps, self.ranges):
                if eps > (b - a):
                    msg = 'Invalid eps {} in range ({}, {})'.format(eps, a, b)
                    raise ValueError(msg)

    def _init_variants(self):
        '''
        Initialize individual variants randomly.
        '''
        variants = []
        for eps, (a, b) in zip(self.precisions, self.ranges):
            n_intervals = (b - a)//eps
            n = int(uniform(0, n_intervals + 1))
            variants.append(a + n*eps)
        return variants

    def encode(self):
        '''
        Encode variant to gene sequence in individual using different encoding.
        '''
        if self.encoding == 'decimal':
            return self.variants

        chromsome = []
        for var, (a, _), length, eps in zip(self.variants, self.ranges,
                                            self.lengths, self.precisions):
            chromsome.extend(self.binarize(var-a, eps, length))

        return chromsome

    def decode(self):
        ''' 
        Decode gene sequence to variants of target function.
        '''
        if self.encoding == 'decimal':
            return self.variants

        variants =  [self.decimalize(self.chromsome[start: end], eps, lower_bound)
                     for (start, end), (lower_bound, _), eps in
                     zip(self.gene_indices, self.ranges, self.precisions)]
        return variants

    def _get_gene_indices(self):
        '''
        Helper function to get gene slice indices.
        '''
        end_indices = list(accumulate(self.lengths))
        start_indices = [0] + end_indices[: -1]
        return list(zip(start_indices, end_indices))

    @staticmethod
    def binarize(decimal, eps, length):
        '''
        Helper function to convert a float to binary sequence.

        :param decimal: the decimal number to be converted.
        :param eps: the decrete precision of binary sequence.
        :param length: the length of binary sequence.
        '''
        n = int(decimal/eps)
        bin_str = '{:0>{}b}'.format(n, length)
        return [int(i) for i in bin_str]

    @staticmethod
    def decimalize(binary, eps, lower_bound):
        '''
        Helper function to convert a binary sequence back to decimal number.
        '''
        bin_str = ''.join([str(bit) for bit in binary])
        return lower_bound + int(bin_str, 2)*eps

