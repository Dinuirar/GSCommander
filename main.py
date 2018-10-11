#!/usr/bin/env python
import ui


if __name__ == "__main__":
    # execute only if run as a script
    prompt = ui.cmdSSG()
    prompt.prompt = '> '
    prompt.cmdloop('GSS waiting for commands')