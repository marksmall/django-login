import subprocess, logging

from django.core.management.base import BaseCommand

LOGGER = logging.getLogger((__name__))


class Command(BaseCommand):
    """ Command to run tests """
    help = "Run server tests in single vs. watch mode"

    def add_arguments(self, parser):
        """ Add custom arguments """
        parser.add_argument(
            "--single",
            action="store_true",
            help="The mode which to run tests in")
        parser.add_argument(
            "files", nargs="*", help="The test file|dir to run")

    def handle(self, *args, **options):
        """ Handle running of tests """
        # LOGGER.debug(f"ARGS: {args}")
        # LOGGER.debug(f"OPTIONS: {options}")
        # LOGGER.debug(f"FILES: {files}")
        mode = options["single"]

        # LOGGER.debug(f"OPTION MODE: {mode}")

        cmd = None
        if mode and mode == True:
            # LOGGER.debug(f"MODE: {mode}")
            if options["files"]:
                cmd = ["pytest", *options["files"]]
            else:
                cmd = ["pytest"]
        else:
            # LOGGER.debug(f"WATCH MODE: {mode}")
            if options["files"]:
                cmd = ["ptw", *options["files"]]
            else:
                cmd = ["ptw"]

        # LOGGER.debug(f"LIST Command to run: {cmd}")
        command = "".join(cmd)
        # LOGGER.debug(f"Command to run: {command}")
        com = " ".join(*options["files"])
        LOGGER.debug(f"ls {com}")
        # subprocess.run(f"ls {com}")
        # subprocess.run(f"ls {options['files']}")
