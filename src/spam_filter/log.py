"""Shared logging configuration for the spam_filter package."""

import logging
import os
import sys


# EN: Export levels so other modules can use log.WARNING, etc.
# FR : Exporter les niveaux pour utiliser log.WARNING, etc. ailleurs.
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class ColorFormatter(logging.Formatter):
    """Colorize the timestamp and severity when output goes to a terminal."""

    RESET = "\033[0m"
    DIM = "\033[2m"
    COLORS = {
        logging.DEBUG: "\033[90m",     # Gray / gris
        logging.INFO: "\033[36m",      # Cyan
        logging.WARNING: "\033[33m",   # Yellow / jaune
        logging.ERROR: "\033[31m",     # Red / rouge
        logging.CRITICAL: "\033[35m",  # Magenta
    }

    def format(self, record: logging.LogRecord) -> str:
        # EN: Let logging format multiline messages and exception tracebacks.
        # FR : Laisser logging formater les messages et les traces d'erreur.
        formatted = super().format(record)

        # EN: Preserve plain output for notebooks, redirected logs, and NO_COLOR.
        # FR : Garder du texte simple pour notebooks, redirections et NO_COLOR.
        if not sys.stdout.isatty() or "NO_COLOR" in os.environ:
            return formatted

        time, separator, remainder = formatted.partition(" │ ")
        level, level_separator, message = remainder.partition(" │ ")
        if not separator or not level_separator:
            return formatted

        color = self.COLORS.get(record.levelno, "")
        return (
            f"{self.DIM}{time}{self.RESET} │ "
            f"{color}{level}{self.RESET} │ {message}"
        )


# EN: Configure one package-wide logger shared by all imports.
# FR : Configurer un logger commun à tous les modules du package.
logger = logging.getLogger("spam_filter")
logger.setLevel(INFO)
logger.propagate = False

# EN: Avoid duplicate handlers when reloading the module in a notebook.
# FR : Éviter les sorties en double lors du rechargement dans un notebook.
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColorFormatter(
            fmt="%(asctime)s │ %(levelname)-7s │ %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    handler.terminator = "\n\n"
    logger.addHandler(handler)


def syslog(
    message: str,
    verbose: bool = True,
    level: int = INFO,
) -> None:
    """Log a message at the requested level when verbose output is enabled."""

    # EN: Return immediately when logging is disabled for this call.
    # FR : Quitter immédiatement si le log est désactivé pour cet appel.
    if not verbose:
        return

    logger.log(level, message)
