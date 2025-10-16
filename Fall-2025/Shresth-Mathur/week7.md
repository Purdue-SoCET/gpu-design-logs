# Explicit Statement: I am not stuck

**Progress:**

* In our gpgu-sim\_distribution repo, cloned the “working\_heuristic” branch  
  * Command:   
    * git clone \-b working\_heuristic –single-branch git@github.com:Purdue-SoCET/gpgpu-sim\_distribution.git
* Akshath and Zohaib need to install CUDA (running into some problems)
    * Look at Daniel Choi's early GPU team design logs from Spring 2025 to learn how to do this
    * Single design log contians all of the necessary info (step-by-step commands to install it)
* This branch contains correct and incorrect code:  
  * Heuristic works  
  * Top-level round robin scheduling scheme works  
  * Arch. specific warp scheduling scheme does NOT work  
    * Need to implement the scheduling policies described in Week 5 design log  
* **Plan for modifying scheduler:**  
  * Need to know all required signals:  
    * **scalar\_mask**  
      * Needed to know which threads are running on scalar mask because I need to set those corresponding threads’ lanes in the SIMT core to the RPC and stall them  
    * **warp\_id**  
      * Needed to know which warp’s lanes to stall if some of its threads are running on scalar core  
    * **thread\_id**  
      * Needed to know which lanes in a warp to stall if their corresponding threads are running on scalar core  
    * **pc**  
      * Needed to know when to reschedule the warp to run (pc \== rpc)  
    * **rpc**  
      * Needed to know when to reschedule the warp to run (pc \== rpc)

**Steps that I am going to take to test/debug my scheduler as I work on it:**

* Compile BFS (or some CUDA workload from Rodinia) and run it on the base GPGPUsim  
* Store the output execution trace somewhere safe  
  * This will be the benchmark with which we will compare every new output execution trace file (from changing the scheduler) to in order to see what changed in the execution  
    * diff \<og\_bfs.txt\> \<new\_bfs.txt\>  
* Learning and understanding the execution trace of a single CUDA program should be good enough because the more I analyze its trace the more I will understand how the workload should function/perform  
  * Use different CUDA programs to test the scheduler only AFTER getting one workload to work correctly  
  * Otherwise it will take too long to understand and profile the workload if we use a new one each time


**Future Plans:**

* I tasked Akshath and Zohaib to work on the register transfer mechanism  
  * This is a hard task so I don’t expect them to finish the code by themselves  
  * I plan on finishing the scheduler and then helping Akshath and Zohaib with the register transfer  
    * OR I can start working on the scalar core  
      * Already work done on that but not fully working  
        * Loads are causing some sort of error (seg fault or something? Ask Hassan)
