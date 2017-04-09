# g4d

This project's goal was to render 3D cross-sections of 4D geometry. There is code for the GPU-based pipeline, 
in addition to tools to generate 4D meshes and volume textures. No further development is planned for now. 

See [the demo](//github.com/tocubed/g4d-demo) which uses this code.

## Building
When cloning, there are several submodules in `deps/` that must also be cloned. After that, 
a simple `cmake /path/to/g4d && make` from within a temporary build folder will suffice. 

The code in this repository and [the demo](//github.com/tocubed/g4d-demo) is best used as a reference, 
as the design is still incomplete and many challenges in 4D rendering remain to be solved.
