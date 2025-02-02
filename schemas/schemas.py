from marshmallow import Schema, fields

class CreateCarSchema(Schema):
  name = fields.Str(required=True)
  brand_id = fields.Str(required=True)
  model = fields.Str(required=True)
  year = fields.Int(required=True)

class CreateBrandSchema(Schema):
  name = fields.Str(required=True)
  description= fields.Str(required=False, default=None)