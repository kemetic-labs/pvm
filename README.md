# PVM: PHP Version Manager

[![Release](https://img.shields.io/github/v/release/kemetic-labs/pvm)](https://img.shields.io/github/v/release/kemetic-labs/pvm)
[![Build status](https://img.shields.io/github/actions/workflow/status/kemetic-labs/pvm/main.yml?branch=main)](https://github.com/kemetic-labs/pvm/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/kemetic-labs/pvm/branch/main/graph/badge.svg)](https://codecov.io/gh/kemetic-labs/pvm)
[![License](https://img.shields.io/github/license/kemetic-labs/pvm)](https://img.shields.io/github/license/kemetic-labs/pvm)

A lightweight, deterministic PHP version manager for Unix-like systems.

## Features
- Clean, reproducible builds for every PHP version.
- Simple CLI: install, use, and manage PHP versions.
- Minimal dependencies, no bloat.

## Getting Started

### 1. Installation

For detailed instructions on installing prerequisites and `pvm` itself, please see the **[Installation Guide (INSTALL.md)](INSTALL.md)**.

### 2. Basic Usage

Once installed, you can manage PHP versions with ease:

```sh
# list available releases (not the full list for brevity, it just shows the latest of each minor version of PHP, you can still install any available version, it checks by tag on php-src)
pvm releases

# install a version you need
pvm install 8.3.8

# load it in the current shell session (you can also use direnv to automatically load it in every shell session)
pvm use 8.3.8

php -v

For more real-world usage examples, see:
- [Simple PHP Setup](recipes/1_simple_setup.md)
- [Minimal PHP CLI](recipes/2_minimal_php_cli.md)
- [PHP with Debug and ZTS](recipes/3_php_debug_zts.md)
- [All Recipes](recipes/)
