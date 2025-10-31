# Week 10 Design Log
Explicit Statement: I am kinda stuck with the sim, it is tough...

## Questions: 

# Week Overview
- Had 570, got a basic implementation of the Ibuffer going for the team to make some progress w/o me. But I am ready to put a good amt of time into it now. 

# Work:
- Thursday's discussion of finally clarify the interface with the team was very useful. 
- On Sunday, since I missed the prev. Thrusday meeting, I had to catch up a lot with the changes and approaches. 
- The idea is, have a large class that allows everyone to implement the logic that they will need, keep it simple. 
- Include bidrectional interfaces. So very similar to 437 and GEM5 in which we have an interface to pass foward and one to pass back. Since everything is run from end to start, the end stages will be able to, on the cycle, take the forward interface, work with it, and pass forward to next stage in NEXT cycle, and pass backward any feedback in the CURRENT cycle. 
- This really helps to clean things up as I was struggling to clear this direction earlier and it was the main bottleneck of my previous attempts. 
- Now, I wanna spend more time on implementing, so let's see how it goes!
  
  
- Issues
  - Honestly, its going to come down to a very fine balancing act. I have 573 in the following week, but that's not really a good reason. I guess it is the fall behind and catch up nature of all the work that everyone is going through, so no reason for me to fall behind on this. 
  - Will try to make up ground and push the project forward. 

# Next Week:
- Shifted the simulations per person done by Wednesday of next week. 
  