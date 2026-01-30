from django.conf import settings

def school_info(request):
    return {
        "SCHOOL_NAME": settings.SCHOOL_INFO["NAME"],
        "SCHOOL_LOCATION": settings.SCHOOL_INFO["LOCATION"],
        "SCHOOL_PRINCIPAL": settings.SCHOOL_INFO["PRINCIPAL"],
        "SCHOOL_PHONE": settings.SCHOOL_INFO["PHONE"],
        "SCHOOL_EMAIL": settings.SCHOOL_INFO["EMAIL"],
        "SCHOOL_OFFICE_HOURS": settings.SCHOOL_INFO["OFFICE_HOURS"],
        "SCHOOL_LOGO": settings.SCHOOL_INFO["LOGO"],
    }