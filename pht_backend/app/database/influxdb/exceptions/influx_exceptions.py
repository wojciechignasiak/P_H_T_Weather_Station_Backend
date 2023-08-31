class InfluxDatabaseError(Exception):
    """Base exception for database related errors."""

class InfluxNotFoundError(InfluxDatabaseError):
    """Exception thrown when the record is not found."""
