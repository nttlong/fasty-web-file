from datetime import datetime

import bson

import ReCompact


@ReCompact.document(
    name="SYS_SingleSignOn",
    keys=[ "SSOID"],
    indexes=["Token","Application","Application,Token","Application,SSOID","ReturnUrlAfterSignIn","Username"]
)
class SSO:
    _id = (bson.ObjectId)
    Token = (str)
    SSOID = (str)
    CreatedOn = (datetime)
    Application = (str)
    ReturnUrlAfterSignIn =(str)
    Username =(str)