# -*- coding: utf-8 -*-

"""

CX JSON
~~~~~~~
CX is an aspect-oriented network interchange format encoded in JSON with a format inspired by the JSON-LD encoding of
Resource Description Framework (RDF). It is primarily used by the Network Data Exchange (NDEx) and more recent versions
of Cytoscape.

.. seealso::

    - The NDEx Data Model `Specification <http://www.home.ndexbio.org/data-model/>`_
    - `Cytoscape.js <http://js.cytoscape.org/>`_
    - CX Support for Cytoscape.js on the Cytoscape `App Store <http://apps.cytoscape.org/apps/cxsupport>`_

"""

import json
import logging
import time
from collections import defaultdict

from ..canonicalize import node_to_bel
from ..constants import *
from ..struct import BELGraph
from ..utils import expand_dict, flatten_dict, hash_node

CX_NODE_NAME = 'label'

__all__ = [
    'to_cx',
    'to_cx_jsons',
    'to_cx_file',
    'from_cx',
    'from_cx_jsons',
    'from_cx_file',
    'NDEX_SOURCE_FORMAT',
]

log = logging.getLogger(__name__)

NDEX_SOURCE_FORMAT = "ndex:sourceFormat"


def _dict_to_cx(d, key_tag='k', value_tag='v'):
    return [{key_tag: k, value_tag: v} for k, v in d.items()]


def _cx_to_dict(list_of_dicts, key_tag='k', value_tag='v'):
    return {d[key_tag]: d[value_tag] for d in list_of_dicts}


def calculate_canonical_cx_identifier(graph, node):
    """Calculates the canonical name for a given node. If it is a simple node, uses the namespace:name combination.
    Otherwise, it uses the BEL string.

    :param BELGraph graph: A BEL Graph
    :param tuple node: A node
    :return: Appropriate identifier for the node for CX indexing
    :rtype: str
    """
    data = graph.node[node]

    if data[FUNCTION] == COMPLEX and NAMESPACE in data:
        return '{}:{}'.format(data[NAMESPACE], data[NAME])

    if VARIANTS in data or FUSION in data or data[FUNCTION] in {REACTION, COMPOSITE, COMPLEX}:
        return node_to_bel(data)

    if VARIANTS not in data and FUSION not in data:  # this is should be a simple node
        return '{}:{}'.format(data[NAMESPACE], data[NAME])

    raise ValueError('Unexpected node data: {}'.format(data))


def build_node_mapping(graph):
    """Builds a mapping from a graph's nodes to their canonical sort order
    
    :param BELGraph graph: A BEL graph 
    :return: A mapping from a graph's nodes to their canonical sort order
    :rtype: dict[tuple,int]
    """
    return {
        node: node_index
        for node_index, node in enumerate(sorted(graph, key=hash_node))
    }


