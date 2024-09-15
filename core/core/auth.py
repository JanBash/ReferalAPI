from mozilla_django_oidc.auth import OIDCAuthenticationBackend

class MyOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """
        Create a new user from the provided claims.
        """
        print(claims)
        
        user = super().create_user(claims)
        
        if 'admin' in claims:
            user.is_admin = True
        user.username = claims['name']
        user.save()
        
        return user
