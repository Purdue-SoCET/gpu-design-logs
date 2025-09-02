# Week 2

## Status

## Progress

### Videos

**Latency and Throughput**

Propagational delay (t_PD): Time from input to output
  
Latency: Time from an input to an associated output
  
Throughput: Rate at which inputs or outputs are 
  
Pipeline:
- Overlap to increase throughput of system
- Stage: each step is a stage

**Pipeline Circuits**

Combinational Circuits:
- Latency == t_PD
- Throughput = 1/(t_PD)
  
Pipeline Circuits:
- latency of each stage is longest delay in that stage -> determines max CLK speed
- Throughput for a stage = 1/(t_PD for that stage)
- Use Registers to store values between stages of pipeline
- Latency of a K-Pipeline = K * peroid of CLK
- Throughput of K-Pipeline = freq of CLK

**Pipeline Methodology**

- Draw lines through ciruit from top to bottom -> registers will be located at intersections
- Goal: Max throughput with fewest possible registers
- Latency = longest path
- Throughput improved by breaking up long combinational path, allowing for a faster CLK
- Too many stages if latency hurt and throughput doesn't improve
- Pipeline components to further decrease bottlenecks

**Circuit Interleaving**

- Add many instances of long stage module switch between uses of each
- Ex: 2 washers and 2 dryers -> if 1 step = 30 minutes then throughput = 2/30 or 1/15 and latency = 60 min

**Control Structure**

- Synchronous, Globally Timed: Easy to design but can be wasteful
- Synchronous, Locally Timed: Best way to build large systems
- Asynchronous, Globally Timed: Large systems can be very complicated
- Asynchronous, Locally Timed: next best idea
- t_CLK = longest stage t_PD + t_setup + t_ PD,REG
- For K pipeline: Throughput = 1/t_CLK ; Latency = K * t_CLK = K / Throughput
   
### Readings
