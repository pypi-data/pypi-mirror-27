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
# Name:        sqltable.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     27/12/2017
# -------------------------------------------------------------------------------
import operator
from spatialdb import *


class SqlTable(dict):

    def __init__(self, sql="", env={}, name="", data=None, db=None, verbose=False):
        self.db = db if db else SpatialDB.From(sql)
        sql = sql if sql else "SELECT * FROM [%s]" % (name)
        data = data if not data is None else self.db.execute(sql, env, outputmode="object", verbose=verbose)
        name = name if name else tempname("tbl_")
        super(SqlTable, self).__init__({"name": name, "data": data})

    def select(self, fieldnames="*", env=None, verbose=False):
        all_fields = (fieldnames == "*")
        fieldnames = listify(fieldnames)
        data = self["data"]
        for row in data:
            for key in row.keys():
                if key.lower() not in lower(fieldnames) and not all_fields:
                    del row[key]
        return self

    def count(self, condition=True):
        counter = 0
        condition = "%s" % (condition)
        for row in self["data"]:
            if eval(condition, {}, row):
                counter += 1
        return counter

    def where(self, condition=True, copy=False):
        data = []
        condition = "%s" % (condition)
        for row in self["data"]:
            if eval(condition, {}, row):
                data.append(row)
        if copy:
            return SqlTable(db=self.db, data=data)
        self["data"] = data
        return self

    def orderby(self, fieldnames="", order="ASC"):
        desc = order.lower() == "desc"
        fieldnames = listify(fieldnames)
        self["data"] = sorted(self["data"], key=operator.itemgetter(*fieldnames), reverse=desc)
        return self

    def per(self, sqltable):
        for row in self["data"]:
            row[sqltable["name"]] = sqltable["data"]
        return self

    def leftjoin(self, sqltable, id_a, id_b=""):
        id_b = id_b if id_b else id_a
        for row_a in self["data"]:
            for row_b in sqltable["data"]:
                if row_a[id_a] == row_b[id_b]:
                    row_a[sqltable["name"]] = row_b
                else:
                    row_b[sqltable["name"]] = None
        return self

    def innerjoin(self, sqltable, id_a, id_b=""):
        id_b = id_b if id_b else id_a
        data = []
        for row_a in self["data"]:
            for row_b in sqltable["data"]:
                if row_a[id_a] == row_b[id_b]:
                    row_a[sqltable["name"]] = row_b
                    data.append(row_a)
        self["data"] = data
        return self

    def spatialjoin(self, sqltable, id_a="geometry", id_b=""):
        id_b = id_b if id_b else id_a
        data = []
        for row_a in self["data"]:
            geom_a = ogr.CreateGeometryFromWkb(str(row_a[id_a]))
            for row_b in sqltable["data"]:
                geom_b = ogr.CreateGeometryFromWkb(str(row_b[id_b]))
                if geom_a.Intersect(geom_b):
                    row_a[sqltable["name"]] = row_b
                    data.append(row_a)

        self["data"] = data
        return self


workdir = r'D:\Users\vlr20\Projects\BitBucket\OpenSITUA\projects\Valerio\Test01'
chdir(workdir)
db = SqliteDB("riskrecombination.sqlite")
receptors = SqlTable(db=db, name="receptors")
areap = SqlTable(db=db, name="AreaPopulation")
print receptors.select("name,ogc_fid,geometry").spatialjoin(areap).count()
