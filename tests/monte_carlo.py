# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from bw2calc import *
from bw2data import config, Database, Method, projects, databases
from bw2data.tests import bw2test
import pytest


@pytest.fixture
@bw2test
def background():
    Database("biosphere").write({
        ("biosphere", "1"): {'type': 'emission'},
        ("biosphere", "2"): {'type': 'emission'},
    })
    Database("test").write({
        ("test", "1"): {
            'exchanges': [{
                'amount': 0.5,
                'minimum': 0.2,
                'maximum': 0.8,
                'input': ('test', "2"),
                'type': 'technosphere',
                'uncertainty type': 4
            }, {
                'amount': 1,
                'minimum': 0.5,
                'maximum': 1.5,
                'input': ('biosphere', "1"),
                'type': 'biosphere',
                'uncertainty type': 4
            }],
            'type': 'process',
        },
        ("test", "2"): {
            'exchanges': [{
                'amount': 0.1,
                'minimum': 0,
                'maximum': 0.2,
                'input': ('biosphere', "2"),
                'type': 'biosphere',
                'uncertainty type': 4
            }],
            'type': 'process',
            'unit': 'kg'
        },
    })
    method = Method(("a", "method"))
    method.register()
    method.write([
        (("biosphere", "1"), 1),
        (("biosphere", "2"), 2),
    ])


def get_args():
    return {("test", "1"): 1}, ("a", "method")


def test_plain_monte_carlo(background):
    mc = MonteCarloLCA(*get_args())
    assert mc.__next__() > 0

def test_monte_carlo_next(background):
    mc = MonteCarloLCA(*get_args())
    assert next(mc) > 0

def test_monte_carlo_as_iterator(background):
    mc = MonteCarloLCA(*get_args())
    for x in mc:
        assert x > 0
        break

def test_direct_solving(background):
    mc = DirectSolvingMonteCarloLCA(*get_args())
    assert next(mc)

def test_multi_mc(background):
    mc = MultiMonteCarlo(
        [
            {("test", "1"): 1},
            {("test", "2"): 1},
            {("test", "1"): 1, ("test", "2"): 1}
        ],
        ("a", "method"),
        iterations=10
    )
    assert mc.calculate()

def test_parallel_monte_carl(background):
    fu, method = get_args()
    mc = ParallelMonteCarlo(fu, method, iterations=200)
    assert mc.calculate()