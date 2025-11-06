from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
 
@dataclass
class Instruction:
    iid: int
    pc: int
    issued_cycle: Optional[int] = None
    stage_entry: Dict[str, int] = field(default_factory=dict)   # stage -> first cycle seen
    stage_exit:  Dict[str, int] = field(default_factory=dict)   # stage -> last cycle completed
    fu_entries:  List[Dict]     = field(default_factory=list)   # [{fu:"ALU", enter: c, exit: c}, ...]
    wb_cycle: Optional[int] = None

    def mark_stage_enter(self, stage: str, cycle: int):
        self.stage_entry.setdefault(stage, cycle)

    def mark_stage_exit(self, stage: str, cycle: int):
        self.stage_exit[stage] = cycle

    def mark_fu_enter(self, fu: str, cycle: int):
        self.fu_entries.append({"fu": fu, "enter": cycle, "exit": None})

    def mark_fu_exit(self, fu: str, cycle: int):
        for e in reversed(self.fu_entries):
            if e["fu"] == fu and e["exit"] is None:
                e["exit"] = cycle
                return

    def mark_writeback(self, cycle: int):
        self.wb_cycle = cycle

@dataclass
class ForwardingIF:
    payload: Optional[Any] = None
    valid: bool = False
    wait: bool = False
    name: str = field(default="BackwardIF", repr=False)

    def push(self, data: Any) -> bool:
        if self.valid:
            return False
        self.payload = data
        self.valid = True
    
    def force_push(self, data: Any) -> None:
        self.payload = data
        self.valid = True

    def snoop(self) -> Optional[Any]:
        return self.payload if self.valid else None
    
    def pop(self) -> Optional[Any]:
        if not self.valid:
            return None
        data = self.payload
        self.payload = None
        self.valid = False
        return data
    
    def set_wait(self, flag: bool) -> None:
        self.wait = bool(flag)

    def clear_all(self) -> None:
        self.payload = None
        self.valid = False
        self.wait = False

    def __repr__(self) -> str:
        return (f"<{self.name} valid={self.valid} wait={self.wait} "
            f"payload={self.payload!r}>")

@dataclass
class LatchIF:
    payload: Optional[Any] = None
    valid: bool = False
    read: bool = False
    name: str = field(default="LatchIF", repr=False)
    forward_if: Optional[ForwardingIF] = None

    def ready_for_push(self) -> bool:
        if self.valid:
            return False
        if self.forward_if is not None and self.forward_if.wait:
            return False
        return True

    def push(self, data: Any) -> bool:
        if not self.ready_for_push():
            return False
        self.payload = data
        self.valid = True
        return True
    
    def force_push(self, data: Any) -> None: # will most likely need a forceful push for squashing
        self.payload = data
        self.valid = True

    def snoop(self) -> Optional[Any]: # may need this if we want to see the data without clearing the data
        return self.payload if self.valid else None
    
    def pop(self) -> Optional[Any]:
        if not self.valid:
            return None
        data = self.payload
        self.payload = None
        self.valid = False
        return data
    
    def clear_all(self) -> None:
        self.payload = None
        self.valid = False
    
    def __repr__(self) -> str: # idk if we need this or not
        return (f"<{self.name} valid={self.valid} wait={self.wait} "
                f"payload={self.payload!r}>")
    
@dataclass
class Stage:
    name: str
    behind_latch: Optional[LatchIF] = None
    ahead_latch: Optional[LatchIF] = None
    forward_if: Optional[ForwardingIF] = None
    # forward_ifs: Dict[str, ForwardingIF] = field(default_factory=dict)

    def has_input(self) -> bool:
        if self.behind_latch is None: 
            # no behind latch, so always assume true
            return True
        return self.behind_latch.valid
    
    def get_input(self) -> Optional[Any]:
        if self.behind_latch is None:
            # no behind latch, so pop nothing
            return None
        return self.behind_latch.pop()
    
    def can_output(self) -> bool:
        if self.ahead_latch is None:
            # no ahead latch, so always assume true
            return True
        if self.ahead_latch.forward_if and self.ahead_latch.forward_if.wait:
            return False
        return self.ahead_latch.ready_for_push()
    
    # def can_output(self) -> bool:
    #     if self.ahead_latch is None:
    #         # no ahead latch, so always assume true
    #         return True
        
    #     # If *any* of the forwarding interfaces assert wait → stall output
    #     for name, f_if in self.forward_ifs.items():
    #         if f_if.wait:
    #             print(f"[{self.name}] Stalled by forwarding path '{name}' (wait high)")
    #             return False

    #     return self.ahead_latch.ready_for_push()
    
    def send_output(self, data: Any) -> None:
        if self.ahead_latch is None:
            print(f"[{self.name}] Done: {data!r}")
        else:
            if self.ahead_latch.ready_for_push():
                self.ahead_latch.push(data)
            else:
                print(f"[{self.name}] Could not push output — next stage not ready.")

    def compute(self, input_data: Any) -> Any:
        # default computation, subclassess will override this
        return input_data

    def step(self) -> None:
        if not self.can_output():
            print(f"[{self.name}] Stalled — next stage not ready.")
            return
        
        if not self.has_input():
            print(f"[{self.name}] No input available, idle this cycle.")
            return
        
        input_data = self.get_input()
        output_data = self.compute(input_data)
        self.send_output(output_data)