# --------------------------------------------------------------------------
#
#    Copyright 2016 Jose Luis Cercos-Pita
#
#    This file is part of NASAL-GEOM.
#
#    NASAL-GEOM is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    NASAL-GEOM is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------

import os
import sys
import numpy as np
from scipy import stats
import trimesh
from OpenGL.GLU import *
from OpenGL.GL import *


tess_style = 0
coords = []
pids = []
triangles = []


def __outlines(mesh):
    """Get the outline paths of a mesh

    Parameters
    ----------
    mesh : trimesh.Trimesh
        Mesh to process

    Returns
    -------
    vertices : list
        List of sorted vertices (by connectivities) of each outline path
    bounds : list
        Bounds of each outline path
    centroids : list
        Centroid of each outline path
    """
    outline = mesh.outline()
    verts = outline.vertices
    paths = outline.paths
    centroids = []
    bounds = []
    vertices = []
    for p in paths:
        entities = outline.entities[p]
        points = []
        for i,e in enumerate(entities):
            ee = entities[(i + 1) % len(entities)]
            if e.points[0] not in ee.points:
                points.append(e.points[0])
            else:
                points.append(e.points[1])
        v = verts[points]
        centroids.append(np.sum(v, axis=0) / len(v))
        bds = []
        for i in range(3):
            bds.append(np.min(v[:,i]))
            bds.append(np.max(v[:,i]))
        bounds.append(bds)
        vertices.append(v)
    return vertices, bounds, centroids


def __cb_vert(v):
    global pids, coords
    if not isinstance(v, int):
        # Appended vertex, we should look for it in the known list
        vid = np.argmin(np.linalg.norm(np.asarray(coords) - v, axis=1))
        pids.append(vid)
        return
    pids.append(v)

        
def __cb_begin(style):
    global tess_style
    tess_style = style


def __cb_end():
    global tess_style, pids, triangles
    if tess_style == GL_TRIANGLE_FAN:
        c = pids.pop(0)
        p1 = pids.pop(0)
        while pids:
            p2 = pids.pop(0)
            triangles.append([c, p1, p2])
            p1 = p2
    elif tess_style == GL_TRIANGLE_STRIP:
        p1 = pids.pop(0)
        p2 = pids.pop(0)
        while pids:
            p3 = pids.pop(0)
            triangles.append([p1, p2, p3])
            p1 = p2
            p2 = p3
    elif tess_style == GL_TRIANGLES:
        while pids:
            p1 = pids.pop(0)
            p2 = pids.pop(0)
            p3 = pids.pop(0)
            triangles.append([p1, p2, p3])
    else:
        print("Tesselation error! Unknown tessellation style '{}'".format(
            tess_style))


def __cb_error(msg):
    print("Tesselation error! '{}'".format(msg))


def __cb_combine(c, v, weight):
    global pids, coords
    # pids.append(len(coords))
    coords.append((c[0], c[1], c[2]))
    return (c[0], c[1], c[2])


def __tess(contours):
    """Tesselate a polygon path

    Parameters
    ----------
    contours : list
        List of contours vertexes, sorted by connectivity

    Returns
    -------
    mesh : trimesh.Trimesh
        Tesselated polygon
    """
    global tess_style, pids, coords, triangles
    tess_style = 0
    pids = []
    coords = []
    triangles = []

    # Use GLU to mesh the polygon
    tess = gluNewTess()
    gluTessCallback(tess, GLU_TESS_VERTEX, __cb_vert)
    gluTessCallback(tess, GLU_TESS_BEGIN, __cb_begin)
    gluTessCallback(tess, GLU_TESS_END, __cb_end)
    gluTessCallback(tess, GLU_TESS_ERROR, __cb_error)
    gluTessCallback(tess, GLU_TESS_COMBINE, __cb_combine)

    pid = 0
    gluTessBeginPolygon(tess, None)
    for path in contours:
        gluTessBeginContour(tess)
        for p in path:
            gluTessVertex(tess, p, pid)
            coords.append(p)
            pid += 1
        gluTessEndContour(tess)
    gluTessEndPolygon(tess)

    if not len(coords) or not len(triangles):
        return None

    # Here degenerated triangles are accepted
    return trimesh.Trimesh(vertices=coords, faces=triangles, process=False)


