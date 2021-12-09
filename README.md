# multishotSR
Algorithm to significantly boost pixel count and image resolution

This code combines 16 images, each shifted by half pixel, to generate a final image with 4x the resolution

The only format it reads right now is pure RAW (no metadata). Specific vendor formats can be added by using rawpy instead of np.fromfile for reading in RAW data

The input images should be numbered from 0.raw to 15.raw. Additional characters can be added before the numbers, but they must be the same across all 16 shots.

Helper code include implementations for getting better result by combining 1/3 pixel (36 total shots) and 1/4 pixel (64 total shots) shifted images 
