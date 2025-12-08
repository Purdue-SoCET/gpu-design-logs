# Explicit Statement: I am not stuck

Currently:

- We decided to scrap most of the previous work because its too jumbled up and hard to understand  
  - Plus at least half of the code is wrong  
- So now we are going to work on a single branch and take a different approach in coding  
  - Each component of the design will be made in a separate file  
  - We will call the top level class “v3” and instantiate our implementation in shader.cc using the v3 class  
    - This will make our design simpler and much easier to understand  
- This is the current split:  
  - I will work on scheduler code (warp scheduler (modifying it based on the two things we still need to add from week 6\)  
  - Akshath will do scalar core instantiation and template for thread transfer mechanism  
- **Debugging:**  
  - Copied over all the heuristic stuff (minus the scalar core logic)  
  - Running into **seg fault** when running program, not much info to go off of  
  - Debugging this by running mmul with baseline gpgpusim and using its execution trace as baseline comparison  
  - Commented out all new lines in shader.cc and reinserting each one by one to see which one breaks it (causes seg fault)  
    - Found faulting function: **check\_sat\_counters()**  
  - **Resolved:**  
    - Some arrays weren’t initialized to any value (I was accessing a NULL ptr)  
    - Simply initialized all arrays to 0s and problem was solved