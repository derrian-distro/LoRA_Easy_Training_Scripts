@echo off
Call PowerShell -NoProfile -ExecutionPolicy Bypass -Command "& {Start-Process PowerShell -ArgumentList 'Set-ExecutionPolicy Unrestricted -Force' -Verb RunAs}"