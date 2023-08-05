"""
Spatial geometric elements.

:Classes:

    ================= ==============================================================
    :class:`Geometry` base class for all geometries
    :class:`Point`    (x, y, z) point
    :class:`Point2`   pair of :class:`Point` instances that define a line, or extent
    :class:`PPoint`   multiple :class:`Point` instances
    ================= ==============================================================

.. note::

    Regression tests provide usage examples: 
    `geometry tests <https://github.com/GeosoftInc/gxpy/blob/master/geosoft/gxpy/tests/test_geometry.py>`_

"""
import numpy as np
import numbers
from collections.abc import Sequence

import geosoft
from . import coordinate_system as gxcs
from . import vv as gxvv

__version__ = geosoft.__version__

def _t(s):
    return geosoft.gxpy.system.translate(s)

def _same_cs(a, b):
    if (a._cs is None or b._cs is None) or (a._cs == b._cs):
        return True
    else:
        if isinstance(a._cs, gxcs.Coordinate_system) or isinstance(b._cs, gxcs.Coordinate_system):
            return a.coordinate_system == b.coordinate_system
        return False


class GeometryException(Exception):
    """
    Exceptions from :mod:`geosoft.gxpy.geometry`.
    """
    pass

class Geometry:
    """
    Geometry base class for all geometries.

    :Parameters:

        :coordinate_system: `geosoft.gxpy.coordinate_system.Coordinate_system` instance.

    .. versionadded:: 9.2
    """

    def __enter__(self):
        return self

    def __exit__(self, xtype, xvalue, xtraceback):
        pass

    def __repr__(self):
        return "{}({})".format(self.__class__, self.__dict__)

    def __init__(self, coordinate_system=None):
        self._cs = coordinate_system

    def __eq__(self, other):
        return _same_cs(self, other)

    @property
    def coordinate_system(self):
        """`geosoft.gxpy.coordinate_system.Coordinate_system` instance.  Can be set."""
        if (self._cs is not None) and not isinstance(self._cs, gxcs.Coordinate_system):
            self._cs = gxcs.Coordinate_system(self._cs)
        return self._cs

    @coordinate_system.setter
    def coordinate_system(self, cs):
        self._cs = cs


class Point(Geometry):
    """
    Spatial location (x,y,z).  Basic instance arithmetic and equality testing is supported.

    :Parameters:

        :p: point in one of the following forms:

                `Point` instance, returns a copy

                (x, y [,z]) implied z is 0.0 if not provided

                k makes a point (k, k, k)

    :Properties:

        :x, y, z:   point ordinate values
        :xy:        (x, y) tuple
        :xyz:       (x, y, z) tuple

    .. versionadded:: 9.2
    """

    def __str__(self):
        return "({}, {}, {})".format(self.x(), self.y(), self.z())

    def __init__(self, p, **kwargs):

        super().__init__(**kwargs)

        if hasattr(p, "__len__"):
            if len(p) > 2:
                self.p = np.array(p[:3], dtype=float)
            elif len(p) == 2:
                self.p = np.array((p[0], p[1], 0.0))
            else:
                self.p = np.array((p[0], p[0], p[0]), dtype=float)
        else:
            if isinstance(p, Point):
                self.p = p.p.copy()
            else:
                self.p = np.array((p, p, p))

    def __add__(self, p):
        if not isinstance(p, Point):
            p = Point(p)
        return Point(self.p + p.p)

    def __sub__(self, p):
        if not isinstance(p, Point):
            p = Point(p)
        return Point(self.p - p.p)

    def __neg__(self):
        return Point(-self.p)

    def __mul__(self, p):
        if not isinstance(p, Point):
            p = Point(p)
        return Point(self.p * p.p)

    def __truediv__(self, p):
        if not isinstance(p, Point):
            p = Point(p)
        return Point(self.p / p.p)

    def __eq__(self, other):
        if not _same_cs(self, other):
            return False
        return np.array_equal(self.p, other.p)

    @property
    def x(self):
        """ x value, can be set"""
        return self.p[0]

    @x.setter
    def x(self, value):
        self.p[0] = float(value)

    @property
    def y(self):
        """ y value, can be set"""
        return self.p[1]

    @y.setter
    def y(self, value):
        self.p[1] = float(value)

    @property
    def z(self):
        """ z value, can be set"""
        return self.p[2]

    @z.setter
    def z(self, value):
        self.p[2] = float(value)

    @property
    def xy(self):
        """ (x, y), can be set"""
        return (self.p[0], self.p[1])

    @xy.setter
    def xy(self, xy):
        self.p[0] = float(xy[0])
        self.p[1] = float(xy[1])

    @property
    def xyz(self):
        """ (x, y, z), can be set"""
        return (self.p[0], self.p[1], self.p[2])

    @xyz.setter
    def xyz(self, xyz):
        self.p[0] = float(xyz[0])
        self.p[1] = float(xyz[1])
        self.p[2] = float(xyz[2])

    def copy(self):
        """ return a copy as a :class:`Point` instance"""
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

