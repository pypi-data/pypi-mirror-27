# orfium\_oauth\_provider

## Purpose
This packages is a plugin on top of the [django-allauth](https://www.intenct.nl/projects/django-allauth/) app that provides the [Orfium](https://www.orfium.com) music platform as an OAuth provider.
 
## Instructions
1. Add `django-allauth` and `this` as requirements to your project and install them.

2. Add the following apps to your INSTALLED_APPS
    * `'django.contrib.auth'`,
    * `'django.contrib.sites'`,
    * `'allauth'`,
    * `'allauth.account'`,
    * `'orfium_oauth_provider'`,

3. Make sure the following context processor is included in the `TEMPLATES` setting:
    `'django.template.context_processors.request'`

4. Add `'allauth.account.auth_backends.AuthenticationBackend'` to the `AUTHENTICATION_BACKENDS` setting.

5. Specify the social account adapter (Allows connecting the orfium user account to your apps local users based on their usernames):
	`SOCIALACCOUNT_ADAPTER = 'orfium_oauth_provider.adapters.ConnectExistingUsersSocialAccountAdapter'`
	
6. Set `SITE_ID = 1` in your settings

7. Use `/accounts/orfium_oauth2/login/?process=login` as the login link to automatically redirect users to Orfium,
    or optionally add the following to your `MIDDLEWARE` setting if you want all pages to be protected:
    `orfium_oauth_provider.middlewares.AuthRequiredMiddleware`
    If you use the middleware, you can specify which paths should be ignored by using the `AUTH_REQUIRED_IGNORE_PATHS` setting:

    ```
    AUTH_REQUIRED_IGNORE_PATHS = [
        '/accounts/',  # all URLs that start with /accounts/
        '/admin/',  # all URLs that start with /admin/
    ]
    ```

8. Add the following to your urls:
    `url(r'^accounts/', include('allauth.urls'))`

9. Migrate:
    `python manage.py migrate`

10. Register your application at https://api.orfium.com/oauth/applications/ and make sure you specify the client type as `Public`
and the authorization grant type as `Authorization code`.
You may use the `API_ORFIUM_ENDPOINT` setting if you want your application to use an alternative endpoint such as `https://api.dev.orfium.com`.
By default the endpoint is set to `https://api.orfium.com`.

11. Update your sites info under `Sites` in the admin and create a new social application for the Orfium provider,
using the App ID and Token you got from the previous step.