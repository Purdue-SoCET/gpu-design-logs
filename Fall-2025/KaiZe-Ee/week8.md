# Week 7 Design Log
Explicit Statement: I am not stuck or blocked

## Questions: 

# Week Overview
- This week included FALL break, so a good amount of time of the week is missing. 
- I mainly focused on trying to get my simulator to work, but after the meeting on Thursday, I realize that I should be working in the reverse direction. 

# Work:
- Simulator in Python: ![alt text](images/week7_GPUsim.png)
  - Spent most of my time working on this. 
  - This print occured because I was just invoking the inital CSR and doorbell fill
  - But when I tried to call the the functional blocks, like ibuffer or others, it just didn't work
    - Was pretty stubborn on trying to get it to work to no avail. 
    - So during our Thursday discussion, I think I neeed to start small first and just get one FU working then go from there. 

  
- Issues
  - I realize that in this FU, we will need the emulator team's implementation as well as it will just be easier to take assembly and work on it. Also there needs to be some representation of "memory" which is quite complicated. Will we even be able to get this done?


Functional Unit Class
- Method
  - Cycle
- Members
  - Number of stages
  - Queue (to hold ins)
- 200 cycle latency for DRAM sim
- 500 MHz


# Next Week:
- Try to get a single FU done, and work on the issues that I thoguht of, rather get the questions answered. 
- I do have 565 exam though, so I might be a bit cooked. 