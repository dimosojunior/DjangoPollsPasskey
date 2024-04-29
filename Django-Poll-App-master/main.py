from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette.templating import Jinja2Templates
import secrets
import base64

templates = Jinja2Templates(directory="templates")


def generate_secret(length: int = 64) -> bytes:
    """https://www.w3.org/TR/webauthn-2/#sctn-cryptographic-challenges"""
    return secrets.token_bytes(length)


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def register_request(request):
    username = request.path_params.get("username")
    if username is None:
        return JSONResponse({"error", "username cannot be empty"})

    # See https://www.w3.org/TR/webauthn-2/#sctn-user-handle-privacy
    # and https://www.w3.org/TR/webauthn-2/#dom-publickeycredentialuserentity-id
    # It is RECOMMENDED to let the user handle be 64 random bytes, and store this value in the user’s account.
    # authentication and authorization decisions MUST be made on the basis of this id member, not the displayName nor name members.
    # See Section 6.1 of [RFC8266]
    # Note we send user_id base64 encoded so that it may be serialized into a JSON string which is returned to the browser
    user_id = base64.b64encode(generate_secret(length=64)).decode("utf-8")

    challenge = base64.b64encode(generate_secret()).decode("utf-8")

    publicKeyCrendentialCreationOptions = {
        "challenge": challenge,  # Must be decoded back into bytes client side
        "rp": {
            "name": "ACME Corp",
            # id not required, and is OK to not provide
            # since the challange includes the origin
            # when generating the attestationObject
            # *"id": "localhost" */
        },
        # user_id Must be decoded back into bytes client side
        "user": {"name": "Bob", "displayName": "Bob", "id": user_id},
        # https://w3c.github.io/webauthn/#dom-publickeycredentialcreationoptions-pubkeycredparams */
        "pubKeyCredParams": [
            {"type": "public-key", "alg": -7},
            {"type": "public-key", "alg": -35},
            {"type": "public-key", "alg": -36},
            {"type": "public-key", "alg": -257},
            {"type": "public-key", "alg": -258},
            {"type": "public-key", "alg": -259},
            {"type": "public-key", "alg": -37},
            {"type": "public-key", "alg": -38},
            {"type": "public-key", "alg": -39},
            {"type": "public-key", "alg": -8},
        ],
        "authenticatorSelection": {
            # https://www.w3.org/TR/webauthn-2/#dom-authenticatorselectioncriteria-requireresidentkey
            # "requireResidentKey": false,
            "userVerification": "preferred",
            "authenticatorAttachment": "platform",
        },
        "timeout": 60000,
        "attestation": "direct",
    }

    return JSONResponse(publicKeyCrendentialCreationOptions)


async def receiveAttestationObject(request):
    """See step 5 of: https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API#registration"""
    data = await request.json()
    breakpoint()
    return "OK"


async def health(request):
    return JSONResponse({"healthy": True})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/register/{username}", register_request),
        Route(
            "/register/sendAttestationObject",
            receiveAttestationObject,
            methods=["POST"],
        ),
    ],
)