def __fill_holes(mesh):
    """Generate outline paths of the holes, and patches to fill them

    Parameters
    ----------
    mesh : trimesh.Trimesh
        Mesh to process

    Returns
    -------
    patchs : [trimesh.Trimesh, ...]
        Patches to fill the holes
    """
    bds = mesh.bounds
    zmin, zmax = bds[0][2], bds[1][2]
    vertices, bounds, centroids = __outlines(mesh)
    patchs = []
    for i in range(len(vertices)):
        tess = __tess([vertices[i]])
        if tess is not None:
            patchs.append(tess)
    return patchs


def __patch_wall(folder):
    """Patch the nasal cavity (wall.stl)

    Parameters
    ----------
    folder : str
        Folder where the files wall.stl and bounds.dat are located
    """
    print('Patching wall.stl...')
    # Load the mesh
    mesh = trimesh.load_mesh(os.path.join(folder, 'wall.stl'))
    # Extract all the non-watertight meshes, and get the best candidate
    meshes = list(mesh.split(only_watertight=False))
    nonwatertight = []
    for m in meshes:
        if not m.is_watertight:
            nonwatertight.append(m)
    meshes = nonwatertight
    candidate = 0
    if len(meshes) > 1:
        for i in range(1, len(meshes)):
            if len(meshes[i].faces) > len(meshes[candidate].faces):
                candidate = i
    mesh = meshes[candidate]
    # Generate all the patches
    patchs = __fill_holes(mesh)
    # Get the theoretical bounds of the pharynx and nostrils
    bounds = {}
    f = open(os.path.join(folder, "bounds.dat"))
    lines = f.readlines()
    f.close()
    for i,bc in enumerate(('out', 'in_right', 'in_left')):
        if lines[i].strip() == 'None':
            # The boundary does not exists
            if bc == 'out':
                raise ValueError('A pharynx is required')
            print('WARNING: Empty boundary {}'.format(bc))
            # Create an empty STL file
            f = open(os.path.join(folder, '{}.stl'.format(bc)), 'w')
            f.write('solid Empty\n')
            f.write('endsolid Empty')
            f.close()
            continue
        data = np.asarray(list(map(float, lines[i].strip().split(' '))))
        bounds[bc] = data[3:]

    # First, extract the pharynx boundaries (it is based just on the z coords)
    zmin, zmax = bounds['out'][4], bounds['out'][5]
    out = None
    other = []
    for patch in patchs:
        z = patch.centroid[2]
        if not zmin <= z <= zmax:
            other.append(patch)
            continue
        out = patch if out is None else out + patch
    patchs = other
    out.export(file_obj=os.path.join(folder, 'out.stl'))
    # Now try to get the best candidates to become the nostrils
    for bc in ('in_right', 'in_left'):
        if bc not in bounds.keys():
            continue
        # Axial slice overlapping area factor
        bds = bounds[bc]
        vol1 = np.prod(np.abs(bds[1::2] - bds[0::2]))
        merits = []
        for patch in patchs:
            if not len(patch.vertices) or not len(patch.triangles):
                merits.append(0.0)
                continue
            b = patch.bounds.T.flatten()
            vol2 = np.prod(np.abs(b[1::2] - b[0::2]))
            # Common outline box volume
            c_min = np.maximum(bds[0::2], b[0::2])
            c_max = np.minimum(bds[1::2], b[1::2])
            c_vol = np.prod(np.maximum(c_max - c_min, (0, 0, 0)))
            # Patch merit
            merits.append(2 * c_vol / (vol1 + vol2))
        # Extract the most merited boundary
        patch = patchs[np.argmax(merits)]
        patch.export(file_obj=os.path.join(folder, '{}.stl'.format(bc)))
        # Drop current patch from the list of cavity patches
        patchs.remove(patch)

    # Patch the input surface
    for patch in patchs:
        mesh += patch
    mesh.process()
    mesh.export(file_obj=os.path.join(folder, 'wall.stl'))


def __patch_face(folder):
    """Patch the nasal cavity (wall.stl)

    Parameters
    ----------
    folder : str
        Folder where the files wall.stl and bounds.dat are located
    """
    print('Patching face.stl...')
    # Load the mesh
    mesh = trimesh.load_mesh(os.path.join(folder, 'face.stl'))
    # Extract all the non-watertight meshes, and get the best candidate
    meshes = list(mesh.split(only_watertight=False))
    nonwatertight = []
    for m in meshes:
        if not m.is_watertight:
            nonwatertight.append(m)
    meshes = nonwatertight
    candidate = 0
    if len(meshes) > 1:
        for i in range(1, len(meshes)):
            if len(meshes[i].faces) > len(meshes[candidate].faces):
                candidate = i
    mesh = meshes[candidate]
    # Generate all the patches
    patchs = __fill_holes(mesh)
    # Patch the input surface
    for patch in patchs:
        mesh += patch
    mesh.process()
    mesh.export(file_obj=os.path.join(folder, 'face.stl'))
    

