---
title: "How to Restore a Crypto Wallet with a Seed Phrase, Step by Step"
seo_title: "How to Restore a Crypto Wallet with a Seed Phrase Safely"
description: Lost your phone or hardware wallet? Learn how to restore a crypto wallet with your 12 or 24-word seed phrase, fix missing balances and avoid recovery scams.
category: crypto
lang: en
date: 2026-11-11T19:00:00+01:00
tags: seed phrase, recovery phrase, crypto wallet, restore wallet, crypto security
---
To restore a crypto wallet with a seed phrase, install a **compatible wallet app or set up a hardware wallet**, choose **"Restore" or "Import existing wallet"**, enter your **12 or 24 words in the exact order**, add your **passphrase** if you set one, and set a new PIN. Your funds reappear because they were never stored in the device, but **on the blockchain**: the seed phrase simply regenerates your private keys. If the balance shows zero, it is usually a **derivation path, network or passphrase** issue, not lost funds.

## How a seed phrase works

A **seed phrase** (also called recovery phrase or mnemonic phrase) is a list of **12, 18 or 24 words** taken from a standard list of 2,048 English words defined by **BIP39**. These words encode a master key from which the wallet derives all your private keys and addresses.

Key points to understand:

- The phrase **is** your wallet. Anyone who has it can take your funds, from anywhere in the world.
- The **order** of the words matters.
- Most wallets follow the same standards (BIP39, BIP32, BIP44 and related), so a phrase created in one wallet can **usually be restored in another**.
- A wallet app or a hardware device is just an interface. If it breaks or gets lost, your coins are still on the blockchain. Our guide on [what a crypto wallet is](/en/what-is-a-crypto-wallet/) explains this in more detail.

## Before you start: security checks

1. **Use a trusted device** free of malware. Avoid public or shared computers.
2. **Download the wallet only from the official source**: the official website or the official app store listing, checking the developer name. Fake wallet apps are a common way to steal seed phrases.
3. If you have significant funds, prefer restoring on a **hardware wallet**: the phrase is entered on the device itself, never on a connected computer.
4. **Never type your seed phrase on a website**, in a form, in an email or in a chat, and never give it to "support". No legitimate company will ever ask for it.

## Step-by-step: restore on a software wallet (phone or computer)

The wording varies slightly, but the process is the same in most apps:

1. Install the wallet from its official source.
2. On the welcome screen, choose **"I already have a wallet"**, **"Import wallet"** or **"Restore from recovery phrase"**. Do not choose "Create new wallet".
3. Select the **number of words** (12 or 24) if asked.
4. Enter each word **in order**. Most apps suggest words as you type: since all BIP39 words are unique in their first 4 letters, auto-complete helps avoid typos.
5. If you had set an **optional passphrase** (sometimes called the "25th word"), enter it exactly, including upper and lower case.
6. Create a new **PIN or password** for the app. This is local to the device and different from the seed phrase.
7. Wait for the wallet to **sync** with the blockchain. It may take a few seconds to several minutes.

## Step-by-step: restore on a hardware wallet

1. Unpack a **new or reset** hardware wallet bought from the manufacturer or an authorised reseller.
2. Connect it to the official companion app.
3. On the device, choose **"Restore from recovery phrase"** (or "Recover wallet").
4. Enter the words **on the device itself** using its buttons or touchscreen.
5. Set a PIN and, if you used one, the passphrase.
6. Add the accounts for each coin in the companion app.

## My balance shows zero: what to check

Don't panic. In most cases the funds are there but the wallet is not looking in the right place.

### 1. The wrong network or coin

If you held **tokens on Ethereum, Polygon, Arbitrum or BNB Chain**, the same address exists on all these networks. Switch networks or **add the custom token** in the app to see it.

### 2. A different derivation path

Wallets can generate addresses along different **derivation paths**. For Bitcoin, for example, there are several address types: legacy (starting with 1), nested SegWit (starting with 3), native SegWit (bc1q) and Taproot (bc1p). If your old wallet used one type and the new one shows another by default, you will see an empty balance. Look for an option to **add an account of a different type** or to change the derivation path in the advanced settings.

### 3. The passphrase

A different passphrase, even one character off, opens a **completely different, empty wallet**. Check capital letters, spaces and special characters.

### 4. Not all accounts were scanned

Some wallets only show the first account. If you used several accounts, add them manually (Account 2, Account 3...).

### 5. Wallets that do not use standard BIP39

A few older or specific wallets use their **own format** (for example, some early Electrum seeds or certain blockchain-specific wallets). You may need to restore in the **same wallet software** that created the phrase.

You can check your balance without restoring anything by pasting your **public address** (never the seed) into a **block explorer** for the right blockchain.

## If a word is missing or wrong

- **One word missing or misspelled**: the last word contains a **checksum**, so most apps reject invalid phrases. Check each word against the official BIP39 word list.
- **Words in the wrong order**: try to find your original backup. Brute-forcing the order of 12 words is not realistic without a strong clue.
- **Forgotten passphrase**: there is no reset. Without it, the funds protected by it cannot be recovered.

Beware of **"crypto recovery services"** that promise to recover funds or phrases: many are scams targeting desperate owners.

## After restoring: secure everything again

- If you restored because your device was **stolen**, or you suspect your phrase was **exposed**, the phrase is compromised. Create a **new wallet with a new seed phrase** and **transfer all funds** to it right away.
- Store the seed phrase **offline**: written on paper or engraved on a metal plate, in a safe place. Never as a photo, cloud note or screenshot.
- Consider keeping **two copies in different locations**.
- Protect the app and your accounts with a [strong password](/en/how-to-create-a-strong-password/) and two-factor authentication on exchanges.
- If you used staking, check that your positions are still there: see [what crypto staking is](/en/what-is-crypto-staking/).

## Common mistakes

- Typing the phrase on a website claiming to "validate" or "sync" a wallet: this is always a scam.
- Downloading a fake wallet app from an ad.
- Concluding funds are lost because the first screen shows zero.
- Keeping using a seed phrase that has been exposed.

## Summary

To restore a crypto wallet, install an **official wallet app or hardware wallet**, choose **Restore**, enter your **12 or 24 words in order** and your **passphrase** if any. If the balance is empty, check the **network, address type, derivation path, passphrase and accounts**. Never share your seed phrase, and if it may have been exposed, **move your funds to a new wallet** immediately.
