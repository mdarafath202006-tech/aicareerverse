"""
app/schemas/user_schemas.py
Marshmallow schemas for request/response validation & serialisation.
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class RegisterSchema(Schema):
    name     = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email    = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role     = fields.Str(required=True, validate=validate.OneOf(["student", "alumni"]))
    # Student fields
    department = fields.Str(load_default="")
    year       = fields.Str(load_default="")
    # Alumni fields
    grad_year = fields.Int(load_default=None)
    company   = fields.Str(load_default="")
    job_role  = fields.Str(load_default="")

    @validates("password")
    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", value):
            raise ValidationError("Password must contain at least one digit.")


class LoginSchema(Schema):
    email    = fields.Email(required=True)
    password = fields.Str(required=True)


class StudentProfileSchema(Schema):
    skills    = fields.Str(load_default="")
    interests = fields.Str(load_default="")
    bio       = fields.Str(load_default="", validate=validate.Length(max=1000))
    github_url   = fields.Url(load_default=None, allow_none=True)
    linkedin_url = fields.Url(load_default=None, allow_none=True)


class AlumniProfileSchema(Schema):
    company   = fields.Str(load_default="", validate=validate.Length(max=150))
    job_role  = fields.Str(load_default="", validate=validate.Length(max=150))
    skills    = fields.Str(load_default="")
    location  = fields.Str(load_default="", validate=validate.Length(max=100))
    linkedin  = fields.Url(load_default=None, allow_none=True)
    bio       = fields.Str(load_default="", validate=validate.Length(max=1000))
    is_hiring = fields.Bool(load_default=False)


class MentorRequestSchema(Schema):
    message = fields.Str(load_default="", validate=validate.Length(max=500))


class SkillGapSchema(Schema):
    target_role = fields.Str(required=True, validate=validate.Length(min=1, max=150))
