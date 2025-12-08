# Explicit Statement: I am not stuck

**Progress:**

* Code in progress for scheduler  
  * Design and test on repeat  
  * Will update with screenshots of commits or local code progress as soon as substantial progress is made  
    * **10/29: check git commits on fall2025 branch – all updates there**

**Important Notes:**

* Look at Hassan’s commit on the “working heuristic” branch from Feb 23 “all added functions and structures compiling”  
  * Contains important additions to the shader.cc and shader.h files  
* **Talked with Hassan and the best way to test this would be the following:**  
  * Add assertions or prints that show the pc for any thread in a warp that is supposed to be on the scalar core  
    * Intended functionality is that once the scalar core register is set, that thread is virtually “gone” from the SIMT core  
      * In reality, there will be some delay in sending the thread context from the SIMT to the scalar core, but from the SIMT core’s perspective the thread is gone  
      * **If done correctly, any thread that is meant to be on the scalar core should have its pc set to its rpc immediately after scalar reg is set**  
* Hassan said that one thing I need to add in shader.cc is the warp mask update  
  * So far, we set the result mask, which is equal to (\~scalar\_mask & warp\_mask)  
  * Now we need to set warp\_mask to result\_mask  
    * Hassan didn’t do this before because this would cause the warp to not issue the thread whose bit in the warp\_mask was turned off  
    * This implies that the scalar core will do work and return the correct values to the SIMT core once it is finished executing  
    * Since the scalar core is incomplete, we would face stalls and other BS problems that we don’t need to handle when just finishing a single component (modularization and abstraction is key)  
* **Scalar core** instantiation found in **“working heuristic”** branch, commit **“Merged with scalar core. Added scheduler logic”**


**Future Plans:**

* Continue working on scheduler code, have it done by next week