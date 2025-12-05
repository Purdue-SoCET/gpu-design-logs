# Week 14
statement: I am not stuck.

## Progress this week
  - working on assembly test.
  - Started from triangle pipeline and split into small unit tests (matrix inversion, depth/Z‑test, vertex interpolation).
  - Working on matrix inversion assembly unit test first.

## Matrix inversion

### workflow
- Load 9 floats from memory
- Compute 2×2 cofactor
- Compute invDet: invDet = 1.0 / det
- Compute all 9 inverse elements: bc_im[i][j] = cofactor(i,j) * invDet
- Store results

### code
  - matrix loading
```
       #float m[3][3] = {
       #{1, 1, 1},
       #{arg.pVs[0][0], arg.pVs[1][0], arg.pVs[2][0]},
       #{arg.pVs[0][1], arg.pVs[1][1], arg.pVs[2][1]}};
      
       #x10 = address to matrix m
       lw x3, 0(x10) # m[0][0] at offset 0
       lw x4, 4(x10) # m[0][1] at offset 4
       lw x5, 8(x10)    
       lw x6, 12(x10)    
       lw x7, 16(x10)    
       lw x8, 20(x10)   
       lw x9, 24(x10)   
       lw x12, 28(x10)   
       lw x13, 32(x10) # m[2][2] at offset 32
  ```
- calcualte on the cofactor
```
       # x16: cofactor(0,0) = m[1][1]*m[2][2] - m[2][1]*m[1][2]
       mulf x14, x7, x13  
       mulf x15, x12, x8  
       subf x16, x14, x15 

       # x19: cofactor(0,1) = m[1][0]*m[2][2] - m[2][0]*m[1][2]
       mulf x17, x6, x13  
       mulf x18, x9, x8   
       subf x19, x17, x18 

       # x22: cofactor(0,2) = m[1][0]*m[2][1] - m[2][0]*m[1][1]
       mulf x20, x6, x12  
       mulf x21, x9, x7   
       subf x22, x20, x21 

       # x27: det = m[0][0]*cofactor(0,0) - m[0][1]*cofactor(0,1) + m[0][2]*cofactor(0,2)
       mulf x23, x3, x16  
       mulf x24, x4, x19  
       subf x25, x23, x24 
       mulf x26, x5, x22 
       addf x27, x25, x26 

       # double invDet = 1.0 / det;
       addi x28, x0, 1 # x28 = 1
       itof x28, x28   # x28 = 1.0 
       divf x29, x28, x27 # x29 = invDet = 1.0 / det
```
  - Inverse matrix calculation using cofactors and invDet
```
       # Row 0
       # cofactor(0,0) = m[1][1]*m[2][2] - m[2][1]*m[1][2]
       mulf x14, x7, x13  
       mulf x15, x12, x8  
       subf x16, x14, x15 # x16 = cofactor(0,0)
       mulf x2, x16, x29 # bc_im[0][0] = cofactor(0,0) * invDet

       # cofactor(0,1) = m[1][0]*m[2][2] - m[2][0]*m[1][2]
       mulf x17, x6, x13 
       mulf x18, x9, x8   
       subf x19, x17, x18 
       mulf x3, x19, x29 # bc_im[0][1] = cofactor(0,1) * invDet

       # cofactor(0,2) = m[1][0]*m[2][1] - m[2][0]*m[1][1]
       mulf x20, x6, x12  
       mulf x21, x9, x7   
       subf x22, x20, x21
       mulf x4, x22, x29 # bc_im[0][2] = cofactor(0,2) * invDet

       # Row 1
       # cofactor(1,0) = m[0][2]*m[2][1] - m[0][1]*m[2][2]
       mulf x14, x5, x12  
       mulf x15, x4, x13 
       subf x16, x14, x15 
       mulf x5, x16, x29 # bc_im[1][0] = cofactor(1,0) * invDet

       # cofactor(1,1) = m[0][0]*m[2][2] - m[0][2]*m[2][0]
       mulf x17, x3, x13
       mulf x18, x5, x9   
       subf x19, x17, x18 
       mulf x6, x19, x29 # bc_im[1][1] = cofactor(1,1) * invDet

       # cofactor(1,2) = m[0][1]*m[2][0] - m[0][0]*m[2][1]
       mulf x20, x4, x9   
       mulf x21, x3, x12  
       subf x22, x20, x21 
       mulf x7, x22, x29 # bc_im[1][2] = cofactor(1,2) * invDet

       # Row 2
       # cofactor(2,0) = m[0][1]*m[1][2] - m[0][2]*m[1][1]
       mulf x23, x4, x8  
       mulf x24, x5, x7  
       subf x25, x23, x24
       mulf x8, x25, x29 # bc_im[2][0] = cofactor(2,0) * invDet

       # cofactor(2,1) = m[0][2]*m[1][0] - m[0][0]*m[1][2]
       mulf x26, x5, x6  
       mulf x27, x3, x8   
       subf x28, x26, x27 
       mulf x9, x28, x29 # bc_im[2][1] = cofactor(2,1) * invDet

       # cofactor(2,2) = m[0][0]*m[1][1] - m[0][1]*m[1][0]
       mulf x30, x3, x7   
       mulf x2, x4, x6    
       subf x2, x30, x2  
       mulf x10, x2, x29 # bc_im[2][2] = cofactor(2,2) * invDet
```
- Store all 9 results
```
       sw x2, 0(x11) # bc_im[0][0]
       sw x3, 4(x11) 
       sw x4, 8(x11)  
       sw x5, 12(x11) 
       sw x6, 16(x11) 
       sw x7, 20(x11) 
       sw x8, 24(x11)  
       sw x9, 28(x11) 
       sw x10, 32(x11) # bc_im[2][2]
       halt
```







  
