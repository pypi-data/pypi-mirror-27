"""
Raster file input which can be read by rasterio.

Currently limited by extensions .tif, .vrt., .png and .jp2 but could be
extended easily.
"""

import os
import rasterio
from shapely.geometry import box
from cached_property import cached_property
from copy import deepcopy

from mapchete.formats import base
from mapchete.io.vector import reproject_geometry, segmentize_geometry
from mapchete.io.raster import read_raster_window


METADATA = {
    "driver_name": "raster_file",
    "data_type": "raster",
    "mode": "r",
    "file_extensions": ["tif", "vrt", "png", "jp2"]
}


class InputData(base.InputData):
    """
    Main input class.

    Parameters
    ----------
    input_params : dictionary
        driver specific parameters

    Attributes
    ----------
    path : string
        path to input file
    profile : dictionary
        rasterio metadata dictionary
    pixelbuffer : integer
        buffer around output tiles
    pyramid : ``tilematrix.TilePyramid``
        output ``TilePyramid``
    crs : ``rasterio.crs.CRS``
        object describing the process coordinate reference system
    srid : string
        spatial reference ID of CRS (e.g. "{'init': 'epsg:4326'}")
    """

    METADATA = {
        "driver_name": "raster_file",
        "data_type": "raster",
        "mode": "r",
        "file_extensions": ["tif", "vrt", "png", "jp2"]
    }

    def __init__(self, input_params):
        """Initialize."""
        super(InputData, self).__init__(input_params)
        self.path = input_params["path"]

    @cached_property
    def profile(self):
        """Return raster metadata."""
        with rasterio.open(self.path, "r") as src:
            return deepcopy(src.meta)

    def open(self, tile, **kwargs):
        """
        Return InputTile object.

        Parameters
        ----------
        tile : ``Tile``

        Returns
        -------
        input tile : ``InputTile``
            tile view of input data
        """
        return InputTile(tile, self, **kwargs)

    def bbox(self, out_crs=None):
        """
        Return data bounding box.

        Parameters
        ----------
        out_crs : ``rasterio.crs.CRS``
            rasterio CRS object (default: CRS of process pyramid)

        Returns
        -------
        bounding box : geometry
            Shapely geometry object
        """
        if out_crs is None:
            out_crs = self.pyramid.crs
        with rasterio.open(self.path) as inp:
            inp_crs = inp.crs
            out_bbox = bbox = box(*inp.bounds)
        # If soucre and target CRSes differ, segmentize and reproject
        if inp_crs != out_crs:
            # estimate segmentize value (raster pixel size * tile size)
            # and get reprojected bounding box
            return reproject_geometry(
                segmentize_geometry(
                    bbox, inp.transform[0] * self.pyramid.tile_size
                ),
                src_crs=inp_crs, dst_crs=out_crs
            )
        else:
            return out_bbox

    def exists(self):
        """
        Check if data or file even exists.

        Returns
        -------
        file exists : bool
        """
        return os.path.isfile(self.path)


class InputTile(base.InputTile):
    """
    Target Tile representation of input data.

    Parameters
    ----------
    tile : ``Tile``
    kwargs : keyword arguments
        driver specific parameters

    Attributes
    ----------
    tile : tile : ``Tile``
    raster_file : ``InputData``
        parent InputData object
    resampling : string
        resampling method passed on to rasterio
    """

    def __init__(self, tile, raster_file, resampling="nearest"):
        """Initialize."""
        self.tile = tile
        self.raster_file = raster_file
        self.resampling = resampling

    def read(self, indexes=None):
        """
        Read reprojected & resampled input data.

        Returns
        -------
        data : array
        """
        return read_raster_window(
            self.raster_file.path,
            self.tile,
            indexes=self._get_band_indexes(indexes),
            resampling=self.resampling
        )

    def is_empty(self, indexes=None):
        """
        Check if there is data within this tile.

        Returns
        -------
        is empty : bool
        """
        # empty if tile does not intersect with file bounding box
        return not self.tile.bbox.intersects(
            self.raster_file.bbox(out_crs=self.tile.crs)
        )

    def _get_band_indexes(self, indexes=None):
        """Return valid band indexes."""
        if indexes:
            if isinstance(indexes, list):
                return indexes
            else:
                return [indexes]
        else:
            return range(1, self.raster_file.profile["count"] + 1)


def get_segmentize_value(input_file=None, tile_pyramid=None):
    """
    Return the recommended segmentation value in input file units.

    It is calculated by multiplyling raster pixel size with tile shape in
    pixels.

    Parameters
    ----------
    input_file : str
        location of a file readable by rasterio
    tile_pyramied : ``TilePyramid`` or ``BufferedTilePyramid``
        tile pyramid to estimate target tile size

    Returns
    -------
    segmenize value : float
        length suggested of line segmentation to reproject file bounds
    """
    with rasterio.open(input_file, "r") as input_raster:
        pixelsize = input_raster.transform[0]
    return pixelsize * tile_pyramid.tile_size
