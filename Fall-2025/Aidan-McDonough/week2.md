# Week 2

## Status

## Progress

### Videos

**Latency and Throughput**
  
  Propagational delay (t_PD): Time from input to output
  
  Latency: Time from an input to an associated output
  
  Throughput: Rate at which inputs or outputs are processed

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

Combinational:

Pipeline:
  - Overlap to increase throughput of system
  - Stage: each step is a stage

### Readings
