"""Data validation schemas for crypto analysis."""

from marshmallow import Schema, fields, validate, ValidationError


class CryptoAnalysisRequestSchema(Schema):
    """Schema for crypto analysis requests."""

    symbol = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=10),
            validate.Regexp(r"^[A-Z]+$", error="Symbol must be uppercase letters only"),
        ],
        error_messages={
            "required": "Symbol is required",
            "invalid": "Invalid symbol format",
        },
    )

    investment = fields.Int(
        required=True,
        validate=[
            validate.Range(
                min=1, max=1000000, error="Investment must be between 1 and 1,000,000"
            )
        ],
        error_messages={
            "required": "Investment amount is required",
            "invalid": "Investment must be a positive integer",
        },
    )


class CryptoAnalysisResponseSchema(Schema):
    """Schema for crypto analysis responses."""

    message = fields.Dict(required=True)
    graph_data = fields.List(fields.Dict(), required=True)
    success = fields.Bool(missing=True)
    error = fields.Str(allow_none=True)


class HealthCheckSchema(Schema):
    """Schema for health check responses."""

    status = fields.Str(required=True)
    service = fields.Str(required=True)
    version = fields.Str(required=True)
    timestamp = fields.DateTime(missing=None)


class ErrorResponseSchema(Schema):
    """Schema for error responses."""

    error = fields.Str(required=True)
    message = fields.Str(required=True)
    status_code = fields.Int(required=True)
    timestamp = fields.DateTime(missing=None)


def validate_crypto_request(data: dict) -> tuple[bool, dict]:
    """
    Validate crypto analysis request data.

    Args:
        data: Request data to validate

    Returns:
        Tuple of (is_valid, errors)
    """
    schema = CryptoAnalysisRequestSchema()
    try:
        schema.load(data)
        return True, {}
    except ValidationError as e:
        return False, e.messages


def validate_health_response(data: dict) -> tuple[bool, dict]:
    """
    Validate health check response data.

    Args:
        data: Response data to validate

    Returns:
        Tuple of (is_valid, errors)
    """
    schema = HealthCheckSchema()
    try:
        schema.load(data)
        return True, {}
    except ValidationError as e:
        return False, e.messages
