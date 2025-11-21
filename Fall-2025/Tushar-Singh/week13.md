Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Overview

This week consisted of 3 presentations. There was the code review, the poster presentation, and the design review. Each of these had a different target audience.

Aiden is sorting an issue with the visiblity of CSR's for block dimensions going from the kernel to the hardware. This is a block of a kind but not too big of an issue immediately.

The team laid out a schedule during our weekly meeting. I skipped the meeting, so I do not have notes on it, but will adhere to these deadlines. I intend to work on the report and relevant code before the end of break.

### Code Review

This is internal to the team. We demonstrated our current coding concepts, the state of our kernels, and the interactions we have had so far with other teams. This was good to clarify our perspectives and find issues in what we are doing. I have realized that the python simulator does not seem to be outputting the correct SAXPY outputs, so I am now debugging the python sim. Listening to the other presentations gives me an idea of how the hardware will be layed out, which allows me to write hardware aware kernels to the extent available.

### Poster Presentation

This was external to SOCET. Not much to say here. We made a poster, and presented it. It seems that as far as software goes, it's easy enough to get the idea across of what we are trying to do.

### Design Review

Either 0 or 2.5% of the grade. We presented to some team leads, mostly AIHW and GPU people. This was a mashup of the code review slides and slides from the week 4 presentation that laid out our original expectations. We only got one question, so the presentation practically went off without a hitch.

### Another matmul and saxpy update

I'm still debugging the saxpy asm. To me, it looks like the issues might just be in how I addressed the memory space, since the values looked okay. I also need to confirm that the original X and Y arrays, as well as the value of a match. The execution itself is not wrong, but the final output is only giving values every 8 bytes instead of at every word. Also, the outputs are incorrect.  I've only just now familarized myself with how the python simulator is getting its output, so now I should be able to debug it and get correct outputs before the next GPU team meeting that I show up to.

As far as matmul goes, I am writing a kernel that uses one threadblock. The TB strides across the matrices. with one constant matrix and one striding matrix(32x32) group at a time, such that all threads are busy with meaningful work. This testcase will work to see if we can multiply matrices of any size, which is a very common GPU workload.

### Plan over thanksgiving week

Finish debugging saxpy, finish writing and then testing matmul. Produce inital draft of final report. Work with compilers team and HW to produce a meaningful assembly file and run it on the functional simulator as soon as possible so that more time can be devoted to the cycle accurate simulator.