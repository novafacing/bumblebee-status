#!/usr/bin/env python

import os
import sys
import logging
import signal
import bumblebee.theme
import bumblebee.engine
import bumblebee.config
import bumblebee.output
import bumblebee.input
import bumblebee.modules.error

try:
    reload(sys)
    sys.setdefaultencoding('UTF8')
except Exception:
    pass


def main():
    def sig_USR1_handler(signum,stack):
        engine.write_output()
        
    config = bumblebee.config.Config(sys.argv[1:])

    if config.debug():
        if config.logfile() in ["stdout", "stderr"]:
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s] %(levelname)-8s %(message)s",
                stream=sys.stdout if config.logfile() == "stdout" else sys.stderr
            )
        else:
            logging.basicConfig(
                level=logging.DEBUG,
                format="[%(asctime)s] %(levelname)-8s %(message)s",
                filename=config.logfile()
            )

    theme = bumblebee.theme.Theme(config.theme(), config.iconset())
    output = bumblebee.output.I3BarOutput(theme=theme, config=config)
    inp = bumblebee.input.I3BarInput()
    engine = None

    try:
        engine = bumblebee.engine.Engine(
            config=config,
            output=output,
            inp=inp,
            theme=theme,
        )
        signal.signal(10,sig_USR1_handler)
        engine.run()
    except KeyboardInterrupt as error:
        inp.stop()
        sys.exit(0)
    except BaseException as e:
        if not engine: raise
        module = engine.current_module()
        logging.exception(e)
        if output.started():
            output.flush()
            output.end()
        else:
            output.start()
        import time
        while True:
            output.begin()
            error = bumblebee.modules.error.Module(engine, {
                "config": config, "name": "error"
            })
            error.set("exception occurred: {} in {}".format(e, module))
            widget = error.widgets()[0]
            widget.link_module(error)
            output.draw(widget, error)
            output.flush()
            output.end()
            time.sleep(1)

if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
