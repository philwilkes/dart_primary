import sys
import os
import glob
import argparse
import trimesh
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from scipy.spatial.transform import Rotation as R
from tqdm.auto import tqdm


def in_hull(p, hull):
    """
    Test if points in `p` are in `hull`

    `p` should be a `NxK` coordinates of `N` points in `K` dimensions
    `hull` is either a scipy.spatial.Delaunay object or the `MxK` array of the
    coordinates of `M` points in `K`dimensions for which Delaunay triangulation
    will be computed
    """
    from scipy.spatial import Delaunay
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0

def generate_twig(xyz):
   
    M = np.identity(4)
    M[:3, :3] = R.from_rotvec(np.random.uniform(0, 90, size=3)).as_matrix()
    M[:3, 3] = xyz

    radius = np.random.uniform(.005, .01)
    height = np.random.uniform(.1, .5)
    volume = height * (np.pi * radius**2)
    surface_area = 2 * np.pi * radius * height

    cyl = trimesh.creation.cylinder(radius=radius,
                                    height=height,
                                    transform=M)
                                   
    return cyl, surface_area, volume

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, type=str, help='path to .obj')
    parser.add_argument('--odir', '-o', required=True, type=str, help='path to output directory')
    parser.add_argument('--frac', '-f', type=float, default=.2, help='fraction of original surface area')
    parser.add_argument('--verbose', action='store_true', help='print something')
    args = parser.parse_args()

    volume = 0

    scene = trimesh.load(args.input, verbose=0)
    leaves = scene.geometry[list(scene.geometry_identifiers.values())[0]]
    wood = scene.geometry[list(scene.geometry_identifiers.values())[1]]
    
    v = leaves.vertices
    v = v[v[:, 1] > v[:, 1].max() / 2]
    hull = Delaunay(v)
    X = np.random.uniform(v[:, 0].min(), v[:, 0].max(), size=(1, 1000000))
    Y = np.random.uniform(v[:, 1].min(), v[:, 1].max(), size=(1, 1000000))
    Z = np.random.uniform(v[:, 2].min(), v[:, 2].max(), size=(1, 1000000))
    XYZ = np.hstack([X.T, Y.T, Z.T])
    XYZ = XYZ[in_hull(XYZ, hull)]

    wsa = wood.area_faces.sum()
    cyl, SA, V = generate_twig(XYZ[0, :])

    with tqdm(total=100, disable=False if args.verbose else True) as pbar:

        for i, row in enumerate(XYZ[1:, :]):
            twig, sa, v = generate_twig(row)
            SA += sa
            V += v
            cyl = trimesh.util.concatenate(cyl, twig)
            pbar.n = int((SA / (wsa * args.frac)) * 100)
            pbar.refresh() 
            if SA > wsa * args.frac: break

    wood = trimesh.util.concatenate(wood, cyl)
   
    scene2 = trimesh.Scene()
    scene2.add_geometry(leaves, geom_name='Leaves')
    scene2.add_geometry(wood, geom_name='TrunksAndBranches')
    
    with open(os.path.join(args.odir, os.path.split(args.input)[1].replace('.obj', '.dat')), 'w') as fh:
        fh.write(f'{i} {SA} {V}')

    XXX = trimesh.exchange.export.export_mesh(scene2, os.path.join(args.odir, os.path.split(args.input)[1]))
