__author__ = 'aarongary'

import unittest

import sys
import json
import pandas as pd
import csv
import networkx as nx
import ndex2
import os
from nicecxModel.NiceCXNetwork import NiceCXNetwork
from ndex2.client import DecimalEncoder
from ndex.networkn import NdexGraph
from nicecxModel.cx.aspects import ATTRIBUTE_DATA_TYPE

upload_server = 'dev.ndexbio.org'
upload_username = 'scratch'
upload_password = 'scratch'

path_this = os.path.dirname(os.path.abspath(__file__))

class TestLoadByAspects(unittest.TestCase):
    @unittest.skip("Temporary skipping")
    def test_node_data_types(self):
        niceCx = ndex2.create_nice_cx_from_server(server='public.ndexbio.org', uuid='fc63173e-df66-11e7-adc1-0ac135e8bacf') #NiceCXNetwork(server='dev2.ndexbio.org', username='scratch', password='scratch', uuid='9433a84d-6196-11e5-8ac5-06603eb7f303')
        found_int_type = False
        for node in niceCx.get_nodes():
            abc_node_attrs = niceCx.get_node_attributes(node)

            if abc_node_attrs is not None:
                for node_attr in abc_node_attrs:
                    if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.INTEGER:
                        found_int_type = True

        self.assertTrue(found_int_type)

        print(niceCx.__str__())

    @unittest.skip("Temporary skipping") # PASS
    def test_node_data_types_from_tsv(self):
        path_to_network = os.path.join(path_this, 'mgdb_mutations.txt')

        with open(path_to_network, 'rU') as tsvfile:
            header = [h.strip() for h in tsvfile.readline().split('\t')]

            df = pd.read_csv(tsvfile,delimiter='\t',engine='python',names=header)

            niceCx = ndex2.create_nice_cx_from_pandas(df, source_field='CDS Mutation', target_field='Gene Symbol', source_node_attr=['Primary Tissue', 'Histology', 'Genomic Locus'], target_node_attr=['Gene ID'], edge_interaction='variant-gene-relationship') #NiceCXNetwork()

            found_int_type = False
            for node in niceCx.get_nodes():
                abc_node_attrs = niceCx.get_node_attributes(node)

                if abc_node_attrs is not None:
                    for node_attr in abc_node_attrs:
                        if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.INTEGER:
                            found_int_type = True

            self.assertTrue(found_int_type)

    @unittest.skip("Temporary skipping") # PASS
    def test_data_types_from_networkx(self):
        G = nx.Graph()
        G.add_node('ABC')
        G.add_node('DEF')
        G.add_node('GHI')
        G.add_node('JKL')
        G.add_node('MNO')
        G.add_node('PQR')
        G.add_node('XYZ')

        G.add_edges_from([('ABC','DEF'), ('DEF', 'GHI'),('GHI', 'JKL'),
                          ('DEF', 'JKL'), ('JKL', 'MNO'), ('DEF', 'MNO'),
                         ('MNO', 'XYZ'), ('DEF', 'PQR')])

        attribute_floats = {
            'ABC': 1.234,
            'DEF': 1.345,
            'GHI': 1.456,
            'JKL': 1.567,
            'MNO': 1.678
        }

        attribute_integers = {
            'ABC': 1,
            'DEF': 2,
            'GHI': 3,
            'JKL': 4,
            'MNO': 5
        }

        nx.set_node_attributes(G, 'floatLabels', attribute_floats)
        nx.set_node_attributes(G, 'integerLabels', attribute_integers)

        G['ABC']['DEF']['weight'] = 0.321
        G['DEF']['GHI']['weight'] = 0.434
        G['GHI']['JKL']['weight'] = 0.555
        G['MNO']['XYZ']['weight'] = 0.987

        niceCx_full = ndex2.create_nice_cx_from_networkx(G)

        abc_node_attrs = niceCx_full.get_node_attributes('ABC')

        found_int_type = False
        found_float_type = False
        if abc_node_attrs is not None:
            for node_attr in abc_node_attrs:
                if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.INTEGER:
                    found_int_type = True
                if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.FLOAT:
                    found_float_type = True

        found_edge_float_type = False
        for edge in niceCx_full.get_edges():
            edge_attrs = niceCx_full.get_edge_attributes(edge)
            if edge_attrs is not None:
                for edge_attr in edge_attrs:
                    if edge_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.FLOAT:
                        found_edge_float_type = True

        self.assertTrue(found_int_type)
        self.assertTrue(found_float_type)
        self.assertTrue(found_edge_float_type)

    #@unittest.skip("Temporary skipping") # PASS
    def test_data_types_with_special_chars(self):
        path_to_network = os.path.join(path_this, 'Metabolism_of_RNA_data_types.cx')

        with open(path_to_network, 'rU') as data_types_cx:
            #============================
            # BUILD NICECX FROM CX FILE
            #============================
            niceCx = ndex2.create_nice_cx_from_cx(cx=json.load(data_types_cx))

            found_list_of_strings_type = False
            for node in niceCx.get_nodes():
                abc_node_attrs = niceCx.get_node_attributes(node)

                if abc_node_attrs is not None:
                    for node_attr in abc_node_attrs:
                        if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.LIST_OF_STRING:
                            found_list_of_strings_type = True

            self.assertTrue(found_list_of_strings_type)