class Point2(Geometry):
    """
    Two points, for a line, or a rectangle, or a cube.  Basic instance arithmetic and equality testing is supported.

    :Parameters:

        :p: Points in one of the following forms:

                (`Point`, `Point`)

                ((x, y [,z]), (x, y [,z])) implied z is 0 if not specified

                (x0, y0, x1, y1) implied z is 0

                (x0, y0, z0, x1, y1, z1)
                        
    :Properties:
    
        :p0:            first `Point` instance
        :p1:            second `Point` instance
        :x2, y2, z2:    tuple pairs for (x0, x1), (y0, y1), (z0, z1)
        :centroid:      center of the two points as a `Point`
        :dimension:     (dx, dy, dz) dimension defines by two points.

    .. versionadded:: 9.2
    """

    def __str__(self):
        return "Point2[({}, {}, {}) ({}, {}, {})]".format(self.p0.x, self.p0.y, self.p0.z,
                                                          self.p1.x, self.p1.y, self.p1.z)

    def __init__(self, p, **kwargs):

        super().__init__(**kwargs)

        if not hasattr(p, '__iter__'):
            self.p0 = self.p1 = Point(p)
        if len(p) == 2:
            self.p0 = Point(p[0])
            self.p1 = Point(p[1])
        elif len(p) == 4:
            self.p0 = Point((p[0], p[1]))
            self.p1 = Point((p[2], p[3]))
        elif len(p) == 6:
            self.p0 = Point((p[0], p[1], p[2]))
            self.p1 = Point((p[3], p[4], p[5]))
        else:
            raise GeometryException(_t('Invalid points: {}').format(p))

    def __eq__(self, other):
        if not _same_cs(self, other):
            return False
        return ((self.p0 == other.p0) and (self.p1 == other.p1)
                 or (self.p0 == other.p1) and (self.p1 == other.p0))

    def __add__(self, p):
        if isinstance(p, Point2):
            return Point2((self.p0 + p.p0, self.p1 + p.p1))
        else:
            if not isinstance(p, Point):
                p = Point(p)
            return Point2((self.p0 + p, self.p1 + p))

    def __sub__(self, p):
        if isinstance(p, Point2):
            return Point2((self.p0 - p.p0, self.p1 - p.p1))
        else:
            if not isinstance(p, Point):
                p = Point(p)
            return Point2((self.p0 - p, self.p1 - p))

    def __neg__(self):
        return Point2((-self.p0, -self.p1))

    def __mul__(self, p):
        if isinstance(p, Point2):
            return Point2((self.p0 * p.p0, self.p1 * p.p1))
        else:
            if not isinstance(p, Point):
                p = Point(p)
            return Point2((self.p0 * p, self.p1 * p))

    def __truediv__(self, p):
        if isinstance(p, Point2):
            return Point2((self.p0 / p.p0, self.p1 / p.p1))
        if not isinstance(p, Point):
            p = Point(p)
            return Point2((self.p0 / p, self.p1 / p))

    def copy(self):
        """return a copy as a :class:`Point2` instance"""
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    @property
    def x2(self):
        """(x0, x1), can be set"""
        return self.p0.x, self.p1.x

    @x2.setter
    def x2(self, value):
        self.p0.x = value[0]
        self.p1.x = value[1]

    @property
    def y2(self):
        """ (y0, y1), can be set"""
        return self.p0.y, self.p1.y

    @y2.setter
    def y2(self, value):
        self.p0.y = value[0]
        self.p1.y = value[1]

    @property
    def z2(self):
        """ (z0, z1), can be set"""
        return self.p0.z, self.p1.z

    @z2.setter
    def z2(self, value):
        self.p0.z = value[0]
        self.p1.z = value[1]


    @property
    def centroid(self):
        """ centroid on the line as a :class:`Point` instance"""
        cx = (self.p1.x + self.p0.x) * 0.5
        cy = (self.p1.y + self.p0.y) * 0.5
        cz = (self.p1.z + self.p0.z) * 0.5
        return Point((cx, cy, cz))

    @property
    def dimension(self):
        """ dimensions as (dx, dy, dz)"""
        dx = abs(self.p1.x - self.p0.x)
        dy = abs(self.p1.y - self.p0.y)
        dz = abs(self.p1.z - self.p0.z)
        return (dx, dy, dz)

    @property
    def extent_xyz(self):
        """Extent as (xmin, ymin, zmin, xmax, ymax, zmax)"""
        return min(self.p0.x, self.p1.x), min(self.p0.y, self.p1.y), min(self.p0.z, self.p1.z), \
               max(self.p0.x, self.p1.x), max(self.p0.y, self.p1.y), max(self.p0.z, self.p1.z)

    @property
    def extent_xy(self):
        """Extent as (xmin, ymin, xmax, ymax)"""
        return min(self.p0.x, self.p1.x), min(self.p0.y, self.p1.y), \
               max(self.p0.x, self.p1.x), max(self.p0.y, self.p1.y)

