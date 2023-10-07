from osgeo import gdal
from typing import Union
import geopandas as gpd
import matplotlib.pyplot as plt

class Geo:

    def tif_to_png(tif_path: str, output_path: str) -> Union[None, str]:
        """
        Converts a TIF file to PNG format.

        Args:
        tif_path (str): The path to the input TIF file.
        output_path (str): The path for the output PNG file.

        Returns:
        Union[None, str]: Returns None on success, or an error message as a string.
        """
        try:
            dataset = gdal.Open(tif_path)
            if dataset is None:
                return "Error: Failed to open TIF file."
        
            width = dataset.RasterXSize
            height = dataset.RasterYSize

            PNG_Driver = gdal.GetDriverByName('PNG')
            PNG_ds = PNG_Driver.Create(output_path, width, height, dataset.RasterCount, gdal.GDT_Byte)
            PNG_ds.SetProjection(dataset.GetProjection())
            PNG_ds.SetGeoTransform(dataset.GetGeoTransform())

            for i in range(1, dataset.RasterCount + 1):
                band = dataset.GetRasterBand(i)
                data = band.ReadAsArray()
                PNG_ds.GetRasterBand(i).WriteArray(data)
                PNG_ds.FlushCache()

            PNG_ds = None
            dataset = None
            return None  # Successful conversion
        except Exception as e:
            return str(e)  # Return the error message as a string
    
    def shp_to_png(shp_path: str, output_path: str,dpi:int):
        """
        Converts a Shapefile file to PNG format.

        Args:
        tif_path (str): The path to the input shapefile file.
        output_path (str): The path for the output PNG file.
        dpi(int):the dpi of the result.(genrally 300/600)

        Returns:
        Union[None, str]: Returns None on success, or an error message as a string.
        """
        try:
            shp = gpd.read_file(shp_path)
            if shp is None:
                return "Error: Failed to open TIF file."
            else:
                fig,ax = plt.subplots()
                shp.plot(ax=ax)
                plt.xticks([]) 
                plt.yticks([])
                plt.axis('off')
                plt.savefig(output_path,dpi=dpi,bbox_inches='tight')
                print('OK!')
                plt.close()
        except Exception as e:
            return str(e)
    
    