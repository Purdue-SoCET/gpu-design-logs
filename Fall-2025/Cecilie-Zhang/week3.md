# Week 3: Research Poster

Status: I'm not stuck with anything

**Progress**: Do research about exploiting uniform or affine variables in GPU

- What are uniform or affine variables?
    - Uniform variable: A variable that has the same value across all threads
    - Affine variable: A variable that has a value that changes in a predictable way across all threads (Vi = x + iy)
- Uniform and affine variables can be stored in the register file with less bits. For example, because uniform variables have the same value across all threads, this value only needs to be stored in one register. This means that the extra storage can be used for more inflight warps (active warps) and increase memory latency. 


**Partial Register File Access**: 
- Focuses on how to optimize the register file by compressing the registers that are written back to the register file. 
- Compresses the register through the BDI compression (Base-Delta-Immediate)
    - Inside a register vector (32 registers for a warp), many of the values stores are similar or in a low dynamic range. Therefore, the values can be represented by a base value, and an array of differences (relative to the base) whos combined size is smaller than the original storage. Some values might differ the base+delta value by a small value. In those cases, an immediate value is incorporated into the encoding
    - Studies have shown that BDI imoproves performance for both single-core and multi-core by almost doublingthe cache size

- It's common to have two bases, one base being zero where the immediate can be thought of as an offset from the zero. The other base being randomly chosen. 

**What are the benefits of BDI**: 
1. High compression ratio: It can often compress some of teh frequently-observed patterns
2. Low decompression latency: To decompress the data, you only need a simple maksed vector addition
3. Relatively modest hardware overhead and impleemntation complexity: compression and decompression only need vector addition, subtraction and comparison operations

**What are some patterns that are observed across data?**
- Zeros: Zero is one of the most frequently observed value in application data. Zero is often used to initialize data, represent NULL pointers or false boolean values
- Repeated Values: A large contiguous region og memory that contains the same repeated value
- Narrow values: When a small value is stored using a large data type. E.g. storing a one-byte value in four-byte integer
- We notice that all of the patters observed above fall under what we call the low dynamic range (a set of values where the difference between the values is much smaller than the value itself)

![](./images/week3/image1.png)

**Why does BDI work?**
1. Simialr data values and types are often grouped together (often due to arrays)
2. Low dynamic range of the data

## Compression Algorithm
**Figure of how BDi works:**
![](images/week3/image2.png)
Assume that you have a set of values that wants to be compressed, S:
- Observation 1: For compression to work, the number of bytes used to represent the delta needs to be strictly less than the number of bytes used to represent the data itself
- Observation 2: The base can be decided by computing the max or min of S. The optimal can be reached by either choosing max(S), min(S), or the value in the middle. However, this introduced compression latency. As a result, it's better to choose the first value from S as the base to avoid the added latency. This only reduces the average compression rate by 0.4%
## Decompression Algorithm
- The values can easily be recalculated by adding the delta to the base

### Why could multiple bases help?
- In a set of data, there might be severla different types of data, like pointers and 1-byte integer (high dynamic range). Obviously, one base won't work for this case
![](images/week3/image3.png)
- Increasing the number of basees will increase the overhead (storage of the bases). Studes have shown that the optimal number of bases is 2. **Having two bases introduces the isseu of what the second arbitrary base should be**
- Most of the times when there are mixed data types, the cause is usually an aggregate data type (e.g. a struct). This means that there are wide values with low dynamic range and narrow values. That's why it's usually better to choose an arbitrary base to compress the wide values and zero as the second base to compress the narrow values. This is called the BDI

## BDI Design
![](images/week3/image4.png)
![](images/week3/image5.png)
- The 1-byte sign extension is extend the 1-byte to 4-bytes using the MSB. If the 4-byte value matches the delta, then the data can be compressed. Otherwise, the delta is too big to be represented by one byte

Bibliography:
- https://hal.science/hal-00396719v1/file/Collange_UniformAffineGPGPU_PPW09.pdf
- BDI: https://users.ece.cmu.edu/~omutlu/pub/bdi-compression_pact12.pdf 