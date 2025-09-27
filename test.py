from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr

# Trường hợp đúng
user = User(name="Nguyen Quyet", email="quyet@example.com")
print(user)  
# > name='Nguyen Quyet' email='quyet@example.com'

# Trường hợp sai
user = User(name="Nguyen Quyet", email="abc")  
# > pydantic.error_wrappers.ValidationError: 1 validation error for User
# > email
# >   value is not a valid email address