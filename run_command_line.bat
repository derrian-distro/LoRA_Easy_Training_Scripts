@echo off

echo Starting command_line training...
venv\Scripts\accelerate.exe launch --num_cpu_threads_per_process 12 lora_train_command_line.py
echo Training complete.
pause