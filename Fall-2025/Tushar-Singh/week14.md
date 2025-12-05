Progress:

I am not stuck with anything right now.

GPU subteam: Graphics

## Overview

This week was not particularly productive for me. It was half off, and for the other half, I had two other course projects to work on. The main plan going forward is to finish the final report, assist the Aida/en's in getting the kernels to compile, and helping to make the SAXPY run on the emulator. I intend to meet with Felix tomorrow to try and debug the emulator to get the SAXPY running properly so that we will be able to move onto debugging the actual graphics programs.

### SAXPY

It seems there is a mismatch between the old program I wrote before and hardware's current concept of the execution model. Quite honestly, I haven't figured out what they are trying to do which makes it difficult to debug. Even if we have linearized the programming model, SAXPY should still run without issues. The output we are seeing is quite odd. My intention is that this will be running before Sunday so we have something to show.

### Matmul

This program seems to be working locally. I will be pushing it before Sunday. It is written to be memory aware and should lead to a good execution time. Since it is a standalone function based on the new programming model, it should ideally be runnable soon. I have delayed converting it for the TWIG compiler until the graphics programs compile, so that I can use them as a starting point for any necessary changes.

### Final Report

Got started here, but not that much to report for a design log. We missed the early review deadline.