def to_cx(graph):
    """Converts BEL Graph to CX data format (as in-memory JSON) for use with `NDEx <http://www.ndexbio.org/>`_

    :param BELGraph graph: A BEL Graph
    :return: The CX JSON for this graph
    :rtype: list

    .. seealso::

        - `NDEx Python Client <https://github.com/ndexbio/ndex-python>`_
        - `PyBEL / NDEx Python Client Wrapper <https://github.com/pybel/pybel2ndex>`_

    """
    node_mapping = build_node_mapping(graph)
    node_index_data = {}
    nodes_entry = []
    node_attributes_entry = []

    for node, node_index in node_mapping.items():
        data = graph.node[node]
        node_index_data[node_index] = data

        nodes_entry.append({
            '@id': node_index,
            'n': calculate_canonical_cx_identifier(graph, node)
        })

        for k, v in data.items():
            if k == VARIANTS:
                for i, el in enumerate(v):
                    for a, b in flatten_dict(el).items():
                        node_attributes_entry.append({
                            'po': node_index,
                            'n': '{}_{}_{}'.format(k, i, a),
                            'v': b
                        })
            elif k == FUSION:
                for a, b in flatten_dict(v).items():
                    node_attributes_entry.append({
                        'po': node_index,
                        'n': '{}_{}'.format(k, a),
                        'v': b
                    })

            elif k == NAME:
                node_attributes_entry.append({
                    'po': node_index,
                    'n': CX_NODE_NAME,
                    'v': v
                })

            elif k in {PRODUCTS, REACTANTS, MEMBERS}:
                node_attributes_entry.append({
                    'po': node_index,
                    'n': k,
                    'v': json.dumps(v)
                })

            else:
                node_attributes_entry.append({
                    'po': node_index,
                    'n': k,
                    'v': v
                })

    edges_entry = []
    edge_attributes_entry = []

    for edge_index, (source, target, d) in enumerate(graph.edges_iter(data=True)):
        uid = node_mapping[source]
        vid = node_mapping[target]

        edges_entry.append({
            '@id': edge_index,
            's': uid,
            't': vid,
            'i': d[RELATION],
        })

        if EVIDENCE in d:
            edge_attributes_entry.append({
                'po': edge_index,
                'n': EVIDENCE,
                'v': d[EVIDENCE]
            })

            for k, v in d[CITATION].items():
                edge_attributes_entry.append({
                    'po': edge_index,
                    'n': '{}_{}'.format(CITATION, k),
                    'v': v
                })

        if ANNOTATIONS in d:
            for annotation, value in d[ANNOTATIONS].items():
                edge_attributes_entry.append({
                    'po': edge_index,
                    'n': annotation,
                    'v': value
                })

        if SUBJECT in d:
            for k, v in flatten_dict(d[SUBJECT]).items():
                edge_attributes_entry.append({
                    'po': edge_index,
                    'n': '{}_{}'.format(SUBJECT, k),
                    'v': v
                })

        if OBJECT in d:
            for k, v in flatten_dict(d[OBJECT]).items():
                edge_attributes_entry.append({
                    'po': edge_index,
                    'n': '{}_{}'.format(OBJECT, k),
                    'v': v
                })

    context_legend = {}

    for key in graph.namespace_url:
        context_legend[key] = GRAPH_NAMESPACE_URL

    for key in graph.namespace_owl:
        context_legend[key] = GRAPH_NAMESPACE_OWL

    for key in graph.namespace_pattern:
        context_legend[key] = GRAPH_NAMESPACE_PATTERN

    for key in graph.annotation_url:
        context_legend[key] = GRAPH_ANNOTATION_URL

    for key in graph.annotation_owl:
        context_legend[key] = GRAPH_ANNOTATION_OWL

    for key in graph.annotation_pattern:
        context_legend[key] = GRAPH_ANNOTATION_PATTERN

    for key in graph.annotation_list:
        context_legend[key] = GRAPH_ANNOTATION_LIST

    context_legend_entry = []
    for keyword, resource_type in context_legend.items():
        context_legend_entry.append({
            'k': keyword,
            'v': resource_type
        })

    annotation_list_keys_lookup = {keyword: i for i, keyword in enumerate(sorted(graph.annotation_list))}
    annotation_lists_entry = []
    for keyword, values in graph.annotation_list.items():
        for value in values:
            annotation_lists_entry.append({
                'k': annotation_list_keys_lookup[keyword],
                'v': value
            })

    context_entry_dict = {}
    context_entry_dict.update(graph.namespace_url)
    context_entry_dict.update(graph.namespace_pattern)
    context_entry_dict.update(graph.namespace_owl)
    context_entry_dict.update(graph.annotation_url)
    context_entry_dict.update(graph.annotation_pattern)
    context_entry_dict.update(graph.annotation_owl)
    context_entry_dict.update(annotation_list_keys_lookup)

    context_entry_dict.update(graph.namespace_url)
    context_entry = [context_entry_dict]

    network_attributes_entry = [{
        "n": NDEX_SOURCE_FORMAT,
        "v": "PyBEL"
    }]
    for k, v in graph.document.items():
        network_attributes_entry.append({
            'n': k,
            'v': v
        })

    # Coalesce to cx
    # cx = create_aspect.number_verification()
    cx = [{'numberVerification': [{'longNumber': 281474976710655}]}]

    cx_pairs = [
        ('@context', context_entry),
        ('context_legend', context_legend_entry),
        ('annotation_lists', annotation_lists_entry),
        ('networkAttributes', network_attributes_entry),
        ('nodes', nodes_entry),
        ('nodeAttributes', node_attributes_entry),
        ('edges', edges_entry),
        ('edgeAttributes', edge_attributes_entry),
    ]

    cx_metadata = []

    for key, aspect in cx_pairs:
        aspect_dict = {
            "name": key,
            "elementCount": len(aspect),
            "lastUpdate": time.time(),
            "consistencyGroup": 1,
            "properties": [],
            "version": "1.0"
        }

        if key in {'citations', 'supports', 'nodes', 'edges'}:
            aspect_dict['idCounter'] = len(aspect)

        cx_metadata.append(aspect_dict)

    cx.append({
        'metaData': cx_metadata
    })

    for key, aspect in cx_pairs:
        cx.append({
            key: aspect
        })

    cx.append({"status": [{"error": "", "success": True}]})

    return cx


