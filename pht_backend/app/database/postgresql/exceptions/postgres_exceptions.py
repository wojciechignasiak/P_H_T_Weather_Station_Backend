class PostgreSQLDatabaseError(Exception):
    """Base exception for database related errors."""

class PostgreSQLNotFoundError(PostgreSQLDatabaseError):
    """Exception thrown when the record is not found."""
