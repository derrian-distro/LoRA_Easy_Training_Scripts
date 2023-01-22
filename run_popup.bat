@echo off

echo Starting popup training...
venv\Scripts\accelerate.exe launch --num_cpu_threads_per_process 12 lora_train_popup.py
echo Training complete.
pause