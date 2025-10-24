# Week 9 Design Log
Explicit Statement: I am kinda stuck with the sim, it is tough...

## Questions: 

# Week Overview
- Had 565, but tried to get my Operand collector logic block going.

# Work:
- Simulator in Python: ![alt text](week_9_OC.png)
  - Spent my free time working on this. 
  - I am spending a lot of time looking at the structure of how GPGPU Sim is set up, and I think that might be hurting me. I am aware that we do not need that level of complexity, but I really am struggling to wrap my head around everything that we need to do. 
  - Another problem might be the fact that I am aware of all the details and complexity, and that is kind of giving me paralysis?
    - But I have been swamped with a lot of work recently in terms of preparing for the 565 exam and I have 570 exam coming up next week. 
  
- Issues
  - It is hard to patch together the logic of the code itself. Like I know my operand collector should receive inputs from the Register file, but there are parts of the Issue logic that is tied into this. OFC I can just spin up something that is all encompassing and get it to work, but it kind of defeats the purpose of the functional simulation as we want to make sure that when we implement in RTL, we don't run into any obstacles as opposed to "getting" a funcsim to work...


# Next Week:
- I understand that everyone needs to have their version of a sim working? Will clarify further with Jing. 
- I will try my best to make up for the missing work. I really want to drive this project forward and am aware that we are behind the planned schedule, so it might come down to thanksgiving break or something to make up for all this. 