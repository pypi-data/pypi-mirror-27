import os
import sys
import math
import numpy as np
import pytest
import unittest

from geopyspark.geotrellis import Extent, ProjectedExtent, Tile
from geopyspark.geotrellis.layer import RasterLayer
from geopyspark.geotrellis.constants import LayerType, NO_DATA_INT, ClassificationStrategy
from geopyspark.tests.base_test_class import BaseTestClass


class ReclassifyTest(BaseTestClass):
    epsg_code = 3857
    extent = Extent(0.0, 0.0, 10.0, 10.0)
    projected_extent = ProjectedExtent(extent, epsg_code)

    @pytest.fixture(autouse=True)
    def tearDown(self):
        yield
        BaseTestClass.pysc._gateway.close()

    def test_tuple_key(self):
        arr = np.zeros((1, 16, 16))
        tile = Tile(arr, 'FLOAT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {(0, 1): 1}

        result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells

        self.assertTrue((result == 1).all())

    def test_list_bad(self):
        arr = np.zeros((1, 16, 16))
        tile = Tile(arr, 'FLOAT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {'apple, orange, banana': 1}

        with pytest.raises(TypeError):
            result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells


    def test_all_zeros(self):
        arr = np.zeros((1, 16, 16))
        tile = Tile(arr, 'FLOAT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {0: 1}

        result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells

        self.assertTrue((result == 1).all())

    def test_various_values(self):
        arr = np.array([[[1, 1, 1, 1],
                         [2, 2, 2, 2],
                         [3, 3, 3, 3],
                         [4, 4, 4, 4]]], dtype=int)
        tile = Tile(arr, 'INT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {1: 10, 3: 17}

        result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells

        expected = np.array([[[10, 10, 10, 10],
                              [17, 17, 17, 17],
                              [17, 17, 17, 17],
                              [-500, -500, -500, -500]]], dtype=int)

        self.assertTrue((result == expected).all())

    def test_ranges(self):
        arr = np.array([[[1, 1, 1, 1],
                         [2, 2, 2, 2],
                         [3, 3, 3, 3],
                         [4, 4, 4, 4]]], dtype=int)
        tile = Tile(arr, 'INT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {2: 20}

        result = raster_rdd.reclassify(value_map, int,
                                       ClassificationStrategy.GREATER_THAN).to_numpy_rdd().first()[1].cells

        expected = np.array([[[-500, -500, -500, -500],
                              [-500, -500, -500, -500],
                              [20, 20, 20, 20],
                              [20, 20, 20, 20]]], dtype=int)

        self.assertTrue((result == expected).all())

    def test_multibands(self):
        arr = np.array([[[1, 1, 1, 1]],
                        [[2, 2, 2, 2]],
                        [[3, 3, 3, 3]],
                        [[4, 4, 4, 4]]], dtype=int)
        tile = Tile(arr, 'INT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {3: 10, 4: 20}

        result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells

        expected = np.array([[[10, 10, 10, 10]],
                             [[10, 10, 10, 10]],
                             [[10, 10, 10, 10]],
                             [[20, 20, 20, 20]]], dtype=int)

        self.assertTrue((result == expected).all())

    def test_floating_voint_ranges(self):
        arr = np.array([[[0.0, 0.0, 0.0, 0.0],
                         [1.0, 1.0, 1.0, 1.0],
                         [1.5, 1.5, 1.5, 1.5],
                         [2.0, 2.0, 2.0, 2.0]]], dtype=float)

        tile = Tile(arr, 'FLOAT', float('nan'))
        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {2.0: 5.0}

        result = raster_rdd.reclassify(value_map, float,
                                       ClassificationStrategy.LESS_THAN).to_numpy_rdd().first()[1].cells

        expected = np.array([[[5.0, 5.0, 5.0, 5.0],
                              [5.0, 5.0, 5.0, 5.0],
                              [5.0, 5.0, 5.0, 5.0]]], dtype=float)

        self.assertTrue((result[0, 2, ] == expected).all())
        for x in result[0, 3, ]:
            self.assertTrue(math.isnan(x))

    def test_no_data_ints(self):
        arr = np.zeros((1, 16, 16), dtype=int)
        tile = Tile(arr, 'INT', NO_DATA_INT)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {0: NO_DATA_INT}

        result = raster_rdd.reclassify(value_map, int).to_numpy_rdd().first()[1].cells

        self.assertTrue((result == NO_DATA_INT).all())

    def test_no_data_floats(self):
        arr = np.array([[[0.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 0.0]]], dtype=float)
        tile = Tile(arr, 'FLOAT', float('nan'))

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {0.0: float('nan')}

        result = raster_rdd.reclassify(value_map, float).to_numpy_rdd().first()[1].cells

        for x in list(result.flatten()):
            self.assertTrue(math.isnan(x))

    @pytest.mark.skipif('TRAVIS' in os.environ,
                         reason="Encoding using methods in Main causes issues on Travis")
    def test_ignore_no_data_ints(self):
        arr = np.ones((1, 16, 16), int)
        np.fill_diagonal(arr[0], NO_DATA_INT)
        tile = Tile(arr, 'INT', NO_DATA_INT)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {1: 0}

        result = raster_rdd.reclassify(value_map, int, replace_nodata_with=1).to_numpy_rdd().first()[1].cells

        self.assertTrue((result == np.identity(16, int)).all())

    @pytest.mark.skipif('TRAVIS' in os.environ,
                         reason="Encoding using methods in Main causes issues on Travis")
    def test_ignore_no_data_floats(self):
        arr = np.ones((1, 4, 4))
        np.fill_diagonal(arr[0], float('nan'))
        tile = Tile(arr, 'FLOAT', float('nan'))

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(LayerType.SPATIAL, rdd)

        value_map = {1.0: 0.0}

        result = raster_rdd.reclassify(value_map, float, replace_nodata_with=1.0).to_numpy_rdd().first()[1].cells

        self.assertTrue((result == np.identity(4)).all())

if __name__ == "__main__":
    unittest.main()
