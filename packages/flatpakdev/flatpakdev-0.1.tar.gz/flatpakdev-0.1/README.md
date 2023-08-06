# FlatpakDev

This python module is an attempt to emulate ```jhbuild build``` and
```jhbuild make``` commands, but with Flatpak sandboxes.

## Install

```bash
$ pip install flatpakdev
```

## Usage

To install an application :

```bash
$ flatpakdev install sourcePath manifestPah
```

To list applications installed by flatpakdev :

```bash
$ flatpakdev list
```

To enter a sandbox :

```bash
$ flatpakdev enter name
```

## Inside the sandbox

Inside the sandbox you will only have access to the source code directory, unless
other directories were specified in the flatpak manifest.

To use this tool inside a sandbox environment it should be installed in the
sdk, or specified as a module in the manifest.

To compile and install an app inside the sandbox, previously installed with
```flatpakdev install```, run :

```
$ flatpakdev make name
```
