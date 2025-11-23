import io
import logging
import unittest
import uuid

from logger import Color
from timer import Timer


class TestTimer(unittest.TestCase):

    def _make_logger(self, buf: io.StringIO):
        name = f"test_timer_{uuid.uuid4().hex}"
        logger = logging.getLogger(name)
        logger.handlers.clear()
        handler = logging.StreamHandler(buf)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        return logger

    def test_timer_logs_enter_and_exit_when_called_directly(self):
        buf = io.StringIO()
        logger = self._make_logger(buf)

        t = Timer(logger=logger, prefix="mytask")
        # call enter/exit directly (Timer.__exit__ currently has no signature for context-manager args)
        t.__enter__()
        t.__exit__(
            None
        )  # note: calling directly to avoid context-manager signature mismatch

        contents = buf.getvalue()
        # prefix and entry pattern
        self.assertIn("mytask", contents)
        self.assertIn("...", contents)
        # exit should log "done" and a time suffix like "s"
        self.assertIn("done", contents)
        self.assertIn("Used", contents)
        self.assertIn("s", contents)
        # color codes from Color should appear
        self.assertTrue(
            any(c in contents for c in (Color.CYAN, Color.WHITE, Color.YELLOW))
        )

        # cleanup
        logger.handlers.clear()


if __name__ == "__main__":
    unittest.main()
