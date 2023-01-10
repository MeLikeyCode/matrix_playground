# Matrix Playground

Interactively play with/visualize matrices, vectors, points, transformations, etc.

Example
~~~~~~~python
v = Vector(4,0)
T = AffineT.rotation(45) * AffineT.scaling(2,2) * AffineT.translation(1,1)
v2 = T * v

v.label = 'v'
T.label = 'T'
v2.label = 'v2'

draw(v,T,v2)
~~~~~~~

See `quickreference.py` for cheatsheet of functionality.