import io
import logging
import unittest
import uuid
from contextlib import redirect_stderr

from logger import Color, get_logger


class TestColorConstants(unittest.TestCase):
    def test_color_constants_exist_and_are_ansi(self):
        for attr in (
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "MAGENTA",
            "CYAN",
            "WHITE",
            "RESET",
        ):
            val = getattr(Color, attr)
            self.assertIsInstance(val, str)
            self.assertNotEqual(val, "")
            # ANSI escape sequences begin with ESC '['
            self.assertTrue(
                val.startswith("\033["), f"{attr} does not start with ESC[: {val}"
            )


class TestGetLoggerBehavior(unittest.TestCase):
    def test_get_logger_adds_handler_and_disables_propagate(self):
        name = f"test_logger_{uuid.uuid4().hex}"
        base = logging.getLogger(name)
        base.handlers.clear()
        base.propagate = True

        logger = get_logger(name)
        self.assertFalse(logger.propagate)
        self.assertGreaterEqual(len(logger.handlers), 1)

        handlers_before = list(logger.handlers)
        logger2 = get_logger(name)
        handlers_after = list(logger2.handlers)
        self.assertIs(logger, logger2)
        self.assertEqual(len(handlers_after), len(handlers_before))
        self.assertEqual(handlers_after, handlers_before)


class TestLoggerOutputFormatting(unittest.TestCase):
    def test_logger_emits_formatted_output_with_colors(self):
        name = f"fmt_logger_{uuid.uuid4().hex}"
        base = logging.getLogger(name)
        base.handlers.clear()
        base.propagate = True

        buf = io.StringIO()
        message = "hello formatted logger"

        # Redirect stderr before creating the handler so StreamHandler binds to this stream
        with redirect_stderr(buf):
            logger = get_logger(name)
            logger.setLevel(logging.INFO)
            logger.info(message)

        contents = buf.getvalue()

        # Basic presence checks
        self.assertIn(name, contents)
        self.assertIn("INFO", contents)
        self.assertIn(message, contents)

        # At least one color code should be present in formatted output
        self.assertTrue(
            any(code in contents for code in (Color.WHITE, Color.GREEN, Color.YELLOW)),
            "Expected at least one ANSI color code in log output",
        )

        # Expect a timestamp- or time-like substring (be permissive)
        self.assertTrue(
            any(ch.isdigit() for ch in contents),
            "Expected digits (timestamp) in log output",
        )


if __name__ == "__main__":
    unittest.main()
