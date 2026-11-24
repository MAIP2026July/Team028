---
id: KB-003
title: Setting up and managing multi-factor authentication (MFA)
category: MFA
last_updated: 2026-06-01
---

## What MFA is used for
MFA is required for Microsoft 365, the VPN, and the Self-Service Password Reset portal. The approved method is the Microsoft Authenticator app with number matching. SMS is allowed only as a backup method.

## First-time setup
1. On your computer go to https://aka.ms/mfasetup and sign in.
2. Choose "Add sign-in method" > Authenticator app.
3. Install Microsoft Authenticator on your phone and scan the QR code.
4. Approve the test notification.
5. Add your mobile number as a backup method.

## Getting a new phone
If you still have your old phone, add the new phone at https://aka.ms/mfasetup before wiping the old one, then delete the old device from the list.
If you no longer have the old phone, contact the Service Desk. After verifying your identity (callback via your manager), they will reset your MFA methods and you will be asked to register again at next sign-in.

## Not receiving push notifications
- Make sure notifications are enabled for the Authenticator app.
- On Android, disable battery optimisation for Authenticator (Settings > Apps > Authenticator > Battery > Unrestricted).
- On iPhone, check Focus modes are not silencing the app.
- You can always open the app and use the 6-digit one-time code instead.

## Unexpected MFA prompts
If you receive an MFA prompt you did not trigger, **deny it** and report it to the Security team immediately. It may mean someone knows your password. Reset your password straight away.
