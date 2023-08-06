# -*- coding: utf-8 -*-

"""

This module assists in running complex workflows on BEL graphs.

Example Pipeline #1
~~~~~~~~~~~~~~~~~~~
This example shows a pipeline that acquires a subgraph and finds possible additions to the subgraph.

>>> network = ...
>>> example = Pipeline()
>>> example.append('get_subgraph_by_annotation_value', 'Subgraph', 'Blood vessel dilation subgraph')
>>> example.append('enrich_unqualified')
>>> example.append('infer_central_dogma')
>>> example.append('expand_periphery')
>>> result = example.run(network)

Example Pipeline #2
~~~~~~~~~~~~~~~~~~~
This example shows how additional data can be integrated into a graph.

>>> from pybel.constants import PROTEIN
>>> network = ...
>>> example = Pipeline()
>>> example.append('infer_central_dogma')
>>> example.append('enrich_unqualified')
>>> example.append('infer_central_dogma')
>>> example.append('expand_periphery')
>>> example.append('expand_nodes_neighborhoods', [(PROTEIN, 'HGNC', 'AKT1'), (PROTEIN, 'HGNC', 'AKT2')])
>>> result = example.run(network)

Example Pipeline #3
~~~~~~~~~~~~~~~~~~~
This example shows how the results from multiple pipelines can be combine.

>>> network = ...
>>> pipeline_a = Pipeline()
>>> pipeline_a.append('get_subgraph_by_annotation_value', 'Subgraph', 'Blood vessel dilation subgraph')
>>> pipeline_b = Pipeline()
>>> pipeline_b.append('get_subgraph_by_annotation_value', 'Subgraph', 'Tau protein subgraph')
>>> pipeline_c = Pipeline.union(pipeline_a, pipeline_b)
>>> result = pipeline_c.run(network)

"""

from __future__ import print_function

import json
import logging
from functools import wraps
from inspect import signature

from pybel.struct.operations import node_intersection, union

__all__ = [
    'Pipeline',
    'in_place_mutator',
    'uni_in_place_mutator',
    'uni_mutator',
    'mutator',
    'splitter'
]

log = logging.getLogger(__name__)

mapped = {}
universe_map = {}
no_universe_map = {}
in_place_map = {}
out_place_map = {}
has_arguments_map = {}
no_arguments_map = {}

#: A map of function names to functions that split graphs into dictionaries of graphs
splitter_map = {}


def _register(universe, in_place, **kwargs):
    """Builds a decorator function to tag mutator functions

    :param bool universe: Does the first positional argument of this function correspond to a universe graph?
    :param bool in_place: Does this function return a new graph, or just modify it in-place?
    :param dict kwargs: Other parameters to annotate to the function
    """

    def decorator(f):
        """A decorator that tags mutator functions

        :param f: A function
        :return: The same function, with additional properties added
        """
        f.__dict__.update(kwargs)

        if universe:
            universe_map[f.__name__] = f
        else:
            no_universe_map[f.__name__] = f

        if in_place:
            in_place_map[f.__name__] = f
        else:
            out_place_map[f.__name__] = f

        z = signature(f)
        if (universe and 3 <= len(z.parameters)) or (not universe and 2 <= len(z.parameters)):
            has_arguments_map[f.__name__] = f
        else:
            no_arguments_map[f.__name__] = f

        mapped[f.__name__] = f

        return f

    return decorator


#: A function decorator to inform the Pipeline how to handle a function
in_place_mutator = _register(universe=False, in_place=True)
#: A function decorator to inform the Pipeline how to handle a function
uni_in_place_mutator = _register(universe=True, in_place=True)
#: A function decorator to inform the Pipeline how to handle a function
uni_mutator = _register(universe=True, in_place=False)
#: A function decorator to inform the Pipeline how to handle a function
mutator = _register(universe=False, in_place=False)

SET_UNIVERSE = 'UNIVERSE'


def splitter(f):
    """A function decorator that signifies a function that takes in a graph and returns a dictionary of keys to graphs

    :param types.FunctionType f: A function
    :rtype: types.FunctionType
    """
    splitter_map[f.__name__] = f
    return f


def function_is_registered(name):
    """Checks if a function is a valid pipeline function

    :param str or types.FunctionType name: The name of the function
    :rtype: bool
    """
    if not isinstance(name, str):
        return name.__name__ in mapped

    return name in mapped

