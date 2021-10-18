from image import Image
from color import Color
from vector import Vector
from point import Point
from sphere import Sphere
from scene import Scene
from engine import RenderEngine
from light import Light
from material import Material
from material import CheckeredMaterial

WIDTH = 960
HEIGHT = 540
RENDERING_IMG = "twoballs.ppm"
CAMERA = Vector(0.0, -0.35, -1)
OBJECTS = [
    Sphere(Point(0.75, -0.1, 1), 0.6, Material(Color.fromHex("#0000FF"))),
    Sphere(Point(-0.75, -0.1, 2.25), 0.6, Material(Color.fromHex("#803980"))),
    Sphere(Point(0, 10000.5, 1), 10000, CheckeredMaterial(color1=Color.fromHex("#420500"),
                                                        color2=Color.fromHex("#E6E6E6"),
                                                        ambient=0.2,
                                                        reflection=0.2)
                                                        )
]
LIGHTS = [
    Light(Point(1.5,-0.5, -10.0), Color.fromHex("#FFFFFF")),
    Light(Point(-0.5,-10.5, 0.0), Color.fromHex("#E6E6E6"))
]