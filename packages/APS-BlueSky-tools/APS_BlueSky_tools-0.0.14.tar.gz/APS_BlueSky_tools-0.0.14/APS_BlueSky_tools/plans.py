"""
Plans that might be useful at the APS using BlueSky

.. autosummary::
   
   ~nscan
   ~sscan

"""

# Copyright (c) 2017-, UChicago Argonne, LLC.  See LICENSE file.

from collections import OrderedDict
import logging
import numpy as np 
from bluesky import preprocessors as bpp
from bluesky import plan_stubs as bps
from _ast import Not


logger = logging.getLogger(__name__).addHandler(logging.NullHandler())


def nscan(detectors, *motor_sets, num=11, per_step=None, md=None):
    """
    Scan over ``n`` variables moved together, each in equally spaced steps.

    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    motor_sets : list
        sequence of one or more groups of: motor, start, finish
    motor : object
        any 'settable' object (motor, temp controller, etc.)
    start : float
        starting position of motor
    finish : float
        ending position of motor
    num : int
        number of steps (default = 11)
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        Expected signature: ``f(detectors, step_cache, pos_cache)``
    md : dict, optional
        metadata
    """
    def take_n_at_a_time(args, n=2):
        yield from zip(*[iter(args)]*n)
        
    if len(motor_sets) < 3:
        raise ValueError("must provide at least one movable")
    if len(motor_sets) % 3 > 0:
        raise ValueError("must provide sets of movable, start, finish")

    motors = OrderedDict()
    for m, s, f in take_n_at_a_time(motor_sets, n=3):
        if not isinstance(s, (int, float)):
            msg = "start={} ({}): is not a number".format(s, type(s))
            raise ValueError(msg)
        if not isinstance(f, (int, float)):
            msg = "finish={} ({}): is not a number".format(f, type(f))
            raise ValueError(msg)
        motors[m.name] = dict(motor=m, start=s, finish=f, 
                              steps=np.linspace(start=s, stop=f, num=num))

    _md = {'detectors': [det.name for det in detectors],
           'motors': [m for m in motors.keys()],
           'num_points': num,
           'num_intervals': num - 1,
           'plan_args': {'detectors': list(map(repr, detectors)), 
                         'num': num,
                         'motors': repr(motor_sets),
                         'per_step': repr(per_step)},
           'plan_name': 'nscan',
           'plan_pattern': 'linspace',
           'hints': {},
           }
    _md.update(md or {})

    try:
        m = list(motors.keys())[0]
        dimensions = [(motors[m]["motor"].hints['fields'], 'primary')]
    except (AttributeError, KeyError):
        pass
    else:
        _md['hints'].setdefault('dimensions', dimensions)

    if per_step is None:
        per_step = bps.one_nd_step

    @bpp.stage_decorator(list(detectors) 
                         + [m["motor"] for m in motors.values()])
    @bpp.run_decorator(md=_md)
    def inner_scan():
        for step in range(num):
            step_cache, pos_cache = {}, {}
            for m in motors.values():
                next_pos = m["steps"][step]
                m = m["motor"]
                pos_cache[m] = m.read()[m.name]["value"]
                step_cache[m] = next_pos
            yield from per_step(detectors, step_cache, pos_cache)

    return (yield from inner_scan())


def sscan(*args, md=None, **kw):        # TODO: planned
    """
    gather data form the sscan record and emit documents
    
    Should this operate a complete scan using the sscan record?
    """
    raise NotImplemented("this is only planned")
