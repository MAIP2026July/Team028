---
id: KB-001
title: Troubleshooting the Acme VPN client
category: VPN
last_updated: 2026-06-15
---

## Overview
The Acme VPN client gives remote access to internal applications (intranet, HR portal, file shares). It supports Windows 11 and macOS 13+. You must use MFA every time you connect.

## VPN will not connect
1. Check you have internet access by opening a public website.
2. Make sure your laptop clock is correct; a wrong time breaks certificate checks.
3. Restart the VPN client (right-click tray icon > Exit, then reopen).
4. If you see "Authentication failed (691)", your saved password is probably out of date. Go to Settings > Account > Forget saved credentials and sign in again.
5. Hotel or airport Wi-Fi may need you to accept a captive portal page first. Open a browser before connecting VPN.

## VPN keeps disconnecting
- Many home routers close idle UDP sessions. Switch the protocol to TCP: Settings > Connection > Protocol > TCP.
- Disable Wi-Fi adapter power saving: Device Manager > Network adapters > your Wi-Fi adapter > Power Management > untick "Allow the computer to turn off this device".
- Avoid using mobile hotspots with weak signal; prefer a wired connection for long sessions.

## Connected but internal sites do not load
- Run `ipconfig /flushdns` in Command Prompt, then reconnect the VPN.
- Check that `nslookup intranet.acme.local` returns a 10.x.x.x address. If it returns nothing, DNS is going through your home router - reconnect, or contact the Service Desk.
- Acme VPN uses split tunnelling: only internal traffic goes through the VPN, so public websites working is expected.

## macOS specific
After installation, macOS blocks the VPN system extension. Open System Settings > Privacy & Security and click Allow next to "Acme VPN", then restart.

## When to contact the Service Desk
Raise a ticket if the steps above do not help, and include: the error message or code, time of the failure, and whether you are on home Wi-Fi, mobile hotspot or public Wi-Fi.
