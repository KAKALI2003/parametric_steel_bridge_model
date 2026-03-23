# Importing dependencies

from OCC.Core.gp import gp_Vec, gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Graphic3d import Graphic3d_NOM_STEEL, Graphic3d_NOM_PLASTIC

from geometry.draw_i_section import create_i_section
from geometry.draw_rectangular_prism import create_rectangular_prism


# ---------------- PARAMETERS ----------------

units = "mm"

span_length = 12000

n_girders = 3
girder_centroid_spacing = 3000

girder_section_d = 900
girder_section_bf = 300
girder_section_tf = 18
girder_section_tw = 10

deck_thickness = 200
deck_overhang = 500

parapet_height = 800
parapet_thickness = 200

kerb_height = 150
kerb_width = 300

deck_width = girder_centroid_spacing * (n_girders - 1) + 2 * deck_overhang


# ---------------- TRANSLATE ----------------

def translate(shape, x, y, z):

    tr = gp_Trsf()
    tr.SetTranslation(gp_Vec(x, y, z))

    return BRepBuilderAPI_Transform(shape, tr).Shape()


# ---------------- GIRDER ----------------

def create_girder():

    girder = create_i_section(
        span_length,
        girder_section_bf,
        girder_section_d,
        girder_section_tf,
        girder_section_tw
    )

    return girder


# ---------------- DECK ----------------

def create_deck():

    deck = create_rectangular_prism(
        deck_width,
        deck_thickness,
        span_length
    )

    deck = translate(
        deck,
        -deck_width / 2,
        girder_section_d - girder_section_tf,
        0
    )

    return deck


# ---------------- KERB ----------------

def create_kerb():

    kerb = create_rectangular_prism(
        kerb_width,
        kerb_height,
        span_length
    )

    return kerb


# ---------------- PARAPET ----------------

def create_parapet():

    parapet = create_rectangular_prism(
        parapet_thickness,
        parapet_height,
        span_length
    )

    return parapet


# ---------------- BUILD GIRDERS ----------------

def build_girders():

    girders = []

    total_width = girder_centroid_spacing * (n_girders - 1)
    start_x = -total_width / 2

    for i in range(n_girders):

        g = create_girder()

        g = translate(
            g,
            start_x + i * girder_centroid_spacing,
            0,
            0
        )

        girders.append(g)

    return girders


# ---------------- BUILD PARAPETS ----------------

def build_parapets():

    parts = []

    # left kerb
    k1 = create_kerb()
    k1 = translate(
        k1,
        -deck_width / 2,
        girder_section_d - girder_section_tf + deck_thickness,
        0
    )

    # right kerb
    k2 = create_kerb()
    k2 = translate(
        k2,
        deck_width / 2 - kerb_width,
        girder_section_d - girder_section_tf + deck_thickness,
        0
    )

    parts.append(k1)
    parts.append(k2)

    # parapets

    p1 = create_parapet()
    p1 = translate(
        p1,
        -deck_width / 2,
        girder_section_d - girder_section_tf + deck_thickness + kerb_height,
        0
    )

    p2 = create_parapet()
    p2 = translate(
        p2,
        deck_width / 2 - parapet_thickness,
        girder_section_d - girder_section_tf + deck_thickness + kerb_height,
        0
    )

    parts.append(p1)
    parts.append(p2)

    return parts


# ---------------- ASSEMBLE BRIDGE ----------------

def assemble_bridge():

    builder = BRep_Builder()

    compound = TopoDS_Compound()
    builder.MakeCompound(compound)

    for g in build_girders():
        builder.Add(compound, g)

    builder.Add(compound, create_deck())

    for p in build_parapets():
        builder.Add(compound, p)

    return compound


# ---------------- EXPORT STEP ----------------

def export_step(shape):

    writer = STEPControl_Writer()

    writer.Transfer(shape, STEPControl_AsIs)

    writer.Write("output/bridge.step")

    print("STEP file exported: output/bridge.step")


# ---------------- DISPLAY ----------------

def display_bridge():

    display, start_display, _, _ = init_display()

    display.View.SetBgGradientColors(
        Quantity_Color(1, 1, 1, Quantity_TOC_RGB),
        Quantity_Color(0.85, 0.9, 1, Quantity_TOC_RGB),
        2,
        True
    )

    display.SetModeShaded()
    display.Context.SetDeviationCoefficient(0.0001)
    display.Context.SetDeviationAngle(0.1)

    steel = Quantity_Color(0.28, 0.28, 0.30, Quantity_TOC_RGB)
    concrete = Quantity_Color(0.45, 0.45, 0.47, Quantity_TOC_RGB)
    kerb_col = Quantity_Color(0.60, 0.60, 0.60, Quantity_TOC_RGB)
    parapet_col = Quantity_Color(0.65, 0.67, 0.70, Quantity_TOC_RGB)

    for g in build_girders():
        display.DisplayShape(g, color=steel, material=Graphic3d_NOM_STEEL, update=False)

    display.DisplayShape(create_deck(), color=concrete, material=Graphic3d_NOM_PLASTIC, update=False)

    parts = build_parapets()

    for i, p in enumerate(parts):

        if i < 2:
            # kerb
            display.DisplayShape(
                p,
                color=kerb_col,
                material=Graphic3d_NOM_PLASTIC,
                update=False
            )

        else:
            # parapet
            display.DisplayShape(
                p,
                color=parapet_col,
                material=Graphic3d_NOM_PLASTIC,
                transparency=0.0,
                update=False
            )
    display.View_Iso()
    display.View.SetUp(0, 1, 0)
    display.FitAll()

    start_display()


# ---------------- MAIN ----------------

if __name__ == "__main__":

    bridge = assemble_bridge()

    export_step(bridge)

    display_bridge()