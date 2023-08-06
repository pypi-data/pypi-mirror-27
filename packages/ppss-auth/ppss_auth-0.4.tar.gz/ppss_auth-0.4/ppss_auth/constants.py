class Conf():


    @classmethod
    def setup(cls,settings):
        cls.adminname   =settings.get("ppss_auth.adminname","dan")
        cls.adminpass   =settings.get("ppss_auth.adminpass","dan")
        cls.logoutroute = settings.get("ppss_auth.post_logout_route","home")
        cls.postloginroute = settings.get("ppss_auth.post_login_route","home")
        cls.postloginfollow = settings.get("ppss_auth.post_login_follow","true").lower() == 'true'
        cls.saltforhash = settings.get("ppss_auth.salt","ImTheSaltOfThisLife")