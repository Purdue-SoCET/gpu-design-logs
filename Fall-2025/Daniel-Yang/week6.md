Status: My brain is fried but I feel like everyone is making good progress and im understanding more than just my specific component of the arch now, I’m starting to get a broader view of everything

Progress: Good progress, started working on the senior design presentation and need to finish up micro-arch/rtl ideas

So this week was kinda nuts I feel like I got so much information in the span of like a day today.

We’ve started working on our top level block diagram and the senior design review presentation ad I’ve started putting together the microarch for the warp scheduler

--IF THE THREAD BLOCK HAS TOO MANY THREADS (1024) WE TELL THE PROGRAMMER TO FUCK OFF SINCE WE CANNOT EXECUTE BLOCKS IN DIFFERENT CHUNKS DUE TO BARRIERS (think about the actual software graphics pipeline, I cant draw triangles until I have my dots etc.)

BIG ISSUE: the HARDWARE is the one who groups the warps, not the compiler, not the software. Basically the only information I’m getting is threadidx, blockidx, blockdim, and gridDim.

Threadidx is the index (xyz) of a specific thread

Blockidx (xyz) is the index of a specific block within my ENTIRE kernel

Blockdim (xyz) is the size of my block

gridDim (xyz) is the size of my grid (kernel data)

with these, I need to take all of these components together so that each thread can compute its global thread id for computation purposes (think about the vector example in the textbook, I forgot the name)

__global__ void saxpy(int n, float a, float * restrict x, float * restrict y) { 

int i = blockIdx.x*blockDim.x + threadIdx.x; if (i < n) y[i] = a*x[i] + y[i];

}

All of these values are held in a special CSU (control) register file which is indexed by warp_id

Speaking of warp id, there is also a grouping that needs to be done by the hardware to actually group threads together, since the compiler is just going to throw like say 512 threads at me and we need to group those threads into different groups. I will need to ask about more specifics in office hours next week to terrorize sooraj.

Other things about warp scheduling—we realized today that since my core is pipelined, I wont know when I hit an end of packet in the warp scheduler until 2 cycles later from decode and so I need to flush my fetch and decode and I need to probably keep a “restart” table for which I need to hold PC values upon the rescheduling of said warp. This is not the worst to implement.

We also realized that we want to keep two warps issuing at a time—this is because each warp is mapped to a specific bank In the register file and we have two banks—this means since the operand collector will take at most 2 cycles to collect data, if we schedule two warps that are in different banks, we can take 2 cycles to collect 2 instructions, which increase our throughput and makes it so we don’t have to wait. This likely won’t complicate my logic that much.

Last thing is to start actually thinking about what my warp scheduler will look like. I think first off I need to come up with states for each warp and store all states in a table which is indexed into by warp_id. Below is a jumble of random arch I was coming up with in MSEE today.

I think for now the states make sense and probably don’t need to much changing and the table definitely makes sense to have (and also add the PC restart address), the muxing of control signals makes sense since I’m only operating on one warp’s state at a time (although this may change to 2 due to the operand collector discussion earlier). The hard part (although conceptually easy) will be coming up with the arbiter to pick warps out of my table to put into my active group. For not In my head the active group looks a bit like a fifo structure, where I can pop out warps that have stalled and reiterate through currently active warps but this is all really up in the air currently. 

The scheduling is going to be like a round robin scheme for upper for which warps to rotate in and out and in the inner level specifically to schedule we will use GTO scheme to service warps. I need to think a little more about the priority implementation I have inmind currently. 
