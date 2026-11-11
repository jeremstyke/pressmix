---
title: "Wi-Fi Connected but No Internet on Windows: 9 Fixes in the Right Order"
seo_title: "Wi-Fi Connected but No Internet on Windows 11: 9 Fixes"
description: Windows says Wi-Fi is connected but there's no internet? Try these 9 fixes in order, from restarting the router to renewing your IP and changing DNS.
category: tech
lang: en
translation: wifi-connecte-mais-pas-d-internet-windows
date: 2026-11-11T07:00:00+01:00
tags: Windows 11, Wi-Fi, no internet, DNS, network reset
---
When Windows shows **"Connected, no internet"** (or "No internet, secured"), your PC is talking to the router, but something is blocking the path between the router and the internet, or Windows is not getting the right settings from the router. In most cases, **restarting the router**, **renewing your IP address** or **changing your DNS server** fixes it. Here are 9 fixes to try in order, from the quickest to the most advanced.

## Step 0: find out where the problem is

Before touching any setting, spend one minute narrowing it down:

- **Do other devices have internet on the same Wi-Fi?** If your phone has no internet either, the problem is the router or your provider, not Windows. Go to fix 1.
- **Do other devices work fine?** Then the problem is on your PC. Skip to fix 3.
- **Does the PC work on another network**, such as your phone's hotspot? If yes, the PC is fine and the issue is specific to your home network settings.

This simple test saves a lot of time.

## Fix 1: restart the router properly

1. Unplug the router (and the modem, if it is a separate box) from the power.
2. Wait **30 seconds**.
3. Plug the modem back in first, wait until its lights are stable, then the router.
4. Wait 2 to 3 minutes before testing.

Check the router's status light. A red or orange "internet" light usually means an **outage on your provider's side**: check their status page or app from your phone's mobile data.

## Fix 2: check for a captive portal or a data cap

On hotel, airport, train or café Wi-Fi, "no internet" often means you have not **accepted the login page**. Open a browser and go to a simple HTTP site like **http://neverssl.com** to trigger the portal. On some mobile plans or prepaid boxes, an expired data allowance has the same symptom.

## Fix 3: forget the network and reconnect

1. Open **Settings > Network & internet > Wi-Fi > Manage known networks**.
2. Click your network and choose **Forget**.
3. Reconnect and type the Wi-Fi password again.

This clears a corrupted profile, which happens after a router change or a password change.

## Fix 4: run the network troubleshooter

In Windows 11, go to **Settings > System > Troubleshoot > Other troubleshooters** and run the **Network and Internet** troubleshooter (depending on your version, it may open in the Get Help app). It automatically resets the adapter and checks the most common settings. It does not always find the cause, but it takes two minutes.

## Fix 5: renew your IP address and flush DNS

A bad IP address (often starting with **169.254**, which means Windows did not get an address from the router) is a classic cause.

Right-click the Start button and open **Terminal (Admin)** or **Command Prompt (Admin)**, then type these commands one by one, pressing Enter after each:

- **ipconfig /release**
- **ipconfig /renew**
- **ipconfig /flushdns**

Finally, type **ipconfig** and check the **IPv4 address**. Something like **192.168.1.25** is normal. If it still starts with 169.254, the router's DHCP is not answering: restart the router again or check that it is not full (some routers limit connected devices).

## Fix 6: change your DNS server

If sites do not load but apps like Teams or games still connect, the problem is often **DNS** (the system that converts site names into addresses). Your provider's DNS can be slow or down.

1. Go to **Settings > Network & internet > Wi-Fi > [your network] > Hardware properties**.
2. Next to **DNS server assignment**, click **Edit** and choose **Manual**.
3. Turn on **IPv4** and enter a public DNS, for example Cloudflare (**1.1.1.1** and **1.0.0.1**) or Google (**8.8.8.8** and **8.8.4.4**).
4. Save and test.

Quick test from the command line: **ping 8.8.8.8** works but **ping google.com** fails? That confirms a DNS problem.

## Fix 7: disable VPN, proxy and security tools

- **VPN**: disconnect it or uninstall it temporarily. A VPN that crashed can leave Windows without a route to the internet.
- **Proxy**: go to **Settings > Network & internet > Proxy** and make sure "Use a proxy server" is off unless your company requires it.
- **Third-party antivirus or firewall**: pause it for a minute to test. If the internet comes back, update or reinstall it.

## Fix 8: update or roll back the Wi-Fi driver

1. Right-click Start and open **Device Manager**.
2. Expand **Network adapters**, right-click your Wi-Fi card (Intel, Realtek, MediaTek, Qualcomm...).
3. Choose **Update driver**, or if the problem started after a Windows update, open **Properties > Driver > Roll Back Driver**.
4. You can also choose **Uninstall device**, then restart: Windows reinstalls the driver automatically.

Also check **Power management** in the adapter's properties and untick "Allow the computer to turn off this device to save power" if the connection drops after sleep.

## Fix 9: reset the network stack

This is the last resort. It removes all network adapters and puts settings back to default (you will need to reconnect to Wi-Fi and reinstall VPN software).

1. Open **Settings > Network & internet > Advanced network settings > Network reset**.
2. Click **Reset now** and confirm.
3. The PC restarts after about 5 minutes.

Command-line equivalent, in an admin terminal:

- **netsh winsock reset**
- **netsh int ip reset**

Then restart the PC.

## Special cases

- **Only one site does not work**: the problem is the site, not your connection. Try another browser or check a down-detector site.
- **It happens after sleep**: disable power saving on the adapter (fix 8) and turn off **Fast startup** in Control Panel > Power Options.
- **Works on 2.4 GHz but not 5 GHz**: your adapter may not support the channel your router uses. Set a fixed channel (36 to 48) in the router settings.
- **Ethernet works, Wi-Fi does not**: the problem is the Wi-Fi driver or adapter, not your provider.

## Common mistakes

- Resetting the router to factory settings first: you will lose your configuration for a problem that a simple restart often fixes.
- Changing several settings at once: you will not know which one worked.
- Forgetting a VPN running in the background.

## Summary

"Connected, no internet" means the PC reaches the router but not the internet. Check whether **other devices** are affected, **restart the router**, then on the PC **forget the network**, **renew the IP and flush DNS**, **switch to a public DNS**, turn off any **VPN or proxy**, update the **driver**, and use **Network reset** as a last resort. If your connection works but feels sluggish, see [why your phone is so slow](/en/why-is-my-phone-so-slow/) or [how to fix lag in online games](/en/how-to-fix-lag-in-online-games/). And while you are in the router settings, make sure the Wi-Fi uses a [strong password](/en/how-to-create-a-strong-password/).
