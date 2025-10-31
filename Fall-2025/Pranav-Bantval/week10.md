# Week 10

State: there's a lot of work

Progress: we have every type besides branch/jump/p/csr in the compiler

I don't know how to do predication in the compiler code itself. This week I am also like half way to adding floating point and function calls (without the stuff talked about in week 9).

### predication code current ideas
- emit different ir than what's currently emitted. this will be kinda hard since i don't know ir. i might also have to change the syntax tree.
- once we emit a different ir we can use that ir to pattern match for btype.
- the problem is that ir naturally breaks up code into basic blocks, but for if statement, we don't really want the condition and ifstatement and else statement codes in different blocks, they can all be in the same one and run sequentially. This means the tree would have to change.
- one other method would be to use the current ir produced `cjmp` and pattern match it to branch then push to the predicate stack and use peek on every instruction to find the current predicate in the stack for every instruction.  

the second problem:
- ok we can add to the software predicate stack (referred to as SPS or stack) when we pattern match for B type NO PROBLEM. but how do we pop from SPS? the syntax tree generates basic blocks and numbers them somehow. currently we hypothesize that if the basic block is less than the current block that signifies a reconvergence point. this might not be too hard to do in code since basic block number can be printed easily. ok we can pop off the predicate stack, but how do we jump to the other condition that we diverged from?? we'd need to save both the convergence and divergence points and push all predicates (e.g. predicates for if, `n` else if's, else) on the stack right before the divergence point, take one branch, then once we reach the convergence point jump back to the divergence point and take all the paths. how do we know that all paths are taken? perhaps save the parent predicate and then peek the stack after popping at the convergence point.

this might be why it would be easier to change the syntax tree to put all if/else in the same block one followed by another? we'd still have the problem of finding out when to pop though.

lastly we could take the cop-out way and just compile everything with branch to assembly then add the predicate instructions after using an external python script. might be hard to detect/track loops i think though.

we also need to change the assembler to be able to start at any address.