def __improve_nostril(folder, bcname):
    """Remesh a nostril patch using a radial technique, extruding a bit each
    radius.

    Parameters
    ----------
    folder : str
        Folder where the STL file to remesh is located
    bcname : {'in_left', 'in_right'}
        Nostril to become remeshed
    """
    print('Improving {}.stl...'.format(bcname))
    fname = os.path.join(folder, '{}.stl'.format(bcname))
    try:
        mesh = trimesh.load_mesh(fname)
    except ValueError as e:
        # Mesh can't be loaded, probably because is empty:
        # https://github.com/mikedh/trimesh/issues/95
        return
    if not len(mesh.vertices) or not len(mesh.triangles):
        # That's the case when the queried nostril is blocked (i.e. not found)
        return
    vs, _, ct = __outlines(mesh)
    sub_patches = []
    I = 0
    if len(vs) > 1:
        # Get the best candidate
        I = np.argmax([len(vvs) for vvs in vs])
        # Convert to patches all other outlines
        for i in range(len(vs)):
            if i == I:
                continue
            tess = __tess([vs[i]])
            if tess is not None:
                sub_patches.append(tess)
    vs = vs[I]
    ct = ct[I]
    n_vs = len(vs)

    # Compute and averaged normal direction
    r = -(vs - ct)                        # Radial vectors
    r_norm = np.linalg.norm(r, axis=1)
    r_norm[r_norm < 1E-8] = 1.0
    r_norm = r_norm.reshape((-1, 1))
    t = vs - np.roll(vs, 1, axis=0)       # Tangential vectors
    t_norm = np.linalg.norm(t, axis=1)
    t_norm[t_norm < 1E-8] = 1.0
    t_norm = t_norm.reshape((-1, 1))
    n = np.cross(r / r_norm, t / t_norm)  # Normal vectors
    normal = np.mean(n, axis=0)
    normal /= np.linalg.norm(normal)
    # Check the normal direction
    if np.abs(normal[2]) > 1E-2:
        # It has a significant z normal component. Hence, we must assert it is
        # downward oriented
        if normal[2] > 0.0:
            normal = -normal
    else:
        # The nostril is a vetical plane, so we must must it is oriented
        # outwards in the y direction
        if normal[1] > 0.0:
            normal = -normal

    # Recursive scaling and mesh
    steps = 6
    normal_factor = 0.1 * np.max(mesh.extents)
    coords = vs
    triangles = None
    for i in range(1, steps + 1):
        # Get the scaled list of vertexes. We must take care in the center (last
        # step) to avoid precission errors
        if i != steps:
            new_vs = vs + r * i / steps
        else:
            new_vs = np.repeat(np.reshape(ct, (1, 3)), n_vs, axis=0)
        # Move them along the normal direction
        r_factor = np.sqrt(1.0 - (1.0 - float(i) / steps)**2)
        new_vs += r_factor * normal_factor * normal
        coords = np.concatenate((coords, new_vs), axis=0)
        # Triangles connectivities
        p1 = np.arange(n_vs) + (i - 1) * n_vs
        p2 = p1 + 1
        p2[-1] -= n_vs
        p3 = np.arange(n_vs) + i * n_vs
        p4 = p3 + 1
        p4[-1] -= n_vs
        t1 = np.array([p1, p2, p3]).T
        t2 = np.array([p2, p3, p4]).T
        if triangles is None:
            triangles = np.concatenate((t1, t2), axis=0)
        else:
            triangles = np.concatenate((triangles, t1, t2), axis=0)

    mesh = trimesh.Trimesh(vertices=coords, faces=triangles)
    mesh.process()
    for sub_patch in sub_patches:
        mesh += sub_patch
    mesh.export(file_obj=fname)


def fix(args):
    """Fix several problems that may eventually affects the surfaces, like
    non-connected surfaces (watertight or not), or holes.

    This tool is loading and eventually overwriting the surfaces wall.stl and
    face.stl. 

    Parameters
    ----------
    args : dict
        Program arguments
    """
    if args.patch_wall or args.patch_improve_nostrils:
        __patch_wall(args.output)
    if args.patch_improve_nostrils:
        for bc in ('in_left', 'in_right'):
            __improve_nostril(args.output, bc)
    if args.patch_face:
        __patch_face(args.output)
