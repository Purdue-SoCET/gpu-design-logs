# Explicit Statement: I am not stuck

Progress:

- I have an idea of how the scheduler is going to look as well as some template code for it, but I first wanted to re-integrate the heuristic code that Hassan had working from last semester back into our design, but in a more modular way  
  - I created a v3\_top.cc file in which I define all the functions that the heuristic will need (so maybe I’ll call it v3\_heuristic.cc later)  
  - The declarations are all in shader[.](http://shader.hh)h  
- Questions (for Hassan):  
  - In many of the commits you played around with the .config files (in the test directory)  
    - Is this important?  
    - Should we replicate when we are testing?  
- Questions (in general):  
  - Need to figure out how to make the Makefile properly compile everything in the v3\_arch subfolder in gpgpu-sim directory  
  - Currently I made it work by simply moving the v3\_top.cc file (holds function definitions for all of the v3 structures required)


Todo:

- Verify heuristic functionality using scalar que display function  
- Once heuristic works, integrate scalar core and get that working  
- Look at first page under “important notes” that is what to work on next