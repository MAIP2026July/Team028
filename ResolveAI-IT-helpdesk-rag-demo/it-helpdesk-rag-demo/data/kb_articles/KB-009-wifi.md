---
id: KB-009
title: Office Wi-Fi networks and connection problems
category: Network & Wi-Fi
last_updated: 2026-02-14
---

## Networks
- **Acme-Corp**: for company laptops only. Connects automatically using the laptop's machine certificate (802.1X). No password needed.
- **Acme-Guest**: internet-only network for visitors and personal devices. Requires a guest pass.

## Connected but "No internet"
This usually means the laptop's certificate has expired or has not been issued, and the network has placed the device in quarantine.
1. Connect with a network cable at a desk, or connect to VPN from another network.
2. Open Command Prompt and run `gpupdate /force` and then `certutil -pulse`.
3. Restart the laptop.
If it still fails, raise a ticket with your laptop's asset tag.

## Guest access
Any employee can create a guest pass at the Guest Wi-Fi portal. Passes last 24 hours (maximum 5 days for longer visits). Personal phones should also use Acme-Guest.

## Slow Wi-Fi
Move closer to an access point, avoid crowded meeting rooms during all-hands, and prefer the 5 GHz band. For large downloads, use a wired connection.
