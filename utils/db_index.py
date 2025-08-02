"""
Company>>>
db.company.create_index("invite_code", unique=True)
db.company.create_index("domain", unique=True)
db.company.create_index("company_unique_id", unique=True)

User>>>
db.User.create_index("Email", unique=True)
"""
