import sys
import os
import glob
import argparse
import trimesh
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.transform import Rotation as R
from tqdm.auto import tqdm


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, type=str, help='path to .obj')
    parser.add_argument('--odir', '-o', required=True, type=str, help='path to output directory')
    parser.add_argument('--frac', '-f', type=float, default=.2, help='fraction of original surface area')
    parser.add_argument('--verbose', action='store_true', help='print something')
    args = parser.parse_args()

    scene = trimesh.load(args.input, verbose=0)
    leaves = scene.geometry[list(scene.geometry_identifiers.values())[0]]
    wood = scene.geometry[list(scene.geometry_identifiers.values())[1]]
   
    x = np.random.choice(np.arange(0, len(leaves.faces))[::2], 
                         size=int((len(leaves.faces) / 2) * args.frac))
    x = np.hstack([x, x+1])
    leaves.update_faces(x)
 
    scene2 = trimesh.Scene()
    scene2.add_geometry(leaves, geom_name='Leaves')
    scene2.add_geometry(wood, geom_name='TrunksAndBranches')
    
    XXX = trimesh.exchange.export.export_mesh(scene2, os.path.join(args.odir, os.path.split(args.input)[1]))
