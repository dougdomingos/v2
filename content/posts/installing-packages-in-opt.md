+++
title = 'Installing software in Linux, the "hard" way'
date = "2024-09-15T13:34:18-03:00"
author = "Douglas Domingos"
tags = ["linux", "tutorial", "sysadmin"]
keywords = ["linux", "tutorial", "sysadmin"]
description = "When package managers aren't enough for your needs, you might need to take matters into your own hands. And this is how you do it."
showFullContent = false
readingTime = true
hideComments = false
+++

## Introduction

Picture this: you're setting up the packages and tools to develop your brand new application.
Everything is going smooth, until you found out that **one of the softwares you need is only
avaliable as package of executable binaries**, without any installers and nowhere to be found
in your package managers. Seems like quite the overhead, right?

Well, not to worry! Because today we're out to get our hands dirty and learn how to install
**ANY PACKAGE** in a Linux system ‒ and you might just learn a few new tricks about Linux
along the way.

## I. Housing the package

The first step to solve our problem is to define **where the package will be stored in
our system**. In practice, you may use any directory you'd like, but to keep things
organized, let's use the `/opt` directory.

> **The `/opt` directory** is reserved for installing software and packages that
> are not part of the system's core components, i.e, **not necessary for your
> system to function** properly.
>
> When installing your package, **you should create a new directory** (preferably
> with the package name, like `/opt/<package_name>`) to **avoid mixing up files**
> of different packages.

You may have noticed that inside your package, there's a `/bin` directory that contains
some executable files. At this point, we can run these files, but we'll have to specify
the full path of the file every time.

## II. Make your package avaliable with `$PATH`

To avoid having to pass the full path of the executables each time we run the software,
we'll make use of the `$PATH` environmental variable to **specify the path of our
installation**.

> **The `$PATH` variable** is a special string variable of the shell that specifies
> a **set of directories where executable files may live**. Each directory is **delimited
> by a colon** (`:`)
>
> You may specify new directories in `$PATH` by **exporting the variable with the new
> value** (`export PATH=/new/dir/path:$PATH`).

Now, there are two ways of adding a executable to `$PATH`:

### Adding a _Symlink_ to the executables

_Symlinks_ are (roughly) **files that "point" to other file paths or directories**. This
allows us to access files accross the file system (and even other file systems), **without
specifying the full path**.

You can create new _symlinks_ using the command `ln -s TARGET LINK_NAME`, where:

- `TARGET` is the **path of the file which the _symlink_ will point to**

- `LINK_NAME` is the **path where the _symlink_ will be created**

To make it avaliable in `$PATH`, we may **create a _symlink_ inside a directory that is
already in `$PATH`**. In this case, let's use the `/usr/local/bin` directory to store our
_symlink_.

To create our _symlink_, simply run the following command:

```bash
# Replace the placeholders with the proper names of your directories/files
ln -s /opt/<package_name>/bin/<filename> /usr/local/bin/<filename>
```

Once created, the executable will be avaliable in your shell. Try it out by **typing the
name of the _symlink_ in your terminal**.

#### Trade-offs of using _symlinks_

This approach is **pretty straightforward and easy to setup**. We don't need to edit
the value of `$PATH`, thus **avoiding possible configuration errors**. Also, by placing
the _symlink_ inside `/usr/local/bin`, we make it **avaliable for all users of the
system**.

Unfortunately, there are also drawbacks. If you need to add multiple executables, you'll
need do **create one _symlink_ per executable**. You may **create a _symlink_ to the `/bin`
directory** of the package, but you'll still need to **specify the name of the
executable**.

> **Links in Linux**  
> Links are a powerful tool in Linux, allowing you to **create shortcuts between
> files and directories**, **organizing your files easily**, and much more.
> I recommend reading this [RedHat post about linking in Linux](https://www.redhat.com/sysadmin/linking-linux-explained).

### Adding the package directory to `$PATH`

If you want a more **robust solution**, you may effectivelly edit the `$PATH` variable to
**include your package directory**. For that, we'll need to **create a configuration file**
to export our updated `$PATH`.

> **The `/etc/` directory** contains configuration files of system applications, e.g.
> service management, network, SSH, and many more. Be careful when making changes to
> files here.

Similar to `/opt`, Linux also has a directory for **storing system-wide configuration files:
the `/etc` directory**. Actually, there's the `/etc/opt` directory, which is intended to
store configuration files for **applications installed in `/opt`**.

To create the configuration file, head to `/etc/opt` and create a new file, named as
`<package_name>rc`. Inside it, paste the following code and replace the placeholders
with the correspondent paths:

```bash
# Replace "PACKAGE_HOME" with the name of your package
export PACKAGE_HOME=/opt/<package_dir>
export PATH=$PACKAGE_HOME/bin:$PATH
```

To load the settings into your shell session, run `source /etc/opt/<config_file>`
and check your `$PATH` variable with `echo $PATH`. If the directory of your package is
there, your configuration file is working.

Now, you might have noticed that **the configurations aren't loaded automatically** when
you open a new terminal. To address this, simply add this configuration to one of the
following files:

```bash
# This loads "PACKAGE" into $PATH
[ -f /etc/opt/<config_file> ] && source /etc/opt/<config_file>
```

- For **only one user**, append the load configuration at the end of `~/.bashrc`

- For **all users**, create a shell script (with the `.sh` suffix) in `/etc/profile.d/`
  with the load configuration

#### Trade-offs of using `$PATH`

One advantage of this approach is that **every executable inside the `/bin` directory
will be avaliable** in your shell. Also, you may choose to **make it avaliable for
only one user or for all users**, by simply placing the load configuration in a
different file.

However, **tweaking with the `$PATH` variable may break your shell configuration**
if you're not careful enough. The same goes for editing files inside `/etc/profile.d`;
it's best to create a new file rather than edit an existing one.

## III. Updating the desktop menu (BONUS)

If you’re installing an application with a graphical interface (not CLI-based), you’ll
likely want to add it to your desktop menu for easier access. In this case, we'll need
to take an extra step.

The entries in your desktop menu are located in the `/usr/share/applications`
directory. Each application has a `.desktop` entry file, containing settings for how it
is displayed in the menu.

To add a desktop entry file for your application:

1. Create a new `.desktop` entry file with the name of your application

2. Open the file and add the following configuration, replacing the placeholders with
   the correct settings:

   ```bash
   [Desktop Entry]
   Version=1.0
   Type=Application
   Name=<APP_NAME>
   Icon=/opt/<PACKAGE_NAME>/<ICON_FILE>
   Exec="/opt/<PACKAGE_NAME>/<EXEC_FILE>" %f
   Comment=<APP_DESCRIPTION>
   Categories=<KEYWORD1;KEYWORD2;>
   ```

3. Save the file and run `sudo update-desktop-database`

Now, the application is avaliable in your app menu, without the need to start it through
the terminal.

## Summary

- Install your package in the `/opt` directory

- Use _symlinks_ or edit your `$PATH` variable to include the package executables for
  an user or all the system

- If the package is not CLI-based, add a `.desktop` entry file at
  `/usr/share/applications` to add the package to your desktop menu

## Conclusion

Although application support for Linux platforms is pretty decent today, you'll
eventually come across a situation like the one we've discussed here. Also, you can
automate this process by creating shell scripts to setup the files for you.

Well, that's it. Until next time! :wave:
