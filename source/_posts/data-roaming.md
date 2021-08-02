---
title: "Data Roaming: A Portable Linux Environment for Data Science"
date: '2021-08-02'
excerpt: "When trying to fit data science in with a busy schedule of study, one often needs to work from shared university or library computers. Rather than spending the first 15 minutes of your working session reinstalling software, why not create a bootable USB stick with all your requirements ready to go?"
thumbnail: /gallery/thumbnails/data-roaming.jpg
toc: true
categories:
- [Data Science, Best Practice]
tags:
- linux
- tutorial
---

{% colorquote warning %}
This post will assume familiarity with Linux and access to an installation of any Linux distribution.
{% endcolorquote %}


## Introduction

If you are a student interested in data science, you might often find yourself working on library or university computers. Depending on the lenience of your university's IT policy, you may run into one of two issues:

1. You are unable to install any new software (such as languages, IDEs, or packages)
2. You can install software but this has to be repeated every time your log in

The first scenario makes data science work completely infeasible whereas the second is simply (though still significantly) a headache and waste of time.

When trying to think of a solution to these problems, my mind first turned to the Ubuntu Live USB image. This is an installer image for Ubuntu that can be burnt to a CD or USB stick. Not only can this be used to install Ubuntu, but it also allows you to run Ubuntu on your hardware, directly from the USB stick (hence the "Live").

This is a step in the right direction. One could use this live USB stick alongside a Bash script used to install all necessary packages and software. Still, although this no longer requires user attention, it may take a while to download and install all requirements.

Instead, it would be nice if we could perform this installation work upfront, creating a custom Ubuntu image with our requirements preinstalled. This is exactly the purpose of [Cubic](https://launchpad.net/cubic), a not-so-well-known tool for building custom Ubuntu images. It is supported by Ubuntu 18.04 and later and can be easily installed using the Aptitude package manager.


{% codeblock lang:bash %}
sudo apt-add-repository ppa:cubic-wizard/release
sudo apt update
sudo apt install --no-install-recommends cubic
{% endcodeblock %}



Cubic is fairly straight forward to use and is incredibly flexible. Below I will detail how I used it to create a simple data science environment containing the following:
- An installation of R, Python, Julia
- An installation of RStudio, VSCode, Jupyter
- An installation of Git and Solaar
- Tools needed to update the image

## Creating the Environment

### Step 1: Prerequisites

You will first need to download an Ubuntu image (as an ISO file). I went for Lubuntu due to its small footprint.

Alongside this, you will need a Bash script used to install additional functionality to the operating system. The script I used can be found [here](https://github.com/THargreaves/data-roaming/blob/master/src/recipe.sh). You can download this and modify it to meet your needs, or start from scratch. Make sure the resulting file is called `recipe.sh`.

{% colorquote warning %}
A few points to note:

- The script will be ran as root, so there is no need to use `sudo`.
- You will likely need to enable the Ubuntu Universe/Multiverse using `add-apt-repository universe`/`add-apt-repository multiverse`.
- Make sure to install Cubic and UNetbootin (bottom of the script) if you want to update the environment directly from the live boot.
{% endcolorquote %}


With these two files, you can start creating your custom image.

### Step 2: Creating the Image

Start by opening Cubic and selecting a directory to store the project files (you'll need to remember this for later). Next, load the Ubuntu ISO as the original disk image. You may wish to change the details of the custom disk (these are aesthetic only).

Once the disk has been analysed, a virtual environment will launch. From here `cd` into `/etc/skel`. This is the skeleton folder, used to populate new users' home folders. Create a new directory with `mkdir -p Desktop/src` and `cd` into this. 

Use the copy dialogue located in the top-left of the window to copy your ISO and `recipe.sh` into the working directory of the virtual environment. Add execute permissions to the recipe file with `chmod +x recipe.sh` and run it with `./recipe.sh`.

This will install all requirements specified in the recipe file. Once this is complete, press next to create the image, optionally selecting any additional packages to be installed from the Ubuntu defaults. Leave all other parameters as their defaults.

### Step 3: Burning the Image

Once the disk image is created you can burn it to a USB stick.

First, you will need to format your USB stick appropriately. This is best done using GParted. You will need to create 3 partitions in either EXT4 or FAT-32 format called `OS`, `DEV` and `DATA` respectively. I would advise using FAT-32 so the data partition is readable by Windows.

Now you can use UNetBootin to burn the ISO file created by Cubic onto the `OS` partition of the USB stick.

### Step 4: Running the Environment

You are now good to go. Plug the USB stick into university computer and go to the boot menu (usually `F2`, `F10` or `F12`). From here, you can select the `OS` partition to boot from.

## Updating the Environment

You cannot make permanent changes to the environment whilst running it (although you can still install new software as you normally would on Ubuntu, just with no persistence between boots). This is why we have created a secondary `DEV` partition. Using the `OS` partition, you can modify the recipe file and use the included Cubic and UNetBootin installations to create an updated image to burn to the `DEV` partition. Once you are happy with the changes, use the `DEV` partition to burn the new image to the main `OS` partition.
