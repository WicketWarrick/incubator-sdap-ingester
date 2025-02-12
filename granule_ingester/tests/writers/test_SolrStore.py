import json
import unittest

from nexusproto import DataTile_pb2 as nexusproto

from granule_ingester.writers import SolrStore


class TestSolrStore(unittest.TestCase):

    def test_build_solr_doc(self):
        tile = nexusproto.NexusTile()
        tile.summary.tile_id = 'test_id'
        tile.summary.dataset_name = 'test_dataset'
        tile.summary.dataset_uuid = 'test_dataset_id'
        tile.summary.data_var_name = json.dumps(['test_variable'])
        tile.summary.granule = 'test_granule_path'
        tile.summary.section_spec = 'time:0:1,j:0:20,i:200:240'
        tile.summary.bbox.lat_min = -180.1
        tile.summary.bbox.lat_max = 180.2
        tile.summary.bbox.lon_min = -90.5
        tile.summary.bbox.lon_max = 90.0
        tile.summary.stats.min = -10.0
        tile.summary.stats.max = 25.5
        tile.summary.stats.mean = 12.5
        tile.summary.stats.count = 100
        tile.summary.stats.min_time = 694224000
        tile.summary.stats.max_time = 694310400
        tile.summary.standard_name = 'sea_surface_temperature'

        tile.tile.ecco_tile.depth = 10.5

        metadata_store = SolrStore()
        solr_doc = metadata_store._build_solr_doc(tile)

        self.assertEqual('sea_surface_temp', solr_doc['table_s'])
        self.assertEqual(
            'POLYGON((-90.500 -180.100, 90.000 -180.100, 90.000 180.200, -90.500 180.200, -90.500 -180.100))',
            solr_doc['geo'])
        self.assertEqual('test_id', solr_doc['id'])
        self.assertEqual('test_dataset!test_id', solr_doc['solr_id_s'])
        self.assertEqual('time:0:1,j:0:20,i:200:240', solr_doc['sectionSpec_s'])
        self.assertEqual('test_granule_path', solr_doc['granule_s'])
        self.assertEqual('sea_surface_temperature', solr_doc['tile_var_name_s'])
        self.assertAlmostEqual(-90.5, solr_doc['tile_min_lon'])
        self.assertAlmostEqual(90.0, solr_doc['tile_max_lon'])
        self.assertAlmostEqual(-180.1, solr_doc['tile_min_lat'], delta=1E-5)
        self.assertAlmostEqual(180.2, solr_doc['tile_max_lat'], delta=1E-5)
        self.assertEqual('1992-01-01T00:00:00Z', solr_doc['tile_min_time_dt'])
        self.assertEqual('1992-01-02T00:00:00Z', solr_doc['tile_max_time_dt'])
        self.assertAlmostEqual(-10.0, solr_doc['tile_min_val_d'])
        self.assertAlmostEqual(25.5, solr_doc['tile_max_val_d'])
        self.assertAlmostEqual(12.5, solr_doc['tile_avg_val_d'])
        self.assertEqual(100, solr_doc['tile_count_i'])
        self.assertAlmostEqual(10.5, solr_doc['tile_depth'])

    def test_build_solr_doc_no_standard_name_02(self):
        tile = nexusproto.NexusTile()
        tile.summary.tile_id = 'test_id'
        tile.summary.dataset_name = 'test_dataset'
        tile.summary.dataset_uuid = 'test_dataset_id'
        tile.summary.data_var_name = json.dumps(['test_variable', 'test_variable_02'])
        tile.summary.granule = 'test_granule_path'
        tile.summary.section_spec = 'time:0:1,j:0:20,i:200:240'
        tile.summary.bbox.lat_min = -180.1
        tile.summary.bbox.lat_max = 180.2
        tile.summary.bbox.lon_min = -90.5
        tile.summary.bbox.lon_max = 90.0
        tile.summary.stats.min = -10.0
        tile.summary.stats.max = 25.5
        tile.summary.stats.mean = 12.5
        tile.summary.stats.count = 100
        tile.summary.stats.min_time = 694224000
        tile.summary.stats.max_time = 694310400

        tile.tile.ecco_tile.depth = 10.5

        metadata_store = SolrStore()
        solr_doc = metadata_store._build_solr_doc(tile)

        self.assertEqual('sea_surface_temp', solr_doc['table_s'])
        self.assertEqual(
            'POLYGON((-90.500 -180.100, 90.000 -180.100, 90.000 180.200, -90.500 180.200, -90.500 -180.100))',
            solr_doc['geo'])
        self.assertEqual('test_id', solr_doc['id'])
        self.assertEqual('test_dataset!test_id', solr_doc['solr_id_s'])
        self.assertEqual('time:0:1,j:0:20,i:200:240', solr_doc['sectionSpec_s'])
        self.assertEqual('test_granule_path', solr_doc['granule_s'])
        self.assertEqual(['test_variable', 'test_variable_02'], solr_doc['tile_var_name_s'])
        self.assertAlmostEqual(-90.5, solr_doc['tile_min_lon'])
        self.assertAlmostEqual(90.0, solr_doc['tile_max_lon'])
        self.assertAlmostEqual(-180.1, solr_doc['tile_min_lat'], delta=1E-5)
        self.assertAlmostEqual(180.2, solr_doc['tile_max_lat'], delta=1E-5)
        self.assertEqual('1992-01-01T00:00:00Z', solr_doc['tile_min_time_dt'])
        self.assertEqual('1992-01-02T00:00:00Z', solr_doc['tile_max_time_dt'])
        self.assertAlmostEqual(-10.0, solr_doc['tile_min_val_d'])
        self.assertAlmostEqual(25.5, solr_doc['tile_max_val_d'])
        self.assertAlmostEqual(12.5, solr_doc['tile_avg_val_d'])
        self.assertEqual(100, solr_doc['tile_count_i'])
        self.assertAlmostEqual(10.5, solr_doc['tile_depth'])

    def test_build_solr_doc_no_standard_name(self):
        """
        When TileSummary.standard_name isn't available, the solr field
        tile_var_name_s should use TileSummary.data_var_name
        """
        tile = nexusproto.NexusTile()
        tile.summary.tile_id = 'test_id'
        tile.summary.data_var_name = json.dumps(['test_variable', 'test_variable_02'])
        tile.tile.ecco_tile.depth = 10.5

        metadata_store = SolrStore()
        solr_doc = metadata_store._build_solr_doc(tile)

        self.assertEqual(['test_variable', 'test_variable_02'], solr_doc['tile_var_name_s'])
