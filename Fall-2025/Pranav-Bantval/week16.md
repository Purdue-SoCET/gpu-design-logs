#week 16

implemented predicate assignment, every instruction now has predicate. the compiler can probably work completely now, as long as there is no nested conditional (see week 15).

the compiler put's a lot of junk at the start of the asm file, if you are using the assembler I made, just delete that. it's there so that if we want to use ppci's linker we can

ppci's linker is gonna be hard to use so we probably wont.

no one has told us csr mappings so we made our own

csr[1] = threadidx; csr[2] = blockidx; csr[3] = blockdim;
