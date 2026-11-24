---
id: KB-005
title: Printing at Acme offices (Follow-Me printing)
category: Printer
last_updated: 2026-03-02
---

## How office printing works
All office printers use Follow-Me printing. You send your document to a single queue and release it at any printer by tapping your ID badge. Jobs not released within 24 hours are deleted.

## Adding the printer to your laptop
1. Connect to the office network or VPN.
2. Open File Explorer and type `\\print01.acme.local` in the address bar.
3. Double-click **FollowMe-Mono** (black and white) or **FollowMe-Colour** (colour, requires approval).
4. Print as normal, then tap your badge on any printer and choose Release.

## Printer shows offline
- Check the printer display for paper jams or errors.
- If several people are affected, raise a ticket with the printer name (on the label, e.g. PRN-3F-01).
- If only you are affected, remove and re-add the FollowMe queue.

## Jobs stuck in queue
1. Open Services (services.msc) and stop the **Print Spooler** service.
2. Delete the files in `C:\Windows\System32\spool\PRINTERS`.
3. Start the Print Spooler service again.
If you do not have admin rights, the Service Desk can do this remotely.

## Toner and paper
Toner is replaced automatically by the print vendor. Paper is stocked by Facilities; report shortages via the Facilities portal, not IT.
