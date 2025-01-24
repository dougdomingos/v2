+++
title = "My First Thoughts on Fedora Linux"
date = "2025-01-04T00:32:27-03:00"
author = "Douglas Domingos"
tags = ["linux", "opinion"]
keywords = ["linux", "fedora", "ubuntu"]
description = "After three years on Ubuntu-based distributions, I've decided to migrate to Fedora 41, for no reason besides pure curiosity. And so far, I have no plans of coming back."
showFullContent = false
readingTime = true
hideComments = false
+++

## Introduction

Since my first contact using Linux back in 2020, I've tried out many distributions, such as
**Ubuntu**, **Linux Mint**, **Kubuntu**, and most recently **Pop!\_OS**. But, as you may already
known, these are all **Debian-based distributions**, so aside from graphical interfaces, **they
function in the exact same way**.

Having expanded my knowledge in Linux throughout the last year, I now feel confortable enough to
tweak with more **cutting-edge systems**. My first idea was to try **Manjaro KDE**, as Arch-based
distributions seemed quite interesting. Yet, after playing around with **Fedora** through LiveUSB,
I've decided to stick around with it for now.

The opinions shared in this post are based on the following use cases:

- **Software Development**, mainly in **Java**, **JavaScript** and **Python** environments
- **Casual tasks and applications** (e.g. music and video streaming, web browsing, etc.)
- **Gaming** (i.e. lightweight games via **SteamOS** and **Proton**)

I've also considered the **opinions of other users** posted on the Reddit community
[r/Fedora](https://www.reddit.com/r/Fedora/), which **I recommend you to follow** for
troubleshooting and customizing configurations.

## The first contact

Something noticeable even _before_ installing Fedora is that it's very **lightweight** - it's
shipped only with **Firefox**, **LibreOffice Suite**, and basic applications/utilities. This also
applies for **GNOME Shell**, **the graphical interface of Fedora Workstation**, which offers a
**pure, vanilla experience**. Sure, finding and testing GNOME extensions for **basic
funcionalities** (e.g. adding app shortcuts to the desktop) is quite **annoying**, but it's a
classic "install and forget" type of job.

The _real_ deal-maker for me was **the package repositories**: many of the softwares I use are
avaliable in DNF with **more recent versions** than those in APT-based distributions. Also, Fedora
comes with **Flatpak** pre-installed, only requiring you to **add the FlatHub repositories** before
installing software.

However, not everything is perfect: Fedora's preference for **open-source software** means that you
may need to **manually install proprietary drivers**, such as those for **Nvidia GPUs**, and **media
codecs** like H.264. Fortunately, most of these **can be found in RPMFusion** - Fedora's third-party
repository. So far, I only had to install a few **video codecs for VLC**, without any struggles with
hardware compatibility. Therefore, your experience with Fedora may vary, depending on **your
hardware specifications** and **which programs you use**.

## Software compatibility

One of my biggest **concerns** when moving away from **Pop!\_OS** was that some applications I use
**wouldn't be compatible**, without any satisfactory alternatives. Thankfully, **this was not the
case**, as Fedora's repositories **provided pretty much all the packages** I needed. But again, for
**third-party packages** and **proprietary software**, you may have to **reach out for RPMFusion**,
which is very easy to setup and use.

On the rare ocasions where the softwares you need is **not within Fedora's repositories nor
RPMFusion**, you can also use **Flatpak** - a package manager that allows you to **install and
execute containerized applications**, keeping their dependencies separate from the system. **I
personally prefer flatpaks** over native packages, though I've seen **many users recommend the
opposite**.

The _only_ cases I believe you may have to **opt for alternatives** are for packages and
applications **distributed only through Snap or PPAs**. For Snap, however, it's probable that you'll
find your software within Flatpak or RPM repositories, which was my case for **Hugo SSG** - the
framework used in this website, distributed in Fedora through DNF.

## Support and resources

It's important to highlight that **Fedora has far less online resources** when compared to
Ubuntu/Debian distributions, which means that you may have **difficulties finding solutions** for
technical problems, specially if you have **little experience with Linux**.

Despite that, I've found Fedora to be **very similar in usability** with Ubuntu distributions so
far. **The most noticeable difference** between the platforms are **the package repositories**, as
Fedora (and RedHat Linux distributions) enphatizes the **adoption of Open-Source software**, and
thus requires add some **overhead configuration to allow proprietary packages** - which are easily
set with only two commands in your terminal.

Although Fedora has proved to be **stable and easy to use** up until now, **I'd still recommend
Debian-based distributions** for those who have no experience in Linux, or simply have no time to
spare on debugging configurations.

## TL\;DR

With my current experience, Fedora stands out on the following:

- Offers **a true vanilla GNOME experience**, leaving all customizations for the users
- Allows users to choose whether to **install proprietary software** (through RPMFusion) or not
- Packages within RPM repositories are offered in **more recent versions** than in APT

However, I see some possible drawbacks of this migration:

- Being a cutting-edge distribution, Fedora may be **less stable than Ubuntu**
- Specific applications **may not be available** for Fedora
- Potential **reduced compatibility** with older hardware (based on some reports from other users)

Some of this aspects may change as my experience with Fedora evolves, so expect updates in the
future.
