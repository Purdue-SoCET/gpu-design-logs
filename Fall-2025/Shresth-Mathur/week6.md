# Explicit Statement: I am not stuck

**Progress:**

* **Met with Akshath and Hassan to onboard Akshath and explain project overview \+ goals**  
* Akshath will work with me or with Zohaib to either work on a component that I am not working on or help me with the component I’m currently working on  
* Explained that this project will require lots of knowledge on GPU microarchitecture and C++ for GPGPUsim  
* Answered all of Akshath’s questions and agreed to meet on Saturday to look through GPGPUsim to try and understand it  
* Currently, we are going to focus on the scheduler and try to make as much progress on it as possible by the **Design Review on Sunday**  
  * **Scheduler modifications to be made** (according to Hassan, may not be holistic):  
    * 1\. If there are threads on the SIMT core that were issued to be run on the scalar core, simply set those threads’ PCs (that are on the SIMT core) to be equal to their reconvergence PC (RPC) and wait for the threads sent to the scalar core to be returned to the SIMT core and only then resume execution  
      * This is important because we don’t want to schedule the same threads that are running on the scalar core to also run on the SIMT core (defeats the whole purpose of our design)  
    * 2\. If there are threads actively running on the scalar core with the same RPC as threads running on the SIMT core, do not schedule threads that reach the RPC to continue execution past the RPC until the scalar core execution mask turns to all 0s (threads running on scalar core are transferred back to the SIMT core)  
      * This is important because we only allow one warp’s threads to run at different PCs when they are NOT on the same core (some threads on SIMT core others on scalar core), other than that they need to move in lockstep  
* **How will I debug/test the scheduler?**  
  * Hassan’s way of debugging/testing was simply compiling different CUDA programs and running them on their modified GPGPUsim and analyzing the traces to see if the execution is working as it should  
    * Brute force, will be difficult, will try to find better ways to do this in the future but currently it is what it is  
* Currently, I am looking through src/gpgpu-sim/shader.cc since that is where the scheduler functions are located  
  * 5000 line file, will take a while to understand  
* I am currently looking through Khoi’s commits from last semester since he did make some progress on the scheduler but was never able to finish  
  * Hassan suggested scrapping all his work and starting fresh since he was running into segfaults and other errors that would not be fun to work with, especially since I’ll first have to understand all his current modifications


**Future Plans:**

* Need to meet with Akshath this Saturday and try to understand the shader.cc file  
  * Will look through Khoi’s commits to understand what direction he was going with the code and possibly try to diagnose incorrect implementation  
  * Will use ChatGPT’s help understanding the code  
* **Aiming to finish the scheduler modifications in 3 weeks (end of October)**