class Pipeline:
    """Builds and runs analytical pipelines on BEL graphs"""

    def __init__(self, protocol=None, universe=None):
        """
        :param list[dict] protocol: The list of dictionaries describing how to mutate/filter a network
        :param pybel.BELGraph universe: The entire set of known knowledge to draw from
        """
        self.universe = universe
        self.protocol = [] if protocol is None else protocol

    def get_function(self, name):
        """Wraps a function with the universe and in-place

        :param str name: The name of the function
        :rtype: types.FunctionType
        """
        f = mapped[name]

        if name in universe_map and name in in_place_map:
            return self.wrap_in_place(self.wrap_universe(f))

        if name in universe_map:
            return self.wrap_universe(f)

        if name in in_place_map:
            return self.wrap_in_place(f)

        return f

    def append(self, name, *args, **kwargs):
        """Adds a function and arguments to the pipeline

        :param str name: The name of the function
        :param args: The positional arguments to call in the function
        :param kwargs: The keyword arguments to call in the function
        :return: This pipeline for fluid query building
        :rtype: Pipeline
        """
        if not isinstance(name, str):
            return self.append(name.__name__, *args, **kwargs)

        if not function_is_registered(name):
            raise KeyError(name)

        av = {
            'function': name,
        }

        if args:
            av['args'] = args

        if kwargs:
            av['kwargs'] = kwargs

        self.protocol.append(av)
        return self

    def extend(self, pipeline):
        """Adds another pipeline to the end of the current pipeline

        :param Pipeline pipeline: Another pipeline
        :return: This pipeline for fluid query building
        :rtype: Pipeline
        """
        self.protocol.extend(pipeline.protocol)
        return self

    def __nonzero__(self):
        return self.protocol

    def _run_helper(self, graph, protocol):
        """Helps run the protocol

        :param pybel.BELGraph graph: A BEL graph
        :param list[dict] protocol: The protocol to run, as JSON
        """
        result = graph

        for entry in protocol:
            if 'meta' not in entry:
                f = self.get_function(entry['function'])
                result = f(
                    result,
                    *(entry.get('args', [])),
                    **(entry.get('kwargs', {}))
                )
            else:
                networks = (
                    self._run_helper(graph, subprotocol)
                    for subprotocol in entry['pipeline']
                )

                if entry['meta'] == 'union':
                    result = union(networks)

                elif entry['meta'] == 'intersection':
                    result = node_intersection(networks)

                else:
                    raise ValueError

        return result

    def run(self, graph, universe=None, in_place=True):
        """Runs the contained protocol on a seed graph

        :param pybel.BELGraph graph: The seed BEL graph
        :param pybel.BELGraph universe: Allows just-in-time setting of the universe in case it wasn't set before.
                                        Defaults to the given network.
        :param bool in_place: Should the graph be copied before applying the algorithm?
        :return: The new graph is returned if not applied in-place
        """
        self.universe = graph if universe is None else universe

        result = graph if in_place else graph.copy()
        result = self._run_helper(result, self.protocol)
        return result

    def wrap_universe(self, f):
        """Takes a function that needs a universe graph as the first argument and returns a wrapped one"""

        @wraps(f)
        def wrapper(graph, *args, **kwargs):
            """Applies the enclosed function with the universe given as the first argument"""
            if self.universe is None:
                raise ValueError('Can not run universe function [{}] - No universe is set'.format(f.__name__))

            return f(self.universe, graph, *args, **kwargs)

        return wrapper

    @staticmethod
    def wrap_in_place(f):
        """Takes a function that doesn't return the graph and returns the graph"""

        @wraps(f)
        def wrapper(graph, *args, **kwargs):
            """Applies the enclosed function and returns the graph"""
            f(graph, *args, **kwargs)
            return graph

        return wrapper

    def to_json(self):
        """Gives this pipeline as json

        :rtype: list[dict]
        """
        return self.protocol

    def to_jsons(self):
        """Gives this pipeline as a JSON string

        :rtype: str
        """
        return json.dumps(self.to_json())

    def dump_json(self, file):
        """Dumps this protocol to a file in JSON"""
        return json.dump(self.protocol, file)

    @staticmethod
    def from_json(protocol):
        """Loads a pipeline from a JSON object

        :param list[dict] protocol:
        :return: The pipeline represented by the JSON
        :rtype: Pipeline
        """
        return Pipeline(protocol=protocol)

    @staticmethod
    def from_json_file(file):
        """Loads a protocol from JSON contained in file using :meth:`Pipeline.from_json`.

        :return: The pipeline represented by the JSON in the file
        :rtype: Pipeline
        """
        return Pipeline.from_json(json.load(file))

    def __str__(self):
        return json.dumps(self.protocol, indent=2)

    @staticmethod
    def _build_meta(meta, pipelines):
        """

        :param str meta:
        :param list[Pipeline] pipelines:
        :return:
        """
        return Pipeline.from_json([{
            'meta': meta,
            'pipelines': [
                pipeline.to_json()
                for pipeline in pipelines
            ]
        }])

    @staticmethod
    def union(*pipelines):
        """Takes the union of multiple pipelines

        :param list[Pipeline] pipelines: A list of pipelines
        :return: The union of the results from multiple pipelines
        :rtype: Pipeline
        """
        return Pipeline._build_meta('union', pipelines)

    @staticmethod
    def intersection(*pipelines):
        """Takes the intersection of the results from multiple pipelines

        :param list[Pipeline] pipelines: A list of pipelines
        :return: The intersection of results from multiple pipelines
        :rtype: Pipeline
        """
        return Pipeline._build_meta('intersection', pipelines)
