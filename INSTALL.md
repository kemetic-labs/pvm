# PVM Installation Guide

In this guide, we'll make sure that your system is ready to use `pvm` to compile and manage PHP versions. The installation process has three steps:

1.  **Install PVM**: Installing the `pvm` application itself using `pipx`.
2.  **System Prerequisites**: Installing the necessary libraries and tools to compile PHP.
3.  **Verify Installation**: Running `pvm doctor` to verify your setup.
4. (Optional) depending on your setup you may need additional libraries to be installed. If you find a good common case, your contributions would be appreciated by the community.

---

## 1. Install PVM

If you have Python 3.9+ installed, you can install `pvm` directly using `pipx` in 1 step. if not, then please read through the next step

#### Install `pipx`:

```sh
pip3 install --user pipx
python3 -m pipx ensurepath
```

**Note:** You may need to restart your terminal after this step for the `PATH` changes to take effect.

#### Install PVM

```sh
pipx install 'git+https://github.com/kemetic-labs/pvm.git'
```

---

## 2. System Dependencies

In order to build php from the source, we need to install some dependencies, covered next

### For Debian / Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv build-essential autoconf \
  bison re2c pkg-config libxml2-dev libsqlite3-dev libssl-dev \
  libcurl4-openssl-dev libonig-dev libzip-dev libreadline-dev \
  libicu-dev libjpeg-dev libpng-dev libxslt1-dev libffi-dev zlib1g-dev
```

### For Fedora / CentOS / AlmaLinux

First, install `pipx` dependencies and the PHP build tools:

```bash
sudo dnf install -y python3-pip gcc gcc-c++ make autoconf bison re2c \
  pkg-config libxml2-devel sqlite-devel openssl-devel libcurl-devel \
  oniguruma-devel libzip-devel readline-devel libicu-devel \
  libjpeg-turbo-devel libpng-devel libxslt-devel libffi-devel zlib-devel
```

### For macOS

On macOS, we will use [Homebrew](https://brew.sh) to manage packages.

**A. Install Xcode Command Line Tools**

If you haven't already, install Apple's command line tools, which provide the core compilers.

```bash
xcode-select --install
```

**B. Install Homebrew & Dependencies**

If you don't have Homebrew, install it from [brew.sh](https://brew.sh). Then, install all required dependencies with a single command:

```bash
brew install python autoconf bison re2c pkg-config libxml2 sqlite openssl \
  curl oniguruma libzip readline icu4c jpeg-turbo libpng libxslt libffi
```

-----

## 3. Verify Installation

After installing PVM and the system prerequisites, verify your setup by running:

```sh
pvm doctor
```

This command will check if all required dependencies are installed correctly. and will report if the dependencies are installed with their expected version specifications.

If all is well, you should see something like

```
 pvm doctor

Dependency Check:
  bison      3.8.2           OK (required: 3.0+)
  autoconf   2.72            OK (required: 2.68+)
  re2c       4.2             OK (required: 1.0.3+ (PHP 8.3+), 0.13.4+ (PHP 8.2 and earlier))

All required dependencies are present.
```

Now we are ready to install our first version. Head to the [Getting Started section in the README.md](README.md#getting-started) to learn how to install and use PHP versions.
