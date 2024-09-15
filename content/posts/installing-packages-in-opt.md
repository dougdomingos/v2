+++
title = "How to globally install packages in `/opt` directory on Linux"
date = "2024-09-15T13:34:18-03:00"
author = "Douglas Domingos"
tags = ["linux", "tutorial", "utility"]
keywords = ["linux", "packages", "software", "sysadmin"]
description = "Installing software in Linux may be tricky sometimes, especially when dealing with packaged files like .zip or .tar.gz. But with this simple guide, solving situations like these will be as easy as moving files between directories (literally)."
showFullContent = false
readingTime = true
hideComments = false
+++

## Introduction

If you're an avid Linux user, it's very likely that you have found yourself in one of the
following situations:

- You needed to **install the most recent version** of a package, but the **package
  mananger of your distribution only had an older version** of it

- You wanted to **install a software**, but **no installer was provided**, or **it wasn't
  avaliable** in your package manager

- You wanted to build a script to **automate the installation** of a package for **all
  users of a system**, but you wasn't sure of **where to save the package** nor **how to
  make it avaliable globally**

If you've had scenarios like these, or you only want to learn something new, stick
around. I got the solution for you.

## A little of Linux file system

You might not know, but each directory in the root of your Linux file system is used to
**store certain files and directories**. Knowing at least a few of them and their
purpose might prove useful in situations like this.

In this scenario, we're gonna focus on three of those directories:

- `/opt`: Stores **third-party software** that is not part of your Linux distribution
- `/etc`: Stores **system-wide configuration files**
- `/usr`: Contains **system commands** and **files required to run installed software**

At this point, you've probably figured out that we're installing our precious packages
in the `/opt` directory.

## `/opt`, the home for your third-party packages

To keep your system organized (and, thus, less prone to breaking out of nowhere),
create a new directory inside `/opt` for your package before saving its file. I recommend
creating a directory with the same name of the package, making it easy to find
afterwards.

Now, you've pretty much done more than half of the work needed to conclude the
installation. If you take a look inside the package directory, you'll probally find a
`/bin` directory. That's where the files you use to actually run the software lives in.
At this point, you can start your apps through the terminal

> *"Cool, but how do I make my software avaliable throughout the whole system?"*

Here's where we make the magic: you only need to add the executable files to your `$PATH`
variable. But how to do it? That's where the `/etc` and `/usr` directories come in.

## Adding your package binaries to `$PATH`

There are two ways of achieving this: the easy and quick way and the risky way.

### 1. EASY: The power of *Symlinks*

Here, all you have to do is **create a symlink to the executable file inside the `/bin`
directory** of your package. The symlink will live inside the `/usr/local/bin`
directory.

> **What are symlinks?**  
> *Links* are special files that "point" to other files. Linux offers support for two
> types of links:
>
> - **Hard links**: a file that points to the data of another file
> - **Soft links**: a file that points to another file or directory
>
> When using links, you'll probably want to use **soft links**, as they're easier to
> manage and more flexible than **hard links**. If you want to learn more about symlinks
> in Linux, give [this article](https://www.redhat.com/sysadmin/linking-linux-explained)
> a read.

To create a symlink, head to your terminal and simply run the following command:

```bash
ln -s /opt/<your_package_dir>/bin/<executable_filename> /usr/local/bin/<executable_filename>
```

This will make the executable avaliable globally in the system, for both users or
scripts.

- Pros: easy to setup, avoid tweaking with `$PATH` configuration
- Cons: can only setup one executable per link

> **Note**: You may **setup the symlink to the package's `/bin` directory** instead of only
> one executable, but you'll have to **specify the executable** when running it with Bash
> (e.g. `test/exec1` instead of simply `exec1`)

### 2. RISKY: The `$PATH` of all things

This is a more complete (but somewhat risky) way of setting up your package globally.
We'll make use of `/etc` directory to **store some configuration files** for our package.
I'm assuming you have basic command-line knowledge, so let's get to it, step by step:

1. Open a terminal window and head to the `/etc` directory

2. Create a new file with the name of your package followed by a `rc` suffix
   (e.g. `vi /etc/myprogramrc`)

3. Add the following code to the file:

    ```bash
    export PACKAGE_HOME=/opt/<your_package_dir>
    export PATH=$PACKAGE_HOME/bin:$PATH
    ```

4. Now, create a new shellscript (e.g. `config-package.sh`) file in `/etc/profile.d/`
   and paste the following code:

    ```bash
    # Load configuration for package <package_name>
    [ -f /etc/<your_config_file> ] && . /etc/<your_etc_file>
    ```

This will effectivelly **load your configuration every time a user logs in** the system.

- Pros: **all executables inside the `/bin` directory** of the package will be loaded
- Cons: executables may not be avaliable for **scripts that do not load `/etc/profile`
  configurations**. You also may **mess up your `$PATH` variable** if not being careful

> **What is `/etc/profile*` used for?**  
> The `/etc/profile` file and `/etc/profile.d` directory **contains variables and
> configurations that are loaded in the user's shell at login**. It's useful to load
> common configurations for all users. If you intend to use these files to
> load another configurations beyond this guide, I recommend **creating a new file
> inside `/etc/profile.d`** to avoid messing up existent configurations.

## Summary

- Store your softwares in `/opt` for easy access throughout all the system
- Use symlinks for quickly setting up single executables for all users
- Create a configuration file in `/etc/` directory and add it to your `$PATH`
  variable if you need to setup multiple executables at once

## Conclusion

Phew. That was quite a lot. Linux might look a bit frightening at first, but once
you learn how to properly use it, it becomes a powerful tool, or maybe just another
reason for you to brag about what an IT genius you are (not me, I'm far from it,
actually).

That's it. I hope this article was helpful and that you have learned something useful
from it. 'Til next time!
