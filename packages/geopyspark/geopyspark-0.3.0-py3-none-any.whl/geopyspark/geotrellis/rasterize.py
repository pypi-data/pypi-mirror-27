import shapely.wkb
from geopyspark import get_spark_context
from geopyspark.geotrellis.constants import LayerType, CellType
from geopyspark.geotrellis.layer import TiledRasterLayer


__all__ = ['rasterize']


def rasterize(geoms, crs, zoom, fill_value, cell_type=CellType.FLOAT64, options=None, num_partitions=None):
    """Rasterizes a Shapely geometries.

    Args:
        geoms ([shapely.geometry]): List of shapely geometries to rasterize.
        crs (str or int): The CRS of the input geometry.
        zoom (int): The zoom level of the output raster.
        fill_value (int or float): Value to burn into pixels intersectiong geometry
        cell_type (str or :class:`~geopyspark.geotrellis.constants.CellType`): Which data type the
            cells should be when created. Defaults to ``CellType.FLOAT64``.
        options (:class:`~geopyspark.geotrellis.RasterizerOptions`, optional): Pixel intersection options.
        num_partitions (int, optional): The number of repartitions Spark will make when the data is
            repartitioned. If ``None``, then the data will not be repartitioned.

    Returns:
        :class:`~geopyspark.geotrellis.layer.TiledRasterLayer`
    """

    if isinstance(crs, int):
        crs = str(crs)

    pysc = get_spark_context()
    wkb_geoms = [shapely.wkb.dumps(g) for g in geoms]
    srdd = pysc._gateway.jvm.geopyspark.geotrellis.SpatialTiledRasterLayer.rasterizeGeometry(pysc._jsc.sc(),
                                                                                             wkb_geoms,
                                                                                             crs,
                                                                                             zoom,
                                                                                             float(fill_value),
                                                                                             CellType(cell_type).value,
                                                                                             options,
                                                                                             num_partitions)
    return TiledRasterLayer(LayerType.SPATIAL, srdd)
