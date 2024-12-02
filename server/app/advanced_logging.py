import io
import logging


# Custom log handler
class MemoryLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []  # Store logs as a list of strings

    def emit(self, record):
        log_entry = self.format(record)
        self.logs.append(log_entry)

    def get_logs(self):
        """Return the stored logs."""
        return self.logs

    def clear_logs(self):
        """Clear the stored logs."""
        self.logs.clear()


# Create a global log handler instance
memory_log_handler = MemoryLogHandler()
