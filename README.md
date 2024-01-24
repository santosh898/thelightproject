# The Light Project

## Recommnded

Using `Thonny IDE` is easier to install packages, test code and move files back and forth between device and local filesystem.

File editing capabilities of thonny are very limited but gets the job done. We can use vscode to edit code and thonny for rest of the things.

Alternatively we can use tools like `rshell` or `ampy` to interact via CLI but that's too complex.

## Prerequisites

The board is expected to be flashed with latest version of micropython.

Connect the board to Thonny IDE and pick the right board name and it will automatically download and flash the binary.

Or

Download and follow instructions from there.
https://micropython.org/download/

## Setting Up

Install all the dependencies in the `requirements.txt`. This list is manually maintained. there is no automatic package management yet. This is yet to be figured out.

To install packages,

### Via Thonny

Connect the Board => Tools => Manage Packages

### Via REPL

```python
import mip
mip.install("thingsboard_micropython")
```

Repeat for all the dependecies.

#### TODO: Write a script that automatically installs dependencies

## Before Running the Code

Edit env.json with appropriate values for your dev setup

### TODO: Build a way to change these values via GUI
