Status: working on cleaning up the emulator and starting the warp scheduler cycle sim, feeling semi-good about progress, feel like I understand everything required tho

I have not written design logs in like forever since I completely like forgot about them for a couple weeks lol (and spring break) so I’m just gonna dump down everything that I have onto here for now.

Big thing->emulator is functionally complete! Actually we don’t truly know if its functionally complete since we don’t have many tests yet but I have been in contact with Zay and Pranav and we kinda agreed that they would hand craft some testcases for us to go and check to see if our emulator is actually correct.

This is what the instruction file format looks like 

![image13.png](image13.png)

Hex encoding #{bitwise translation} {assembly instruction}

![image14.png](image14.png)

The setup is a lot like the 437 flow, where we have a simulated memory with the instructions and we log the nonzero contents of memory into another file.

The memory file will be {address} {data}

Ok so there is a ton of stuff in the way we set up the emulator currently.

In terms of classes, we have a warp, reg file, predicate register file, memory, and instruction class. We instantiate one memory object (global memory) and however many warps we need (for emulation purposes we could technically just have 1024 threads in a warp). We call our emulation on each warp and then each line we read will get instantiated into its own instruction object.

Currently, there is a ton of stuff that can be shuffled around and cleaned up and so I think next week me seth and felix will probably spend some time smoothing things our and going over what we can clean up and organize. 

I’m going to try to write the memory file in a more efficient manner next week because currently it is taking way to long to dump values into memory.

I will also have to start giving thought to the warp scheduler structure next week lol. Hopefully 437 does not take a whole lot of time this week to get done (I don’t think it should).

I also lowkey want to touch up with my oop with python specifically, since I kinda forgot everything that was going on lol so now when gpt generates me bs I can actually call it out without blind faith following its code.

NEXT WEEK OBJECTIVES: 

-clean up/streamline memory class for emulator

-start on the warp scheduler class and figure out what everything else is set up like in the functional sim

-touch up on oop with python

-get more testcases from compilers, hopefully jalrs and branches to test our predicate mask implementations.