from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, BackgroundTasks, Response, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist

from .dependencies import AccessTokenBearer
from .schemas import (
    UserCreateModel,
    UserLoginModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .services import UserService
from .utils import (
    create_access_token,
    decode_token,
    send_verification_mail,
    verify_password,
    generate_passwd_hash,
    create_url_safe_token,
    decode_url_safe_token,
)
from src.errors import (
    AccountNotVerified,
    UserAlreadyExists,
    UserNotFound,
    InvalidCredentials,
    InvalidToken,
)
from src.config import Config


auth_router = APIRouter()
user_service = UserService()


REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/register")
async def register_user(
    user_data: UserCreateModel,
    bg_task: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    """
    Create user account using email, username, first_name, last_name
    params:
        user_data: UserCreateModel
    """
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists

    new_user = await user_service.create_user(user_data, session)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token = decode_url_safe_token(token)

    user_email = token.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel,
    session: AsyncSession = Depends(get_session),
    response: Response = None,
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid and not (user.is_verified):
            send_verification_mail(email)
            raise AccountNotVerified()

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                max_age=REFRESH_TOKEN_EXPIRY * 24 * 60 * 60,  # Convert days to seconds
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(request: Request, response: Response = None):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidToken

    token_details = decode_token(refresh_token)
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken


@auth_router.get("/logout")
async def revoke_token(
    request: Request, token_details: dict = Depends(AccessTokenBearer())
):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        token_details = decode_token(refresh_token)
        jti = token_details["jti"]
        await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """
    subject = "Reset Your Password"

    send_email.delay([email], subject, html_message)
    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        passwd_hash = generate_passwd_hash(new_password)
        await user_service.update_user(user, {"password_hash": passwd_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
