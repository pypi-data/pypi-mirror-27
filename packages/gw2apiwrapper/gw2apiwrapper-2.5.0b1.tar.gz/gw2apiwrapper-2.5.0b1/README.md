# GW2API [![Build Status](https://travis-ci.org/PatchesPrime/GW2API.svg?branch=master)](https://travis-ci.org/PatchesPrime/GW2API) [![Coverage Status](https://coveralls.io/repos/github/PatchesPrime/GW2API/badge.svg?branch=master)](https://coveralls.io/github/PatchesPrime/GW2API?branch=master)
Object Orientated GW2 API Wrapper

**2017-11-13 - Decent sized refactor in progress. Majority of conversion is done, but still a few fiddly bits..**

Being dissatisfied with the current implementations of the Guild Wars 2 API written in python, I began this project.

It will eventually (as it's released) implement all of the GW2 v2 API.

To install, simply change to your projects directory and run this:
``` bash
git clone https://github.com/PatchesPrime/GW2API.git
```
Then import it.


Example:
``` python
import GW2API

# Get an account based object. Requires API Key.
personal = GW2API.AccountAPI("<APIKEY>")

# Get a 'Global' api object. (Non-authed)
workHorse = GW2API.GlobalAPI()

# This is iterable, as not only does it fill the personal.bank
# attribute, it also returns that information.
personal.getBank()

bankIDs = [slot['id'] for slot in personal.bank if slot is not None]

# GlobalAPI's getItem can take different types, all documented.
itemObjects = workHorse.getItem(bankIDs)

# Get the names of all items in bank.
for item in itemObjects:
  print(item.name)

```
