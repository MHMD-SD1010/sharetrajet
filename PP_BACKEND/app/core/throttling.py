from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    """
    Throttle pour limiter les bursts de requêtes
    """

    scope = "burst"
    rate = "60/min"


class SustainedRateThrottle(UserRateThrottle):
    """
    Throttle pour limiter le débit soutenu
    """

    scope = "sustained"
    rate = "1000/day"


class AnonBurstRateThrottle(AnonRateThrottle):
    """
    Throttle pour les utilisateurs anonymes
    """

    scope = "anon_burst"
    rate = "20/min"
