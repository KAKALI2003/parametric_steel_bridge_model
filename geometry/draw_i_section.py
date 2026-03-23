# Importing dependencies

from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform


def translate(shape, x, y, z):
    tr = gp_Trsf()
    tr.SetTranslation(gp_Vec(x, y, z))
    return BRepBuilderAPI_Transform(shape, tr, True).Shape()


def create_i_section(length, bf, d, tf, tw):
    """
    I section axes:
    X = flange width
    Y = height
    Z = span length
    """

    # bottom flange
    bottom = BRepPrimAPI_MakeBox(bf, tf, length).Shape()

    # top flange
    top = BRepPrimAPI_MakeBox(bf, tf, length).Shape()
    top = translate(top, 0, d - tf, 0)

    # web
    web_height = d - 2 * tf
    web = BRepPrimAPI_MakeBox(tw, web_height, length).Shape()
    web = translate(web, (bf - tw) / 2, tf, 0)

    # fuse parts
    shape = BRepAlgoAPI_Fuse(bottom, top).Shape()
    shape = BRepAlgoAPI_Fuse(shape, web).Shape()

    return shape