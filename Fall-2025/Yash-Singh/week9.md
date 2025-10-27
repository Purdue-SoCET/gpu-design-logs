NOTE: SO SORRY FOR THE DELAY. I WAS THINKING A LOT OF THOUGHTS!
Status: Decent, need some hands with building the functional simulator integration lowkey.

SUMMARY:
This week was focused on developing the functional simulator and cycle accurate simulator base classes for everyone to simulate their modules in. Much of the efforts were dedicated towards experimenting in python to find a hierarchy that works.

MEETINGS THIS WEEK:
1. 19/10: Senior Design Meeting, focused on fleshing out some co-design ideas and requirements across teams. Decided what kind of framework would be needed and what peoples expectations are out of this simulator.
     KEY TAKEAWAYS: Use a hierarchichal, modular-level class structure to break down the flow. I assumed the responsibility to make the base class for the functional simulator.
   
3. 20/10: Meeting with Sooraj and the Compilers team to discuss how the threads and predication and stack was going to be implemented together to handle function calls.
    KEY TAKEAWAYS: Reserve a single thread to handle function calls. Unlikely tha ew'll have multiple fucntion calls in our program anyway, so this can work just fine. Clarified some requirments from graphics.
   
5. 23/10: Hardware Meeting to discuss work thus far on the simulator, and how to use what I had thus far. I also took the time to clarify some requirements and necessities.
    KEY TAKEAWAYS: This framework can work, everyone in hardware is instructed to make some unit tests for their modules by NEXT sunday (not the upcoming sunday). Also bought up the necessity of some sort of performance counter/tracker.

PROOF OF WORK:

For the hierarchy of the functional unit base class for testing, I made the following:

Each pipeline stage communicates through a **`StageInterface`** object, which manages:
- **valid/ready handshakes**
- **cycle-based latency**
- **backpressure and stalls**

Each simulation **cycle** runs in three main phases:

1. Every `StageInterface` advances timing (`.tick()`).
2. Each `PipelineStage` executes its `.cycle()`, which:
   - Pulls data from its input interface (`.receive()`).
   - Processes it (`.process()`).

I also made a small test case with my decode stage to see how it does--it seems to be decent. I started wwork on a more cycle-sim level implementation, but its still a work in progress and needs more revision. Beta tests as cuh are going to be pushed onto 'testing'.
See the commit blame here: https://github.com/Purdue-SoCET/gpu/commit/2e116abc774cc2b08b6001c1174f7a67cb4cf7ba#diff-96fb16bf99f473aaaf2fd253ef29ad812e307a98c328a483f1a826353eb866c9
   - Sends results to its output interface (`.send()`).
3. The simulator runs stages **back-to-front** each cycle to avoid overwriting pending values.
