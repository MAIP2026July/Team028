---
id: KB-007
title: Microsoft Teams audio, video and presence issues
category: Teams & Collaboration
last_updated: 2026-06-20
---

## Camera not working in Teams
1. Check the camera works in the Windows Camera app.
2. Go to Windows Settings > Privacy & security > Camera and turn on both "Camera access" and "Let desktop apps access your camera".
3. In Teams, open Settings > Devices and pick the correct camera.
4. Close other apps that may be using the camera (Zoom, browser tabs).

## Echo or poor audio
- Use the company headset rather than laptop speakers.
- Make sure the same device is selected as both speaker and microphone in Teams > Settings > Devices.
- Run a test call (Settings > Devices > Make a test call).
- On VPN, Teams media traffic bypasses the tunnel; if calls are choppy, check your home internet speed first.

## Presence shows "Away"
Teams sets you to Away after 5 minutes of inactivity or when your computer is locked. This is expected. You can set a fixed status with a duration (click your picture > status > Duration).

## Clearing the Teams cache
If Teams behaves oddly (blank screens, missing chats), quit Teams, delete the contents of `%LocalAppData%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams`, and restart Teams.
