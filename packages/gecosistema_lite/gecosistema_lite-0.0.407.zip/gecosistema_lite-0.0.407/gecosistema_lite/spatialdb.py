# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        spatialite.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     23/11/2017
# -------------------------------------------------------------------------------
from sqlitedb import *
import ogr

class SpatialDB(SqliteDB):

    def __init__(self, filename, modules=[]):
        """
        Constructor
        :param filename:
        """
        SqliteDB.__init__(self, filename, ["mod_spatialite"]+modules)
        self.CreateSpatialReferenceTable()
        self.CreateGeometryColumnTable()

    def CreateSpatialReferenceTable(self):
        sql = """
        CREATE TABLE [spatial_ref_sys] (
          [srid] INTEGER NOT NULL PRIMARY KEY, 
          [auth_name] TEXT NOT NULL, 
          [auth_srid] INTEGER NOT NULL, 
          [ref_sys_name] TEXT NOT NULL DEFAULT 'Unknown', 
          [proj4text] TEXT NOT NULL, 
          [srtext] TEXT NOT NULL DEFAULT 'Undefined');
        --INSERT OR REPLACE INTO [spatial_ref_sys](srid,auth_name,auth_srid,ref_sys_name,proj4text,srtext)
        --VALUES ({epsg},'epsg',{epsg},'epsg:'||{epsg},'{proj4text}','{srtext}');
        """
        self.execute(sql)

    def CreateGeometryColumnTable(self):
        sql = """
        CREATE TABLE IF NOT EXISTS [geometry_columns] (
          [f_table_name] VARCHAR, 
          [f_geometry_column] VARCHAR, 
          [geometry_type] INTEGER, 
          [coord_dimension] INTEGER, 
          [srid] INTEGER, 
          [geometry_format] VARCHAR, 
          PRIMARY KEY ([f_table_name]));
        """
        self.execute(sql)

    def CreateLayer(self, layername, epsg=3857, fieldnames="", fieldtypes="", geom_type=1, overwrite=True, verbose=False):

        srs = ogr.osr.SpatialReference()
        srs.ImportFromEPSG(epsg)

        fieldnames = ["geometry"] + listify(fieldnames)
        fieldnames = wrap(fieldnames, "[", "]")
        fieldtypes = ["BLOB"] + listify(fieldtypes)
        r = len(fieldnames) - len(fieldtypes)
        r = r if r >= 0 else 0
        fieldtypes = fieldtypes + ["TEXT"] * r
        fielddefs = [" ".join(item) for item in zip(fieldnames, fieldtypes)]
        fielddefs = ','.join(fielddefs)

        env = {
            "layername": layername,
            "epsg": epsg,
            "geom_type": geom_type,  # 1=Point,3=Polygons
            "proj4text": srs.ExportToProj4(),
            "srtext": srs.ExportToWkt(),
            "fielddefs": fielddefs,
            "if_overwrite": "" if overwrite else "--"
        }

        sql = """
        {if_overwrite}DROP TABLE IF EXISTS [{layername}];
        CREATE TABLE IF NOT EXISTS [{layername}](ogc_fid INTEGER PRIMARY KEY AUTOINCREMENT,{fielddefs});
        INSERT OR REPLACE INTO [geometry_columns]( f_table_name,f_geometry_column,geometry_type,coord_dimension,srid,geometry_format)
            VALUES('{layername}','geometry',{geom_type},2,{epsg},'WKB');
        INSERT OR REPLACE INTO [spatial_ref_sys](srid,auth_name,auth_srid,ref_sys_name,proj4text,srtext)
            VALUES ({epsg},'epsg',{epsg},'epsg:'||{epsg},'{proj4text}','{srtext}');
        """
        self.execute(sql, env, verbose=verbose)

    def GridFromExtent(self, layername, extent, dx=500.0, dy=None, verbose=False):

        [minx, miny, maxx, maxy] = extent
        minx, miny, maxx, maxy = val(minx), val(miny), val(maxx), val(maxy)
        minx, miny, maxx, maxy = min(minx, maxx), min(miny, maxy), max(minx, maxx), max(miny, maxy)

        dx = float(dx)
        dy = float(dy) if dy else dx

        width  = maxx - minx
        height = maxy - miny
        m,n = int(height / dy),int(width  / dx)

        values = []
        for i in range(m):
            for j in range(n):
                x = minx + (dx / 2.0) + (dx * j)
                y = miny + (dy / 2.0) + (dy * i)
                point = ogr.Geometry(ogr.wkbPoint)
                point.AddPoint_2D(x, y)
                blob = point.ExportToIsoWkb()
                values.append((blob,))

        self.executemany("""INSERT OR REPLACE INTO [{layername}](geometry) VALUES(?);""", {"layername": layername}, values, verbose=verbose)

def main():

    workdir = "c:/users/vlr20/Desktop"
    chdir(workdir)
    db = SpatialDB("test.sqlite")
    db.CreateLayer("layer1")
    db.GridFromExtent("layer1", [0,0,1000,1000], 10)
    db.close()

if __name__ == "__main__":
    main()