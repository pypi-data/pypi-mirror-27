To use this - add this to your setting.py's INSTALLED_APPS:

    'userservice',

And this to your MIDDLEWARE_CLASSES:

    'userservice.user.UserServiceMiddleware',                                   


This project uses authz_group to control access to the user override app.  If you want to use that app, add this to your project/urls.py:


and this to your setting.py:

    AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation....'           
    USERSERVICE_ADMIN_GROUP = '... group name ...' 

If you want to allow anyone to be able to override - and don't do that in production - you can use this:

    AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'           

If you want to validate the user ids required for override, add this to your settings.py:

    USERSERVICE_VALIDATION_MODULE='userservice.validation.is_email'
    
The validation module can be replaced with a local implementation for your applicaiton.  

With all of that in place, request.user will be either the actual user, or the user you are impersonating.  To get more information about the current user, you can use:

    user_service = UserService() 
    
    # This is the logged in user's name:
    user_service.get_original_user()
    
    # This is the override user:
    user_service.get_override_user()

    # This will be the override user if it exists, the logged in user otherwise:
    user_service.get_user() 

To make this a dependency for your app, add this to your requirements.txt:

    Django-UserService

or to install, just run:

    pip install Django-UserService
