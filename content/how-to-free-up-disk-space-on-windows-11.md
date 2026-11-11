---
title: "How to Free Up Disk Space on Windows 11: 10 Safe Ways to Reclaim Gigabytes"
seo_title: "How to Free Up Disk Space on Windows 11: 10 Safe Methods"
description: C drive full on Windows 11? Free up disk space safely with Storage Sense, cleanup recommendations, temp files, hibernation and big-file hunting, step by step.
category: tech
lang: en
translation: comment-liberer-de-l-espace-sur-un-pc-windows
date: 2026-11-11T08:00:00+01:00
tags: Windows 11, disk space, Storage Sense, C drive full, PC cleanup
---
To free up disk space on Windows 11, start with **Settings > System > Storage**: delete **temporary files**, turn on **Storage Sense** and follow the **cleanup recommendations**. Then hunt for **large files** in Downloads and old videos, uninstall unused apps and games, and move photos to an external drive or the cloud. These steps usually recover anywhere from a few gigabytes to tens of gigabytes without any risk to Windows.

## First, see what is using the space

Open **Settings > System > Storage**. Windows shows a breakdown of your C: drive by category: **Apps & features, Temporary files, Documents, Pictures, Videos, Other**... Click **Show more categories** to see everything.

This view tells you where to act. For example:

- **Temporary files at 15 GB**: easy win, see method 1.
- **Apps at 120 GB**: games are probably the culprit, see method 5.
- **Other at 60 GB**: often caches, virtual machines or folders created by specific programs.

A rule of thumb: keep at least **10 to 15% of the drive free**. Below that, Windows updates can fail and the PC slows down.

## Method 1: delete temporary files

1. In **Settings > System > Storage**, click **Temporary files**.
2. Windows scans and lists categories: Windows Update Cleanup, Delivery Optimization files, thumbnails, Recycle Bin, Downloads...
3. **Untick "Downloads"** unless you have checked that folder: it contains your downloaded files, not junk.
4. Click **Remove files**.

**Windows Update Cleanup** and **Previous Windows installation(s)** can weigh several gigabytes each. Removing the previous installation means you can no longer roll back to the previous version of Windows, so only do it once you are sure the update works well.

## Method 2: use the cleanup recommendations

Still in **Settings > System > Storage**, open **Cleanup recommendations** (under Storage management). Windows suggests:

- **Large or unused files** that you have not opened for a long time;
- **Files synced to the cloud** that can be made online-only;
- **Unused apps**.

Review each list before deleting. It is a quick way to spot a forgotten 8 GB video or an old installer.

## Method 3: turn on Storage Sense

**Storage Sense** cleans automatically in the background.

1. Go to **Settings > System > Storage > Storage Sense**.
2. Turn on **Automatic User content cleanup**.
3. Configure it: run when disk space is low (or every week), delete Recycle Bin files after **30 days**, and decide whether to clean the Downloads folder (set it to **Never** if you use Downloads as a working folder).
4. Click **Run Storage Sense now** for an immediate cleanup.

## Method 4: empty Downloads and find large files

The Downloads folder is often the biggest waste: installers, ISO images, ZIP archives you already extracted.

1. Open **File Explorer** and go to Downloads.
2. Switch to **Details** view and click the **Size** column to sort from largest to smallest.
3. Delete what you no longer need.

To find big files anywhere, type **size:gigantic** in the File Explorer search box on C: (it lists files over 4 GB), or **size:huge** (128 MB to 4 GB). Free tools like WizTree or WinDirStat show a visual map of the drive.

## Method 5: uninstall unused apps and games

1. Go to **Settings > Apps > Installed apps**.
2. Sort by **Size (large to small)**.
3. Click the three dots next to an app and choose **Uninstall**.

Modern games often take **50 to 150 GB each**. In Steam, Xbox or Epic, uninstalling a game you finished keeps your saves in the cloud in most cases (check before). Also remove trial software preinstalled by the manufacturer.

## Method 6: move photos and videos

Phone backups and videos fill drives quickly. Options:

- Move them to an **external hard drive** or USB stick.
- With **OneDrive**, enable **Files On-Demand**: files stay visible but only download when you open them. Right-click a folder and choose **Free up space**.

If you are unsure how to organise this, our guide on [how to back up photos from your phone](/en/how-to-back-up-photos-from-your-phone/) explains a good backup routine.

## Method 7: disable hibernation (if you don't use it)

The hibernation file **hiberfil.sys** can take several gigabytes, depending on your RAM. If you never use hibernation:

1. Open **Terminal (Admin)**.
2. Type **powercfg /hibernate off** and press Enter.

This also disables **Fast startup**, which relies on hibernation. On a laptop you rely on for hibernating, skip this method.

## Method 8: reduce restore points

System Protection keeps restore points that can take a lot of space.

1. Search for **Create a restore point** in the Start menu.
2. Select drive C: and click **Configure**.
3. Lower **Max Usage** to around 5 to 10%, or click **Delete** to remove old points (keep protection on).

## Method 9: clean browser and app caches

Browsers, Teams, Spotify, Adobe apps and game launchers store caches of several gigabytes. Clear them from each app's settings. In Chrome or Edge, press **Ctrl + Shift + Delete** and clear **cached images and files**.

## Method 10: run the classic Disk Cleanup

The old **Disk Cleanup** tool still works. Type **cleanmgr** in the Start menu, select C:, then click **Clean up system files** to include update leftovers and log files.

## What you should never delete

- The **Windows**, **Program Files** and **ProgramData** folders, or files in them by hand.
- **pagefile.sys** and **swapfile.sys**: Windows needs them.
- The **WinSxS** folder manually (use Disk Cleanup instead).
- Anything in **AppData** unless you know exactly what it is.

> **Tip:** avoid "PC cleaner" apps that promise to free 20 GB in one click. Windows' built-in tools do the same job without the risk of deleting important files or installing adware.

## Common mistakes

- Deleting the Downloads folder in Temporary files without checking it.
- Removing the previous Windows installation right after a major update.
- Filling the drive back to 99% after cleaning: set Storage Sense to run automatically.

## Summary

To free up space on Windows 11, start in **Settings > System > Storage**: remove **temporary files**, follow the **cleanup recommendations** and turn on **Storage Sense**. Then sort **Downloads** by size, uninstall **heavy games and apps**, move **photos and videos** and, if relevant, disable **hibernation**. Never delete system files by hand. If your PC is still slow after cleaning, the cause may be elsewhere: see [why your device is so slow](/en/why-is-my-phone-so-slow/) for the same diagnostic logic.
