---
id: KB-008
title: OneDrive, shared drives and restoring deleted files
category: Files & OneDrive
last_updated: 2026-04-28
---

## Where to store files
- **OneDrive**: your personal work files. 1 TB per user. Backed up automatically.
- **Shared drives (S:, \\fs01)**: team files, permissioned by AD group.
- **Teams/SharePoint**: files you collaborate on with a team.
Do not store work files only on your desktop or C: drive; they are not backed up.

## OneDrive sync problems
Common causes of sync getting stuck:
- File paths longer than 400 characters
- File names containing characters such as `" * : < > ? / \ |` or starting with a space
- Files open in another application
Fix the file names, then reset OneDrive: press Windows + R and run `%localappdata%\Microsoft\OneDrive\onedrive.exe /reset`. Sync restarts within a few minutes.

## Restoring deleted files
- **OneDrive**: deleted files stay in the OneDrive recycle bin for 93 days. Go to https://onedrive.com > Recycle bin.
- **Shared drives**: snapshots are taken every 4 hours and kept for 30 days. Right-click the parent folder > Properties > Previous Versions and choose a version to restore.
- Older than 30 days: raise a ticket; restore from backup tape takes 2-3 working days.

## Getting access to a shared folder
Request access through the Access Portal by selecting the folder's AD group (e.g. FS-Finance-RW). The data owner must approve. After approval, log off and back on so the new group membership takes effect.
