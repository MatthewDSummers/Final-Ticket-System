from django.db import models
import re
import bcrypt

class UserManager(models.Manager):

    """
    Custom manager for the User model.

    This manager provides functionality for validating user data inputs.

    Methods:
        validator(postData, form_type=None, authorizer=None):
            Validates user data inputs based on specific rules.
            form_type="Edit" for edit form
            authorizer=current user logged in (used in edit function)

    """

    def validator(self, postData, form_type=None, authorizer=None, target_user=None):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        required_fields = {'first_name', 'last_name'}
        flag = 0

        if form_type is None:
            required_fields.add('password')
            required_fields.add('confirm_password')
            required_fields.add('email')

        elif form_type == "Edit":
            # regular users can't change thier email 
            if authorizer.level != 1:
                required_fields.add('email')

        for field in required_fields:
            if postData.get(field) is None:
                field_name = field.replace("_", " ")
                errors[field] = f'Missing field: "{field_name}"'
                flag += 1

        if flag != 0:
            return errors

        else:
        # INCORRECT PASSWORD PROVIDED IN "EDIT" FORM 
            # return errors early so they only get the too_many_attempts error.
            # user must login again to clear the fail authorization attempts 
            if form_type == "Edit":
                if not bcrypt.checkpw(postData.get('own_password').encode(), authorizer.password.encode()):
                    authorizer.failed_authorization()

                    if authorizer.failed_authorization_attempts != 3:
                        remaining_attempts = "One attempt" if authorizer.failed_authorization_attempts == 2 else "Two attempts"
                        errors["incorrect_password"] = f"Incorrect password. {remaining_attempts} remaining"

                    elif authorizer.failed_authorization():
                        errors['too_many_attempts'] = "Too many authorization attempts. Login again to continue."
                        return errors
                else:
                    authorizer.reset_failed_authorizations()

        # FIRST NAME
            #  at least 2 characters
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name must be at least 2 characters"
            # Letters only
            if postData['first_name'].replace(' ', '').isalpha() == False:
                errors['first_name'] = "First name must be letters only"
            # Required

        # LAST NAME
            # at least 2 characters
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name must be at least 2 characters"
            # letters only
            if postData['last_name'].replace(' ', '').isalpha() == False :
                errors['last_name'] = "Last name must be letters only"
            # Required
            if len(postData['last_name']) == 0:
                errors['last_name'] = "Last name required"

        # EMAIL
            if "email" in required_fields:
                # Required
                if len(postData['email']) == 0:
                    errors['email'] = "Account must have an email"
                # valid format
                elif not EMAIL_REGEX.match(postData['email']):
                    errors['email'] = "Invalid email address"

        #Registered email is unique
            if form_type is None:
                try: 
                    self.get(email=postData['email'])
                    errors['email_unique'] = "An account is already associated with that email"
                except User.DoesNotExist:
                    pass
            elif form_type == "Edit":
                try: 
                    user_object_with_that_email = self.get(email=postData['email'])
                except User.DoesNotExist:
                    pass
                else:
                    # can't update a user to have someone else's email
                    if target_user != user_object_with_that_email:
                        errors['email_unique'] = "An account is already associated with that email"
                    # regular users can't change their email 
                    if authorizer.level == 1:
                        errors['email_unique'] = "If you need help changing your email, please contact support"

        # PASSWORD:
            # at least 8 Chars
            if "password-checkbox" in postData or form_type == None: # for edit form, they don't have to change their password
                if len(postData.get('password')) < 8:
                    errors['password'] = "Password must be at least 8 characters"
                # Required
                if postData.get('password') == "":
                    errors['password'] = "Account must have a password"
                # Matches Confirmation
                if postData.get('password') != postData.get('confirm_password'):
                    errors['password'] = "Password and password confirmation must match"

                if postData.get('password') == "password":
                    # what about all the other colors of the rainbow?... (see passlib, etc)
                    errors['password'] = "Try a more complex password"

        return errors


        
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, default="")
    level = models.IntegerField()
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    failed_authorization_attempts = models.IntegerField(default=0)
    objects = UserManager()


    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super(User, self).save(*args, **kwargs)

    def failed_authorization(self):
        self.failed_authorization_attempts += 1 
        self.save()
        if self.failed_authorization_attempts >= 3:
            print("failed authorization attempts are this many:", self.failed_authorization_attempts)
            print("User is getting kicked out")
            return True
        else:
            print("failed authorization attempts are this many:", self.failed_authorization_attempts)
            print("Still more attempts left")
            return False
        # return self.failed_authorization_attempts

    def reset_failed_authorizations(self):
        self.failed_authorization_attempts = 0
        self.save()
        print("failed authorization attempts are this many:", self.failed_authorization_attempts)
        print("resetting the failed authorization attempts")
        return

    def serialize(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'level':self.level,
            'email':self.email,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
        }

    def unviewed_message_count(self):
        return(self.inbox.messages.all().count() - self.inbox.viewed.all().count())