class PPoint(Geometry, Sequence):
    """
    Poly-Point class. Basic instance arithmetic and equality testing is supported.

    :Parameters:

        :xyz:   array-like: (p1, p2, ...), ((x, y), ...), ((x, y, z), ...) or (vv_x, vv_y, [vv_z]).

                vv data is resampled to match the first vv.

        :z:     constant z value for (x, y) data, ignored for (x, y, z) data

    :Properties:
     
        :pp:        np_array shape (n, 3)
        :x, y, z:   np_arrays of each ordinate set shape (n,)
        :xy:        np_arrays of (x, y) points (n, 2)
        :xyz:       same as pp

    .. versionadded:: 9.2
    """

    def __init__(self, xyz, z=0.0, **kwargs):

        super().__init__(**kwargs)

        def blankpp(length):
            self.pp = np.zeros(length * 3, dtype=np.float).reshape((length, 3))

        def np_setup(xyz):
            blankpp(xyz.shape[0])
            self.pp[:, 0] = xyz[:, 0]
            self.pp[:, 1] = xyz[:, 1]
            if xyz.shape[1] > 2:
                self.pp[:, 2] = xyz[:, 2]
            else:
                self.pp[:, 2] = z

        def vv_setup(xyz):
            blankpp(xyz[0].length)
            self.pp[:, 0] = xyz[0].get_data()[0][:]
            xyz[1].refid(xyz[0].fid, self.pp.shape[0])
            self.pp[:, 1] = xyz[1].get_data()[0][:]
            if len(xyz) > 2:
                xyz[2].refid(xyz[0].fid, self.pp.shape[0])
                self.pp[:, 2] = xyz[2].get_data()[0][:]
            else:
                self.pp[:, 2] = z

        def point_setup(xyz):
            blankpp(len(xyz))
            i = 0
            for p in xyz:
                self.pp[i, :] = p.xyz
                i += 1

        if isinstance(xyz, np.ndarray):
            np_setup(xyz)
        elif isinstance(xyz[0], gxvv.GXvv):
            vv_setup(xyz)
        elif isinstance(xyz[0], Point):
            point_setup(xyz)
        else:
            np_setup(np.array(xyz))

        self._next = 0

    @classmethod
    def from_list(cls, xyzlist, z=0.0):
        """
        .. deprecated:: 9.3 `PPoint` can create directly from a list
        """
        return cls(np.array(xyzlist, dtype=np.float), z)

    def __len__(self):
        return self.pp.shape[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self._next >= self.pp.shape[0]:
            self._next = 0
            raise StopIteration
        else:
            self._next += 1
            return Point(self.pp[self._next - 1])

    def __getitem__(self, item):
        return Point(self.pp[item])

    def __add__(self, p):
        if isinstance(p, PPoint):
            return PPoint(self.pp + p.pp)
        if isinstance(p, Point):
            return PPoint(self.pp + p.p)
        return PPoint(self.pp + Point(p).p)

    def __sub__(self, p):
        if isinstance(p, PPoint):
            return PPoint(self.pp - p.pp)
        if isinstance(p, Point):
            return PPoint(self.pp - p.p)
        return PPoint(self.pp - Point(p).p)

    def __neg__(self):
        return PPoint(self.pp * -1.0)

    def __mul__(self, p):
        if isinstance(p, PPoint):
            return PPoint(self.pp * p.pp)
        if isinstance(p, Point):
            return PPoint(self.pp * p.p)
        return PPoint(self.pp * Point(p).p)

    def __truediv__(self, p):
        if isinstance(p, PPoint):
            return PPoint(self.pp / p.pp)
        if isinstance(p, Point):
            return PPoint(self.pp / p.p)
        return PPoint(self.pp / Point(p).p)

    def __eq__(self, other):
        if not _same_cs(self, other):
            return False
        return np.array_equal(self.pp, other.pp)

    def copy(self):
        """return a copy as a :class:`PPoint` instance"""
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    @property
    def length(self):
        """number of points"""
        return self.__len__()

    @property
    def x(self):
        """ x array slice, can be set"""
        return self.pp[:,0]

    @x.setter
    def x(self, v):
        self.pp[:,0] = v

    @property
    def y(self):
        """ y array slice, can be set"""
        return self.pp[:,1]

    @y.setter
    def y(self, v):
        self.pp[:,1] = v

    @property
    def z(self):
        """ z array slice, can be set"""
        return self.pp[:,2]

    @z.setter
    def z(self, v):
        self.pp[:,2] = v

    @property
    def xy(self):
        """ (x, y) array slice, can be set"""
        return self.pp[:, 0:2]

    @xy.setter
    def xy(self, v):
        self.pp[:, 0:2] = v

    @property
    def xyz(self):
        """ xyz point array"""
        return self.pp

    def extent(self):
        """
        Volume extent as (`Point`, `Point`) for (min, max).

        .. versionadded:: 9.2
        """
        p1 = Point((np.amin(self.x), np.amin(self.y), np.amin(self.z)))
        p2 = Point((np.amax(self.x), np.amax(self.y), np.amax(self.z)))
        return p1, p2

    @property
    def extent_xyz(self):
        """
        Returns 3D extent as tuple (xmin, ymin, zmin, xmax, ymax, zmax)

        .. versionadded:: 9.3
        """
        p1, p2 = self.extent()
        return p1.x, p1.y, p1.z, p2.x, p2.y, p2.z

    @property
    def extent_xy(self):
        """
        Returns horizontal extent as tuple (xmin, ymin, xmax, ymax)

        .. versionadded:: 9.3
        """
        p1, p2 = self.extent()
        return p1.x, p1.y, p2.x, p2.y

    def make_xyz_vv(self):
        """
        Return x, y and z as a set of :class:`geosoft.gxpy.vv.GXvv`.
        
        :returns: (xvv, yvv, zvv)
        
        .. versionadded:: 9.2
        """

        return gxvv.GXvv(self.x), gxvv.GXvv(self.y), gxvv.GXvv(self.z)