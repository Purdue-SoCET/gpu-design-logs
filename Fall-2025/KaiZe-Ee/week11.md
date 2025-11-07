# Week 11 Design Log
Explicit Statement: I am not blocked for no

## Questions: 

# Week Overview
- Made good process rearchitecting the the main classes with Zach. On Sunday, we identified that we needed to capture the funcitonal simulation we needed the interface, stage and instruction classes. 

# Work:
- Defined what was needed in the instruction class, specific starter fields and basic functions to look into the function. However, later on development of the interfaces solves this, as we are just able to keep the stage arguments as is and make a bunch of interfaces to pass bettween stages if needed. 
- The stage object will contain a compute method and allow a derived object to add any method it wants. 
  - The high level idea is that each person should be able to simply port and at worst adapt their logic to a stage. Then we have large loop that will act as the subcore and run all the stages in a backwards manner. 
- Another key point is that since we are deriving a specific instruciton object to be passed through the entire pipeline, we will have each stage fill in the necessary members of the object. Further the object will be able to have performance trackers/counters to let us test different parts of our design. 
  

- Define the Issue Stage itself. I set up the order of what need to happen within the issue stage. Specifcally, first check if the later stage is ready, then cehck the validity of the previous stage before doing any operation of the stage. 
  
- Issues
  - The operand collector need to be paramaterized, in terms of depth. I initially thought that it can easily be expanded by holding the number of entries in the buffer, but will need to look at exactly how that occurs. Because I don't really get the idea behind the depth increase, as all the operand collector feels like is not like a tomasoulo's value tracking. Regardless, 100% agree with the need to keep things parameterized, but I guess it needs to have a certain limit that makes sense with the earlier scheduling policies
  - Really really need to sort out the CSR stuff so that the other teams will be able to do thier things. 
    - I have spent a lot of time trying to get what we want to do there without good progress. Hopefully we can straighten this out once and for all during our meeting on Sunday!
  

# Next Week:
- Get the issue stage 80% --> 100%, then give it test inputs as if the decoded stage has filled in all the right fields. Finally make sure the output being sent to the register file is as expected.
- Clear up the CSR issue so that other people can make progress, and so that I personally can move on from this...