State: I am not stuck with anything

# Progress

## Work Completed:
Presentation heavy week
* Code review
* Undergraduate research Expo
* Team Leads Design Review
* Created basic timeline & goals for rest of semester

## Progress

### Code Review
* Slides were a mixture of our previous design review with added ASM notes
* Spent majority of time walking through code -> went long
* Feedback
  * did well on actual design and code
  * Need to get SAXPY Working on the emulator
  * Kernel launch for pixels assuming infinite threads is a problem that should be looked at further
  * Unbalanced speaking time

### Undergraduate Research Expo
* first judge was interested and knew the topic. Second didn't but we got the basic accross

### Team Leads Design Review
* Grade still pending
* Initial feedback and questions was minimal
  * Questions were small clarifications, nothing critical
  * Basic feedback of a need to know the content better and not read of the slides -> Something to improve on for next year

### Basic timeline and goals for rest of 1st semester
* Final Report
  * Get a draft to Sooraj by 11/28 to get feedback
  * Still not started. Team needs to start planning a general stucture
* Converting Kernels for the compiler
  * Initial conversion by this Sunday
  * Shouldn't be to bad, hardest part will be keeping kernels compiling on CPU_SIM while converting to compile on twig
  * Currently **blocked**: Need feedback from hardware and compilers on how we are handling threadblock dimensions
    * My understanding was that we were to only be given a linear threadID, but we would still pass in 3D block dimensions, which would be available via CSRs
    * Currently Compiler only supports passing in a single dimension for the block size
    * This could be worked around, but want to clarify with hardware before making these changes
* Code optimization
  * Once kernels are converted to compile with twig, we should go though and optimize the code to reduce extra computation
  * Can't be done until compiling with twig
    * ASM files will help with viewing any potentail optimizaiton areas
* Emulator Main
  * This is our "final product"
  * Should be done by coming back from break
    * Gives time for hardware to fix any possible emulator issues
  * Will use the hardware team's emulator (and func sim in the future) to stitch together our compiled kernels
  * Ideally, will generate identical output to that of the CPU_SIM. A nice cube
  * Can be started as soon as kernels are compiling on twig
    * Can't be finished until optimiziations done, as slow code may make "emulator main" take to long for practical testing