# Week 14 Design Log
## 11/28/25 - 12/04/25
I am not currently stuck or blocked

## Sunday (11/30/25) - Final Report Preparation
- Looked through report rubric to get a gist of what needs to be included in the report
- We had a lot of things covered throughout the semester
- Checked my design logs to kind of make a list of what we did the entire semester, brought it down to
- 1) ISA; 2) Stack; 3) Twig Teal Card; 4)PPCI; 5) Preprocessor; 6) Immediate Generator; 7) Codegen; 8) Assembler
- Made a big list of items that we've covered and assigned myself to the ones I'm familiar with
- Looked through the example section formats in the Report Format
- Added raw sections for now to talk to teammates about later
- Will need to discuss with teammates and Sooraj on the Results section of the report

## Monday (12/01/25) - Weekly Meeting with Sooraj
- Missed meeting with Sooraj, will try to plan a meeting later in the week

## Thursday (12/04/25) - Weekly SoCET Meeting
- DFT Technique: Scan Insertion
- Converts FFs to be controllable/observable
- Auto Test Pattern Generation (ATPG); Make patterns and create expected response;  compared pass/fail
- On-Chip Clock Controller (OCC); bridge between slow tester clock and fast internal clock networks; switches to what is needed
- Scan Insertion: Scripting; scan IO, clks, rsets, synthesis steps
- Main DT Trade Off; more scan chains reduce chain length but requires more scan IOs
- Scripting had many manual inscriptions, so had to decide parameters by themselves
- There are DFT Rules that needs to be followed for ATPG pattern; these warning were broughout in the summary report
- Scan Compression; has compressor and decompressor block; simple fan out
- Main takeaways were great learning experience and real-world exposure to Synopsys DTMAX/TestMAX workflows

- Timothy announces tape out of AFT
- From Design Flow team who worked with AMD AI during sumer
- GPU SRAM > GPU HBM > CPU DRAM
- Keep as much in the GPU as possible to avoid memory
- Matrix Multiplication is very Prallelizable
- Different words and each having a heat map
- Take vector, find max, shift it down; finding softmax; used as probability distribution
- Tiling is how GPU SRAM is utilized; load in a tile and multiply, and reuse it; 