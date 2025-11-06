from latch_forward_stage import LatchIF, ForwardingIF, Stage
from typing import Any

class Stage0(Stage):
    def compute(self, input_data: Any) -> Any:
        if input_data is None:
            return None
        
        if self.forward_if and self.forward_if.wait:
            print(f"[{self.name}] Stalled due to wait from next stage.")
            return None
        # if any(fwd.wait for fwd in self.forward_ifs.values()):
        #     print(f"[{self.name}] Stalled due to wait from next stage(s).")
        #     return None
        
        fwd_val = self.forward_if.snoop() if self.forward_if else None
        # fwd_vals = [fwd.snoop() for fwd in self.forward_ifs.values() if fwd.snoop() is not None]

        # fwd_sum = sum(fwd_vals) if fwd_vals else 0
        # output = input_data + fwd_sum + 100
        
        if fwd_val is not None:
            output = input_data + fwd_val + 100
        else:
            output = input_data + 100

        print(f"[{self.name}] Computed output: {output!r} (forward value: {fwd_val!r})")

        return output
    
class Stage1(Stage):
    def compute(self, input_data: Any) -> Any:
        if input_data is None:
            return None
        
        if self.forward_if and self.forward_if.wait:
            print(f"[{self.name}] Stalled due to wait from next stage.")
            return None
        # if any(fwd.wait for fwd in self.forward_ifs.values()):
        #     print(f"[{self.name}] Stalled due to wait from next stage(s).")
        #     return None
        
        # fwd_val = self.forward_if.snoop() if self.forward_if else None
        # fwd_vals = [fwd.snoop() for fwd in self.forward_ifs.values() if fwd.snoop() is not None]

        # fwd_sum = sum(fwd_vals) if fwd_vals else 0
        # output = input_data + fwd_sum + 100

        # print(f"[{self.name}] Computed output: {output!r} (forward value: {fwd_vals!r})")

        # fwd_if = self.forward_ifs.get("fwd_1to0")
        # if fwd_if:
        #     fwd_if.force_push(output)
        #     print(f"[{self.name}] Forwarded {output!r} to Stage0")

        # return output
        
        # output = input_data + 200
        # print(f"[{self.name}] Computed output: {output!r}")

        # if self.forward_if:
        #     self.forward_if.force_push(output / 2)
        #     print(f"[{self.name}] Forwarded back {output / 2!r} to Stage0")
        
        # return output

        fwd_val = self.forward_if.snoop() if self.forward_if else None

        if fwd_val is not None:
            output = input_data + fwd_val + 100
        else:
            output = input_data + 100

        print(f"[{self.name}] Computed output: {output!r} (forward value: {fwd_val!r})")

        return output
    
class Stage2(Stage):
    def compute(self, input_data: Any) -> Any:
        if input_data is None:
            return None
        
        output = input_data + 100
        print(f"[{self.name}] Computed output: {output!r}")

        # fwd_if = self.forward_ifs.get("fwd_2to0")
        # if fwd_if:
        #     fwd_if.force_push(output)
        #     print(f"[{self.name}] Forwarded {output!r} to Stage0")

        return output
    
class FetchStage(Stage):
    def compute(self, input_data: Any) -> Any:
        if input_data is None:
            return None
        
        # give instruction.PC to iCache, iCache will return the instruction if it has it, otherwise we will wait for memory,
        # and FetchStage will set the forwarding_if wait high so that the warp scheduler does not give new input to the fetch stage
    
### TESTING ###

stage0_stage1_latch = LatchIF(name = "Latch0to1")
stage1_stage2_latch = LatchIF(name = "Latch1to2")
forward_if_stage1_to_stage0 = ForwardingIF(name = "Forward1to0")
# forward_if_stage2_to_stage0 = ForwardingIF(name = "Forward2to0")
forward_if_stage2_to_stage1 = ForwardingIF(name = "Forward2to1")

stage0 = Stage0(
    name = "Stage0",
    behind_latch = None,
    ahead_latch = stage0_stage1_latch,
    forward_if = forward_if_stage1_to_stage0
    # forward_ifs = {"fwd_2to0": forward_if_stage2_to_stage0, "fwd_1to0": forward_if_stage1_to_stage0}
)

stage1 = Stage1(
    name = "Stage1",
    behind_latch = stage0_stage1_latch,
    ahead_latch = stage1_stage2_latch,
    forward_if = forward_if_stage1_to_stage0
    # forward_ifs = {"fwd_1to0": forward_if_stage1_to_stage0}
)

stage2 = Stage2(
    name = "Stage2",
    behind_latch = stage1_stage2_latch,
    ahead_latch = None,
    forward_if = forward_if_stage2_to_stage1
    # forward_ifs = {"fwd_2to0": forward_if_stage2_to_stage0}
)

input_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# i = 0

# for cycle in range (5):
#     print(f"\n=== Cycle {cycle} ===")

#     if cycle == 1:
#         forward_if_stage1_to_stage0.set_wait(True)
#         print("[Stage1] Setting wait HIGH (stall Stage0)")
#     elif cycle == 3:
#         forward_if_stage1_to_stage0.set_wait(False)
#         print("[Stage1] Clearing wait LOW (resume Stage0)")

#     if stage1.behind_latch and stage1.behind_latch.valid:
#         input_stage1 = stage1.behind_latch.pop()
#         output_stage1 = stage1.compute(input_stage1)

#     if not forward_if_stage1_to_stage0.wait:
#         input_stage0 = input_values[i]
#         i = i + 1
#     output_stage0 = stage0.compute(input_stage0)
#     stage0.send_output(output_stage0)

for cycle in range(10):
    print(f"\n=== Cycle {cycle} ===")

    ### STAGE2 LOGIC ###
    if stage2.behind_latch and stage2.behind_latch.valid:
        input_stage2 = stage2.behind_latch.pop()
        output_stage2 = stage2.compute(input_stage2)

    ### STAGE1 LOGIC ###
    if not forward_if_stage2_to_stage1.wait and stage1.behind_latch.valid:
        input_stage1 = stage1.behind_latch.pop()
        output_stage1 = stage1.compute(input_stage1)
        stage1.send_output(output_stage1)

    ### STAGE0 LOGIC ###
    if not forward_if_stage1_to_stage0.wait:
        input_stage0 = input_values[cycle]
        output_stage0 = stage0.compute(input_stage0)
        stage0.send_output(output_stage0)