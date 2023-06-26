import math
from typing import List, Optional

from torch.optim.lr_scheduler import _LRScheduler


# TODO: process first_cycle_steps according to restarts set, skip cycle_mult, add min_lr to the args, ensure warmup
#  steps is properly set up to be handled according to restart, and allow gamma to be set, rename it to "decay" or
#  something
#  args to add to the UI: min_lr, gamma
class CosineAnnealingWarmupRestarts(_LRScheduler):
    def __init__(self, optimizer, first_cycle_steps: int, cycle_mult: float = 1.0, min_lr: float = 1e-6,
                 warmup_steps: int = 0, gamma: float = 0.9, last_epoch: int = -1):
        self.first_cycle_steps = first_cycle_steps
        self.cycle_mult = cycle_mult
        self.max_lrs: list[float] = []
        self.active_lrs: list[float] = []
        self.base_lrs: list[float] = []
        self.min_lr = min_lr
        self.warmup_steps = warmup_steps
        self.gamma = gamma
        self.cur_cycle_steps = first_cycle_steps
        self.step_in_cycle = last_epoch
        self.last_epoch = last_epoch
        self.cycle: int = 0
        self._last_lr = None

        if self.warmup_steps >= self.first_cycle_steps:
            raise ValueError(
                f'[-] warmup_steps must be smaller than first_cycle_steps. '
                f'{self.warmup_steps} < {self.first_cycle_steps}'
            )

        super().__init__(optimizer, last_epoch)

        self.init_lr()

    def init_lr(self):
        self.max_lrs = []
        self.active_lrs = []
        self.base_lrs = []
        for param_group in self.optimizer.param_groups:
            self.max_lrs.append(param_group['initial_lr'])
            self.active_lrs.append(param_group['initial_lr'])
            min_lr = self.min_lr if param_group['initial_lr'] > self.min_lr else 0.0
            param_group['lr'] = min_lr
            self.base_lrs.append(min_lr)

    def get_lr(self) -> List[float]:
        if self.step_in_cycle == -1:
            return self.base_lrs

        if self.step_in_cycle < self.warmup_steps:
            output = []
            for max_lr, base_lr in zip(self.active_lrs, self.base_lrs):
                output.append((max_lr - base_lr) * self.step_in_cycle / self.warmup_steps + base_lr)
            return output

        output = []
        for max_lr, base_lr in zip(self.active_lrs, self.base_lrs):
            output.append(
                base_lr + (max_lr - base_lr) * (1 + math.cos(
                    math.pi * (self.step_in_cycle - self.warmup_steps) / (self.cur_cycle_steps - self.warmup_steps)
                )) / 2.0)
        return output

    def step(self, epoch: Optional[int] = None):
        if epoch is None:
            epoch = self.last_epoch + 1
            self.step_in_cycle = self.step_in_cycle + 1
            if self.step_in_cycle >= self.cur_cycle_steps:
                self.cycle += 1
                self.step_in_cycle = self.step_in_cycle - self.cur_cycle_steps
                self.cur_cycle_steps = (
                        int((self.cur_cycle_steps - self.warmup_steps) * self.cycle_mult) + self.warmup_steps
                )
        elif epoch >= self.first_cycle_steps:
            if self.cycle_mult == 1.0:
                self.step_in_cycle = epoch % self.first_cycle_steps
                self.cycle = epoch // self.first_cycle_steps
            else:
                n: int = int(math.log((epoch / self.first_cycle_steps * (self.cycle_mult - 1) + 1), self.cycle_mult))
                self.cycle = n
                self.step_in_cycle = epoch - int(
                    self.first_cycle_steps * (self.cycle_mult ** n - 1) / (self.cycle_mult - 1)
                )
                self.cur_cycle_steps = self.first_cycle_steps * self.cycle_mult ** n
        else:
            self.cur_cycle_steps = self.first_cycle_steps
            self.step_in_cycle = epoch

        for i in range(len(self.active_lrs)):
            self.active_lrs[i] = self.max_lrs[i] * (self.gamma ** self.cycle)

        self.last_epoch = math.floor(epoch)

        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group['lr'] = lr
        self._last_lr = [group['lr'] for group in self.optimizer.param_groups]
