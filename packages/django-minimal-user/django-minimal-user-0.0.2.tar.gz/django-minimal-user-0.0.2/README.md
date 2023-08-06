# django-minimal-user - Minimum User model for Django

Contains a User implementation without the cruft

There are two primary uses:

* Use `minimal_user`.User directly
* Inherit from `minimal_user.AbstractUser` to create a User model with only
  the fields necessary for your project.