def to_cx_file(graph, file, indent=2, **kwargs):
    """Writes this graph to a JSON file in CX format

    :param BELGraph graph: A BEL graph
    :param file file: A writable file or file-like
    :param Optional[int] indent: How many spaces to use to pretty print. Change to None for no pretty printing

    Example:

    >>> from pybel import from_url, to_cx_file
    >>> from pybel.constants import SMALL_CORPUS_URL
    >>> graph = from_url(SMALL_CORPUS_URL)
    >>> with open('graph.cx', 'w') as f:
    >>> ... to_cx_file(graph, f)
    """
    graph_cx_json_dict = to_cx(graph)
    json.dump(graph_cx_json_dict, file, ensure_ascii=False, indent=indent, **kwargs)


def to_cx_jsons(graph, **kwargs):
    """Dumps a BEL graph as CX JSON to a string
    
    :param BELGraph graph: A BEL Graph
    :return: CX JSON string
    :rtype: str
    """
    graph_cx_json_str = to_cx(graph)
    return json.dumps(graph_cx_json_str, **kwargs)


def from_cx(cx):
    """Rebuilds a BELGraph from CX JSON output from PyBEL

    :param list cx: The CX JSON for this graph
    :rtype: BELGraph
    """
    graph = BELGraph()

    context_legend_entry = []
    annotation_lists_entry = []
    context_entry = {}
    network_attributes_entry = []
    node_entries = []
    node_attributes_entries = []
    edge_annotations_entries = []
    edges_entries = []
    meta_entries = defaultdict(list)

    for element in cx:
        for k, v in element.items():
            if k == 'context_legend':
                context_legend_entry.extend(v)
            elif k == 'annotation_lists':
                annotation_lists_entry.extend(v)
            elif k == '@context':
                context_entry.update(v[0])
            elif k == 'networkAttributes':
                network_attributes_entry.extend(v)
            elif k == 'nodes':
                node_entries.extend(v)
            elif k == 'nodeAttributes':
                node_attributes_entries.extend(v)
            elif k == 'edges':
                edges_entries.extend(v)
            elif k == 'edgeAttributes':
                edge_annotations_entries.extend(v)
            else:
                meta_entries[k].extend(v)

    context_legend = _cx_to_dict(context_legend_entry)

    annotation_lists = defaultdict(set)
    for d in annotation_lists_entry:
        annotation_lists[d['k']].add(d['v'])

    for keyword, entry in context_entry.items():
        if context_legend[keyword] == GRAPH_NAMESPACE_URL:
            graph.namespace_url[keyword] = entry
        elif context_legend[keyword] == GRAPH_NAMESPACE_OWL:
            graph.namespace_owl[keyword] = entry
        elif context_legend[keyword] == GRAPH_NAMESPACE_PATTERN:
            graph.namespace_pattern[keyword] = entry
        elif context_legend[keyword] == GRAPH_ANNOTATION_URL:
            graph.annotation_url[keyword] = entry
        elif context_legend[keyword] == GRAPH_ANNOTATION_OWL:
            graph.annotation_owl[keyword] = entry
        elif context_legend[keyword] == GRAPH_ANNOTATION_PATTERN:
            graph.annotation_pattern[keyword] = entry
        elif context_legend[keyword] == GRAPH_ANNOTATION_LIST:
            graph.annotation_list[keyword] = annotation_lists[entry]

    for d in network_attributes_entry:
        if d['n'] == NDEX_SOURCE_FORMAT:
            continue
        graph.graph[GRAPH_METADATA][d['n']] = d['v']

    node_name = {}
    for d in node_entries:
        node_name[d['@id']] = d['n']

    node_data = defaultdict(dict)
    for d in node_attributes_entries:
        node_data[d['po']][d['n']] = d['v']

    node_data_pp = defaultdict(dict)
    node_data_fusion = defaultdict(dict)
    node_data_variants = defaultdict(lambda: defaultdict(dict))

    for nid, d in node_data.items():
        for k, v in d.items():
            if k.startswith(FUSION):
                node_data_fusion[nid][k] = v
            elif k.startswith(VARIANTS):
                _, i, vls = k.split('_', 2)
                node_data_variants[nid][i][vls] = v
            elif k in {PRODUCTS, REACTANTS, MEMBERS}:
                node_data_pp[nid][k] = json.loads(v)
            else:
                node_data_pp[nid][k] = v

    for nid, d in node_data_fusion.items():
        node_data_pp[nid][FUSION] = expand_dict(d)

    for nid, d in node_data_variants.items():
        node_data_pp[nid][VARIANTS] = [expand_dict(d[i]) for i in sorted(d)]

    for nid, d in node_data_pp.items():
        if CX_NODE_NAME in d:
            d[NAME] = d.pop(CX_NODE_NAME)
        graph.add_node(nid, attr_dict=d)

    edge_relation = {}
    edge_source = {}
    edge_target = {}
    for d in edges_entries:
        eid = d['@id']
        edge_relation[eid] = d['i']
        edge_source[eid] = d['s']
        edge_target[eid] = d['t']

    edge_data = defaultdict(dict)
    for d in edge_annotations_entries:
        edge_data[d['po']][d['n']] = d['v']

    edge_citation = defaultdict(dict)
    edge_subject = defaultdict(dict)
    edge_object = defaultdict(dict)
    edge_annotations = defaultdict(dict)

    edge_data_pp = defaultdict(dict)

    for eid, d in edge_data.items():
        for k, v in d.items():
            if k.startswith(CITATION):
                _, vl = k.split('_', 1)
                edge_citation[eid][vl] = v
            elif k.startswith(SUBJECT):
                _, vl = k.split('_', 1)
                edge_subject[eid][vl] = v
            elif k.startswith(OBJECT):
                _, vl = k.split('_', 1)
                edge_object[eid][vl] = v
            elif k == EVIDENCE:
                edge_data_pp[eid][EVIDENCE] = v
            else:
                edge_annotations[eid][k] = v

    for eid, d in edge_citation.items():
        edge_data_pp[eid][CITATION] = d

    for eid, d in edge_subject.items():
        edge_data_pp[eid][SUBJECT] = expand_dict(d)

    for eid, d in edge_object.items():
        edge_data_pp[eid][OBJECT] = expand_dict(d)

    for eid in edge_relation:
        edge_data_pp[eid][ANNOTATIONS] = edge_annotations[eid] if eid in edge_annotations else {}

        if eid in edge_citation:
            graph.add_edge(
                edge_source[eid],
                edge_target[eid],
                attr_dict=edge_data_pp[eid],
                **{RELATION: edge_relation[eid]}
            )
        elif edge_relation[eid] in unqualified_edges:
            graph.add_edge(
                edge_source[eid],
                edge_target[eid],
                key=unqualified_edge_code[edge_relation[eid]],
                **{RELATION: edge_relation[eid], ANNOTATIONS: {}}
            )
        else:
            raise ValueError('problem adding edge: {}'.format(eid))

    return graph


def from_cx_jsons(graph_cx_json_str):
    """Reconstitutes a BEL graph from a CX JSON string
    
    :param str graph_cx_json_str: CX JSON string 
    :return: A BEL graph representing the CX graph contained in the string
    :rtype: BELGraph
    """
    graph_cx_json_dict = json.loads(graph_cx_json_str)
    return from_cx(graph_cx_json_dict)


def from_cx_file(file):
    """Reads a file containing CX JSON and converts to a BEL graph

    :param file file: A readable file or file-like containing the CX JSON for this graph
    :return: A BEL Graph representing the CX graph contained in the file
    :rtype: BELGraph
    """
    graph_cx_json_dict = json.load(file)
    return from_cx(graph_cx_json_dict)
