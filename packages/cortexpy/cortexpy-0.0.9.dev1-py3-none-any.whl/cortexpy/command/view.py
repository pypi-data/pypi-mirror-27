from enum import Enum

import logging

import attr
import sys

from Bio import SeqIO

from cortexpy.graph import ContigRetriever, parser as g_parser, traversal
from cortexpy.graph.parser.streaming import kmer_generator_from_stream
from cortexpy.graph.serializer import Serializer

logger = logging.getLogger('cortexpy.view')


class ViewContigChoice(Enum):
    term = 0
    json = 1


class ViewTraversalChoice(Enum):
    json = 1
    fasta = 2


class ArgparseError(ValueError):
    """Is raised if the args object is misconfigured"""
    pass


def add_subparser_to(subparsers):
    parent_parser = subparsers.add_parser('view', help='Display a subset of a Cortex graph')
    subparsers = parent_parser.add_subparsers()
    child_parsers = []

    graph_parser = subparsers.add_parser('graph', help='List graph records')
    contig_parser = subparsers.add_parser('contig', help='Display a contig from a Cortex graph')
    traversal = ViewTraversal(subparsers)

    child_parsers.append(graph_parser)
    child_parsers.append(contig_parser)
    child_parsers.append(traversal.parser)

    for parser in child_parsers:
        parser.add_argument('graph', help='Input Cortex graph')

    graph_parser.set_defaults(func=view_graph)
    contig_parser.set_defaults(func=view_contig)

    contig_parser.add_argument('contig', help='Contig to retrieve records for')
    contig_parser.add_argument('--output-type', default='term',
                               choices=[v.name for v in ViewContigChoice])

    traversal.add_arguments()


@attr.s(slots=True)
class ViewTraversal(object):
    subparsers = attr.ib()
    parser = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.parser = self.subparsers.add_parser('traversal',
                                                 help='Display a Cortex graph traversal')

    def add_arguments(self):
        parser = self.parser
        parser.set_defaults(func=view_traversal)
        parser.add_argument('initial_contig',
                            help='Start traversal from every kmer in this contig')
        parser.add_argument('--orientation', default='both',
                            choices=[o.name for o in traversal.EngineTraversalOrientation])
        parser.add_argument('--color', default=0, type=int)
        parser.add_argument('--max-nodes', default=1000, type=int)
        parser.add_argument('--output-type', default='term',
                            choices=[v.name for v in ViewTraversalChoice])


def get_file_handle(graph):
    return open(graph, 'rb')


def view_graph(args):
    print_cortex_file(get_file_handle(args.graph))


def view_contig(args):
    contig_retriever = ContigRetriever(get_file_handle(args.graph))
    if args.output_type == ViewContigChoice.term.name:
        print_contig(contig_retriever, args.contig)
    else:
        serializer = Serializer(contig_retriever.get_kmer_graph(args.contig))
        if args.output_type == ViewContigChoice.json.name:
            print(serializer.to_json())
        else:
            raise ArgparseError


def view_traversal(args):
    traverser = traversal.Engine(
        g_parser.RandomAccess(get_file_handle(args.graph)),
        color=args.color,
        orientation=traversal.EngineTraversalOrientation[args.orientation],
        max_nodes=args.max_nodes,
    )
    graph = traverser.traverse_from_each_kmer_in(args.initial_contig)
    if args.output_type == ViewTraversalChoice.json.name:
        serializer = Serializer(graph, annotate_graph_edges=True)
        print(serializer.to_json())
    elif args.output_type == ViewTraversalChoice.fasta.name:
        serializer = Serializer(graph, annotate_graph_edges=False, collapse_unitigs=False)
        SeqIO.write(serializer.to_seq_records(), sys.stdout, 'fasta')


def print_cortex_file(graph_handle):
    for kmer in kmer_generator_from_stream(graph_handle):
        print(kmer_to_cortex_jdk_print_string(kmer))


def print_contig(contig_retriever, contig):
    contig_kmers = contig_retriever.get_kmers(contig)
    for kmer, kmer_string in contig_kmers:
        print(kmer_to_cortex_jdk_print_string(kmer, alt_kmer_string=kmer_string))


def kmer_to_cortex_jdk_print_string(kmer, alt_kmer_string=None):
    is_revcomp = bool(alt_kmer_string is not None and kmer.kmer != alt_kmer_string)

    edge_set_strings = (edge_set.to_str(as_revcomp=is_revcomp) for edge_set in kmer.edges)
    to_print = [str(kmer.kmer)]
    if alt_kmer_string is not None:
        to_print.append(': ' + alt_kmer_string)
    to_print.append(' ' + ' '.join(map(str, kmer.coverage)))
    to_print.append(' ' + ' '.join(edge_set_strings))
    return ''.join(to_print)
