# Week 6
**State:** Currently not stuck, but will probably have many questions once I start on the simualtor

**Progress:**
- Sunday:
    - Presented our design review presentation to the other sub-teams
    - The graphics argued that they didn't need a t$ the main reason being that the texture filtering shouldn't be a priority for rendering a cube. The resolution for the cube doesn't need to be extremely high and their main goal should be making it functional first. As pointed out by Jing,  without a t$, the d$ might have an overwhelming amoutn of requests making it the bottleneck. Perhaps just have a t$ without the texture filtering. In that way, the t$ will be exactly like a d$, but with varying size depending on the workload
    - Talked a bit with Andrew who is responsible for hte load/store unit about the interfacing between the unit and dcache. We discussed about coalescing and whether or not we planned to do that. For the d$, I assumed that the requests would be coalesced to reduce the number of memory requests that are accesing different blocks in a set to one memory requests. The coalesing is now placed in the LD/ST unit. Additionally, in my original d$, I had the cache sent a write request to the writeback buffer. I didn't take into account that the data needs to be de-coalesced so that when the data is returned, it knows which warps requested that data. Therefore, the data needs to be sent to the LD/ST to be de-coalesced

- We were told on Discord by Sooraj to wait until Thursday or Friday as he would explain the general structure of the simulator

- Wednesday:
    - Did the midterm report, the project proposal, and the CATME survey

Thursday Meeting:
- Parent class (each functional unit) has cycle method
    - There's a queue and in the cycle method, it moves all the data forward in the queue, moves the data to the next state of the pipeline
    - We need to know how which stage the instruction will be at the nex cycle (cycle-accurate)
    - We need to execute the deepest stage of the pipeline first (WB -> Mem -> Exec -> Decode -> Fetch). This prevents fetching/decoding stages to be overwritten. 
    - dRAM transaction is 200 cycles (static latency). Don't need to hook up with teh actual dRAM for simulator
    - Target frequency: 500 Mhz on 90nm
    - I think we'll each make a list of I/O ports for the modules we're responsible for making it easier for other team members to know what data they need to pass

**I/O output ports:**
1. L1 d$:
- Inputs:
    - **warpID** (when a memory requests miss, I need to return the warpID with the miss so that the LD/ST unit knows which warp the missed request comes from)
    - **threadID** (Same reason as above, need to know which thread issues the memory request)
    - **Memory address** (The address that we want to fetch data from. The memory address will be used to index into the cache banks)
    - **L/S Mode** (Need to know whether to fetch data from cache or write data to cache)
    - **Store value** (If writing to cache, the data to be written)
- Outputs:
    - **Hit** (If the data is found in the L1 d$)
    - **Miss** (If the data is missing in the L1 d$)
    - **threadID** (Accompaies the hit or miss signal so that teh LD/ST unit knows which requests hit or missed)
    - **warpID** (Same as above)
    - **Replay** (From the MSHR buffer. Once a missed request's data has been written back to teh d$, this signal will be sent to the LD/ST unit to tell it to replay the request)
    - **replay_address** (From the MSHR buffer. Accompanies the replay signal and tells the LD/ST unit to replay the request for the data at this address)
    - **load_values** (This is the data from the load_address returned back to the LD/ST unit)
    - **load_address** (This is the address in which the load_values are from)
    - **miss address** (This is sent from the MSHR buffer to the bank dispatcher which calculates the bank and set of the address in the L2 d$)

2. L2 d$: 
- Inputs:
    - **Memory address** (The address that we want to fetch data from. The memory address will be used to index into the cache banks)
    - **L/S Mode** (Need to know whether to fetch data from cache or write data to cache)
    - **victim address** (The address of the data that has been kicked out to from the l1 cache)
- Outputs:
    - **Hit + hit address** (If the data is found in the L2 d$)
    - **Miss + miss address** (If the data is missing in the L2 d$)
    - **Replay** (From the MSHR buffer. Once a missed request's data has been written back to the d$, this signal will be sent to the LD/ST unit to out-of-order)
    - **replay_address** (From the MSHR buffer. Accompanies the replay signal and tells the bus to replay the request for the data at this address)
    - **load_values** (This is the data from the load_address returned back to the fill unit)
    - **load_address** (This is the address in which the load_values are from)
    - **Miss address** (This will be sent to the main memory)

3. T$:
- Inputs:
    - **warpID** (when a memory requests miss, I need to return the warpID with the miss so that the LD/ST unit knows which warp the missed request comes from)
    - **threadID** (Same reason as above, need to know which thread issues the memory request)
    - **Memory address** (The address that we want to fetch data from. The memory address will be used to index into the cache banks)
- Outputs:
    - **Hit** (If the data is found in the t$)
    - **Miss** (If the data is missing in the L1 t$)
    - **threadID** (Accompaies the hit or miss signal so that teh LD/ST unit knows which requests hit or missed)
    - **warpID** (Same as above)
    - **Replay** (From the MSHR buffer. Once a missed request's data has been written back to teh d$, this signal will be sent to the LD/ST unit to tell it to replay the request)
    - **replay_address** (From the MSHR buffer. Accompanies the replay signal and tells the LD/ST unit to replay the request for the data at this address)
    - **load_values** (This is the data from the load_address returned back to the LD/ST unit)
    - **load_address** (This is the address in which the load_values are from)
    - **miss address** (This is sent from the MSHR buffer to the bank dispatcher which calculates the bank and set of the address in the L2 d$)