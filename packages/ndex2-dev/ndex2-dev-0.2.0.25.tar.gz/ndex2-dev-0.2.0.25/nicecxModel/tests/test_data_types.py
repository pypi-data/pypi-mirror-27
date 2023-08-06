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
            if found_int_type:
                break
            if niceCx.get_node_attributes(node) is not None:
                for node_attr in niceCx.get_node_attributes(node):
                    if node_attr.get_data_type() == ATTRIBUTE_DATA_TYPE.INTEGER:
                        found_int_type = True
                        break

        self.assertTrue(found_int_type)

        print(niceCx.__str__())

    #@unittest.skip("Temporary skipping") # PASS
    def test_node_data_types_from_tsv(self):
        path_to_network = os.path.join(path_this, 'mgdb_mutations.txt')

        with open(path_to_network, 'rU') as tsvfile:
            header = [h.strip() for h in tsvfile.readline().split('\t')]

            df = pd.read_csv(tsvfile,delimiter='\t',engine='python',names=header)

            niceCx = ndex2.create_nice_cx_from_pandas(df, source_field='CDS Mutation', target_field='Gene Symbol', source_node_attr=['Primary Tissue', 'Histology', 'Genomic Locus'], target_node_attr=['Gene ID'], edge_interaction='variant-gene-relationship') #NiceCXNetwork()

            upload_message = niceCx.upload_to(upload_server, upload_username, upload_password)
            self.assertTrue(upload_message)

