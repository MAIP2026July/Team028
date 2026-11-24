---
id: KB-012
title: Laptop performance, docking stations and hardware faults
category: Laptop & Hardware
last_updated: 2026-05-25
---

## Laptop is slow
1. Restart - many updates only finish after a reboot. Check Settings > Windows Update for "Restart required".
2. Open Task Manager (Ctrl + Shift + Esc) and look for apps using high CPU, memory or disk.
3. After a large update, OneDrive may re-sync many files; pause sync for a couple of hours if needed.
4. Run Disk Cleanup and tick "Windows Update Cleanup" to free space.
5. Keep at least 15% of disk space free.

## Docking station and monitors
- Use the USB-C port marked with the Thunderbolt or DisplayPort icon.
- Update dock firmware from Software Center ("Dock Firmware Updater").
- Unplug the dock power for 30 seconds to reset it.
- Press Windows + P and choose "Extend".

## Battery problems
Run `powercfg /batteryreport` in Command Prompt; it creates battery-report.html. If "Full charge capacity" is below 50% of "Design capacity", the battery should be replaced. Raise a hardware ticket; replacements under warranty are free.

## Liquid spills and physical damage
Turn the laptop off immediately, unplug it, and do not try to charge it. Bring it to the IT bar or raise a P2 ticket. A loaner laptop is available the same day, and your OneDrive files will be available on it straight away.
