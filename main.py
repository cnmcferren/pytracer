#!/usr/local/bin/pypy3

import argparse
import importlib

from engine import RenderEngine
from scene import Scene

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('-s', '--scene', type=str, required=True)
    parser.add_argument('-p', '--processes', action='store', type=int, dest="processes", default=0)
    args = parser.parse_args()

    processes = 1
    if args.processes > 0:
        processes = args.processes

    mod = importlib.import_module(args.scene)

    scene = Scene(mod.CAMERA, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()

    with open(args.output, 'w') as imgFile:
        engine.renderMultiprocess(scene, processes, imgFile)

if __name__=='__main__':
    main()