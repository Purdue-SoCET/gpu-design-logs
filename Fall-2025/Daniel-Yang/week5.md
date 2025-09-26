Week 5 Design Log

Currently looking at different warp scheduler schemes, progress is good,
going slow but I think I'm picking up momentum thankfully.

Simplest is round robin, also looking into two-level scheduler currently

ROUND ROBIN:

-   Very simple scheme, each warp is assigned a number, the scheduler
    will try to schedule each warp in sequence

-   If a warp stalls, the next one is attempted to be scheduled instead

-   BIG ISSUES

    -   Since round robin causes warps to progress in lockstep, they are
        all often executing the same parts of the program at one time

    -   Since most warps come from the same kernel, they also have the
        same instructions at the same places most times

    -   This means warps usually reach long latency operations (cache
        misses) at the same time, which causes all warps to stall out at
        once, leading to lower throughput

TWO-LEVEL:

-   Still a fairly simple scheme, total warps are grouped into different
    groups by hardware

-   There is an inner scheduling (warps within a group) and an outer
    scheduling (fetch group)

    -   Inner scheduling is simply a round robin, but only across warps
        in that specific group

    -   Outer scheduling is also fairly simple, when all warps in a
        group stall, the outer scheduler will switch the fetch group to
        a different group, also in round robin

-   Warps within a group will stay relatively close because of round
    robin, which leads to good data reuse in caches

-   Different groups drift apart so not all warps in a kernel stall at
    once, SIMD lanes are still busy.

-   There are other different types of two-level schedulers, in any
    implementation there is an active set and a pending set. The first
    overall "group" scheduler hides long latencies (like memory access),
    the second "per warp" scheduler deals with shorter latencies like
    dependencies or busy resources.

This week I personally didn't talk to other teams but I know Yash talked
to both the backend team and a little to compilers about what how
everything is going to look. We are moving away from hardware
scoreboarding it seems to software scoreboarding where the instructions
will be sent to us in "packets", meaning there is a yield bit that lets
us know start of packet and if following instructions are dependent or
independent. I think this packeting will help us more with the second
level "internal" scheduler as there must be some way to keep track of
dependencies across packets. It seems that this dependency is tracked in
hardware and not software so we need to figure out where to go with
this: do I need to keep track of all registers in a packet then? But If
I keep track of current in flight warps and packets are of variable
length, then I have no way of knowing how big my buffer to keep track of
instructions must be. IDK. However, I'm feeling more and more confident
about this stuff and especially the scheduler protocol.

Next week I think I want to move forward with reading a little more
literature especially about instruction buffer things and register file
cache, and if we all are on the same page(hopefully) for the two-level
scheduling approach, then I would also like to start constructing the
block diagram and thinking through the logic for the scheduler. Also the
hardware frontend is likely going to try to talk to Rogers next week and
hopefully get some more clarifications on some GPU questions we still
have.
