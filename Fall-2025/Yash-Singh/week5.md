Design log for this week (sorry for submitting it late I SWEAR I did things this week)

Key goals of this week: start to synthesize uarch across teams 

Roadblocks: None. Most things makes sense. Everything is coming into place. I see the light, the future is bright, and the horizon promises success. Beautiful.

Plans for next week:
  1. Make block diagrams for the units
  2. Ask sooraj about simulator frameworks
  3. Document meetings better
     
Links to readings, annotations, and notes taken this week:
1. Read, but not annotated:
  a. A Compile-Time Managed Mult-level Register Fil Hierarchy
  b. Energy-efficient Mechanisms for Managing Thread Context in Throughput Processors
2. Read + Annotated
  a. Random Notes: https://drive.google.com/file/d/1DBm6zjGyhJDa6IL7iAPKrF5EcHxS7T15/view?usp=sharing
  b. Improving GPU Performance via Large  Wars and Two-Level Warp Scheduling: https://drive.google.com/file/d/1vux7M_aO6S98tCzlUd3Ns4fT0f3tYlF2/view?usp=sharing
  c. GPU book Chapter 5 Readiings: https://docs.google.com/document/d/1oRuDElZsJe1Lt-ygDqS6sJVZ1vIpwepFmGAylGBdTas/edit?usp=sharing

Summaries for understandings:
KEY MEETINGS:
	1. 19/09/2025 - Friday Meeting to discuss Arch stuff (made questions list from the Compilers Team)
	2. 21/09/2025 - Sunday Meeting to discuss cross team things such as ISA, RFC(replaced with Register file) implementation
	3. 22/09/2025 - Monday meeting for project pitch
	4. 24/09/2025 - Met with Rishi to discuss specific uarch details for compiler managed packet based implementation into the instruction buffer + integration semantics with two level scheduling.
	5. 25/09/2025 - General Hardware team meeting to discuss uarch, two level scheduling, buffers, and OC usage.

NOTES:

1. Conversation summary for predication tables
  The conversation began with an explanation of compiler-managed predication tables for GPU branching. The key idea is that the compiler can convert divergent branches into a straight-line sequence of predicated instructions, using bit masks to control which threads' results are committed.
  Development of understanding
  Initial explanation: The conversation started with a high-level overview of predication, contrasting it with the "regular" method of hardware-managed serialization. The advantages and disadvantages of predication (efficient for short branches, wastes cycles for long ones) were outlined [4].
  Contrasting predication with serialization: A detailed comparison highlighted the core difference: predication uses a single, flattened instruction stream with conditional writes, while serialization uses a dynamic, stack-based approach to execute divergent paths sequentially [5].
  Function of predication tables (masks): The role of the "predication table" (more accurately, the predicate mask) was clarified. It's a bit vector that controls whether each thread's result is written back to memory or discarded [6].
  Refining predication flow: An initial misconception about predication only handling the if case was corrected. Predication handles both if and else paths by generating separate masks for each and executing a flattened instruction stream for the entire warp [7].
  Predication vs. serialization in implementation: The distinction between the compiler's static code transformation for predication and the hardware's dynamic stack management for serialization was emphasized. Predication is a single "flight" of instructions, while serialization involves multiple flights managed by a stack [9].
  Handling nested conditionals: The conversation explored how nested conditionals are managed by extending both predication (using combined predicate masks) and serialization (using a deeper hardware stack to manage more divergent paths) [10].
  Clarifying the "thread division" mechanism: A question arose about how threads are divided based on a conditional, given they all evaluate the same condition. The answer clarified that the division is a logical partitioning using execution masks, not a physical splitting of hardware. This partition controls which threads are active for a given instruction or instruction stream [11, 12].
  Questions asked
  What is the "regular" way to handle branch divergence besides predication?
  How does predication differ from the hardware-managed version, given both use masks?
  What does a predication table do, and which hardware unit uses it?
  Generate a flow chart for each implementation.
  How can all threads "visit" divergent branches simultaneously if they can only take one branch?
  If instructions for the if path are serialized, what happens with the else path?
  What happens with nested conditionals?
  Why and how are threads divided based on a conditional?
  Key analogies and examples
  Compiler-managed predication vs. hardware-managed serialization:
  BFS vs. DFS: Predication is like a breadth-first search (executing all levels at once), while serialization is like a depth-first search with backtracking (executing one path completely before moving to the next) [8].
  Team with tasks: A construction team analogy illustrated the difference. With predication, all workers perform all tasks, but only those with the right vest (mask) commit their work. With serialization, teams with different vests perform their respective tasks sequentially [5].
  Predicate mask function: The mask acts as a "gatekeeper" or "no-op" controller, allowing only active threads to write results while inactive threads have their results discarded [6, 12]. 
  Development in understanding
  The conversation moved from a high-level comparison to a detailed understanding of the underlying mechanisms. The user's grasp of the distinction between static (compile-time) code transformation and dynamic (runtime) hardware management deepened. The roles of the predicate mask and the hardware stack became clearer, as did the trade-offs between computational waste and scheduling overhead for the two approaches. The final questions refined the understanding of how threads, despite following only one logical path, still interact with the instructions of all divergent paths in a predicated scenario.
  
  2. What is the difference between the hardware managed vs. compiler managed implementations of predication?
	
	Compiler-managed predication is like a breadth-first traversal: All nodes at a certain "level" (representing one or more instructions) are visited simultaneously by all threads. The threads simply use masks to decide whether they should commit their results.
	Hardware-managed serialization is like a depth-first traversal with backtracking: The hardware follows one divergent path (one branch of the tree) to its conclusion, masking out all other threads. Then it "backtracks" and starts following another divergent path, activating a different subset of threads.
  <img width="873" height="62" alt="image" src="https://github.com/user-attachments/assets/f95a0ca0-466d-466e-a82f-00e76be8836c" />

	
	Hardware-managed serialization is like a depth-first traversal with backtracking: The hardware follows one divergent path (one branch of the tree) to its conclusion, masking out all other threads. Then it "backtracks" and starts following another divergent path, activating a different subset of threads.
<img width="922" height="1616" alt="image" src="https://github.com/user-attachments/assets/d971a492-b254-49b7-8a95-f1dae7e87014" />
