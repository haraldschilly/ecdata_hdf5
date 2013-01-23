# -*- coding: utf8 -*-

from tables import IsDescription, UInt32Col, Int32Col, UInt8Col, StringCol, Int64Col

class EC_Curve_1(IsDescription):
    conductor = UInt32Col()
    isogeny   = StringCol(3)
    nb        = UInt8Col()
    rank      = UInt8Col()
    torsion   = UInt8Col()

    class coefficient(IsDescription):
        a1 = Int64Col()
        a2 = Int64Col()
        a3 = Int64Col()
        a4 = Int64Col()
        a6 = Int64Col()


