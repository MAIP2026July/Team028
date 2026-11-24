---
id: KB-004
title: Common Outlook problems and fixes
category: Email & Outlook
last_updated: 2026-04-10
---

## Outlook will not start or hangs on "Loading Profile"
1. Close Outlook fully (check Task Manager for OUTLOOK.EXE).
2. Press Windows + R and run `outlook.exe /safe`.
3. If Outlook opens in safe mode, an add-in is the likely cause. Go to File > Options > Add-ins > Manage COM Add-ins > Go, and untick add-ins one at a time.
4. If safe mode also fails, repair Office: Settings > Apps > Microsoft 365 Apps > Modify > Quick Repair.
You can always use Outlook on the web (https://outlook.office.com) while the desktop app is being fixed.

## Mailbox full
Standard mailboxes are 50 GB. When full you cannot send email.
- Empty the Deleted Items and Junk folders.
- Use the search box "size:>10MB" to find large emails and save attachments to OneDrive.
- Ask the Service Desk to enable the Online Archive; items older than 2 years are moved automatically.

## Search does not find recent emails
Outlook search uses the Windows Search index. Rebuild it: Control Panel > Indexing Options > Advanced > Rebuild. Indexing can take up to an hour; leave Outlook open.

## Shared mailboxes
When you are given access to a shared mailbox it normally appears automatically within 60 minutes after restarting Outlook. If it does not, add it manually: File > Account Settings > Account Settings > Change > More Settings > Advanced > Add, then type the mailbox name.
Access to shared mailboxes is requested through the Access Portal and must be approved by the mailbox owner.
