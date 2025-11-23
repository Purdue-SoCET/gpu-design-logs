Status: not stuck

- Helped create poster and presented at fall research conference. [SoCET Fall 25 Poster.pptx](https://github.com/user-attachments/files/23698506/SoCET.Fall.25.Poster.pptx)
- Created this SIMD diagram<img width="1327" height="766" alt="image" src="https://github.com/user-attachments/assets/7c7db3e6-79bd-4fa7-94cf-39bee05e38f5" />
- Testing and debugging saxby.asm. Currently, the program doesn't actually predicate correctly!
    - PC goes to branch PC rather than PC + 4 and predicating.
- Fixed predication logic and halt_count (number of halted warps) logic. Currently trying to figure out what software is doing that
is resulting in an integer overflow for a LW? 
