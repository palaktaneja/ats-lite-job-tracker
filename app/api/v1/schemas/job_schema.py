from marshmallow import Schema, fields, validate

class JobCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=3))
    description = fields.String(required=True)
    location = fields.String(required=True)


class JobResponseSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    location = fields.String()