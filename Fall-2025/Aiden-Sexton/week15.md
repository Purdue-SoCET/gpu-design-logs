State: I am not stuck with anything

# Progress

## Work Completed:
* Worked on converting microC kernels to be twig compatable

## Progress

### Converting kernels
* Took existing work from Aidan and his conversion of the pixel kernel and adapted it to no longer directly have IFDEFs for CPU vs GPU
* Adapted the existing universal kernel.h to provide the needed externed functions to work with the twig compiler
* To ensure more direct compatability with the kernels, the CPU only section of the header was updated to recreate all the GPU hardware functions with macros, allowing continued development on the CPU while moving towards GPU compilation
* Currently suppported shared functions
  * **float** cos(**float**)
  * **float** sin(**float**)
  * **int** ftoi(**float**)
  * **float** itof(**int**)
  * **float** isqrt(**float**)

### Updating to a single dimension
* The original existing kernels were built around the original assumptions of hardware supporting 3 dimensions
  * Changes with the hardware teams architecture meant that hardware will now only support one dimension
* My original understanding of the change was that while the kernels themselves would only get one dimension, the kernel would still be launched with 3 dimensions
  * This is not the case as i assumed, instead hardware is fully one-dimensions
* To accomidate for this, both the pixel and triangle kernel which used two-dimensions for going across a screen, were adapted to now use one dimensions
* To convert these, basic math involving division and modulus were used.
  * Note: For now, no existing modulus exists, so this is forced to be done with integer division and multiplicaiton. While inefficent, this only happens once/twice a program, so likely not a notable concern for now
* To accomidate for not getting three dimensions in the hardware, the software must pass in what used to be the 3D grid dimensions as an argument in memory
  * This will create an extra load from memory, but shouldn't matter given that the cache block containing the arguments will likely need to be loaded from memory later

### Compiler restrictions
* The current twig compiler, as provided by the team, only supports one egg (C) file
  * To support multiple files, I made a manual addition to the twig compilers "main" and got it working, but many aspects of the compiler had issues with using other files functions
  * Moving forward, kernels must be integrate to one file, with helper functions being duplicated across the relavent kernels
* Currently limited without access to certian boolean instructions.
  * !, ||, and && are all not currently available
  * Can be replaced with the equivalent bitwise instruction, carefully
