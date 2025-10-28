import uuid
from fastapi import HTTPException, Header, Depends, status
from sqlalchemy import text
from src.dao.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import re
from datetime import date
from src.utils.constants import RequestValidationErrorMessage

# from sentence_transformers import SentenceTransformer, util
import asyncio
import hashlib
from datetime import timedelta, datetime
from src.core.config import settings
import jwt

# from jwt import ExpiredSignatureError
from uuid import UUID
import logging
from src.exceptions.user_authentication import ExpiredToken, InvalidOrExpiredToken
from src.utils.constants import ErrorMessage
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Cipher import PKCS1_OAEP

import base64


def generate_random_uuid():
    """
    Generate a random UUID.

    Returns:
        str: Random UUID as a string.
    """
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def attach_prefix_to_uuid(input_uuid, prefix):
    """
    Attach a prefix to a UUID.

    Args:
        input_uuid (str or UUID): Input UUID.
        prefix (str): Prefix to attach.

    Returns:
        str: UUID with the prefix attached.
    """
    if isinstance(input_uuid, str):
        input_uuid = uuid.UUID(input_uuid)

    result_uuid = f"{prefix}{input_uuid}"

    return result_uuid


def remove_prefix(value: str) -> UUID:
    """
    Removes the prefix from a string in the format 'prefix:<UUID>'
    and returns the UUID object.
    """
    return UUID(value.split(":")[1])


async def get_current_user(
    user_id: str = Header(None, convert_underscores=False),
    db: AsyncSession = Depends(get_db),
):
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID missing")

    query = text('SELECT id FROM "users"."users" WHERE id = :user_id')
    result = await db.execute(query, {"user_id": user_id})
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid User ID")

    return user


def validate_if_alphabet(value: str):
    """
    This function checks if the input is a string and only contains alphabets.

    :param value: Pass the value of the input field to if_alpha function
    :return: The value of the string if it only contains alphabets
    """
    if all(letter.isalpha() or letter.isspace() for letter in value):
        return value
    raise ValueError(RequestValidationErrorMessage.VALIDATE_NAME.format(value=value))


def validate_date(value: date):
    """
    This function checks if the date is greater than today.

    :param value: Pass the value of the date that is being validated
    :return: The value of the date if it is less to today
    """
    if value > date.today():
        raise ValueError(RequestValidationErrorMessage.VALIDATE_DATE)
    return value


def error_loc(loc: list):
    """
    This function is used to return an error message when there
    is a validation exception.

    :param loc:list: Determine the location of the error
    :return: The location of the error
    """
    tokens = []
    for i in range(0, len(loc)):
        if str(loc[i]).isdigit():
            index = len(tokens) - 1
            tokens[index] = tokens[index] + "[" + str(loc[i]) + "]"
        else:
            tokens.append(loc[i])
    return ".".join(tokens)


def validate_phone_number(phone_number: str):
    """
    This function checks if phone number is valid or not.

    :param phone_number: value of phone_number
    :return: Returns phone_number if valid.
    """
    regex = r"^(?:(?:\+{0,2})52(\s*[\-]\s*)?|0?)?[6-9]\d{9}$"
    if re.match(regex, phone_number):
        return phone_number
    raise ValueError(RequestValidationErrorMessage.VALIDATE_PHONE_NUMBER)


def validate_email(email: str):
    """
    This function checks if email is valid or not.

    :param email: value of email
    :return: Returns email if valid.
    """
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(regex, email):
        return email
    raise ValueError(RequestValidationErrorMessage.VALIDATE_EMAIL)


def validate_password(password: str):
    """
    This function checks if password is valid or not.

    :param password: value of password
    :return: Returns password if valid.
    """
    regex = r"^[A-Za-z](?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%#*?&]{7,11}$"
    if re.match(regex, password):
        return password
    raise ValueError(RequestValidationErrorMessage.VALIDATE_PASSWORD)


# model = SentenceTransformer("all-MiniLM-L6-v2")

# words = [
#     "men",
#     "man",
#     "male",
#     "boy",
#     "gentleman",
#     "guy",
#     "women",
#     "woman",
#     "female",
#     "girl",
#     "lady",
#     "kids",
#     "children",
#     "boys",
#     "girls",
#     "unisex",
#     "infant",
#     "toddler",
#     "baby",
#     "shirt",
#     "tshirt",
#     "kurta",
#     "jeans",
#     "jacket",
#     "sweater",
#     "hoodie",
#     "top",
#     "blouse",
#     "dress",
#     "skirt",
#     "shorts",
#     "trousers",
#     "saree",
#     "lehenga",
#     "blazer",
#     "coat",
#     "suit",
#     "salwar",
#     "churidar",
#     "tank top",
#     "cotton",
#     "denim",
#     "silk",
#     "linen",
#     "polyester",
#     "wool",
#     "leather",
#     "velvet",
#     "satin",
#     "nylon",
#     "formal",
#     "casual",
#     "ethnic",
#     "party wear",
#     "activewear",
#     "sportswear",
#     "designer",
#     "vintage",
#     "trendy",
#     "classic",
#     "minimal",
#     "boho",
# ]

# word_embeddings = model.encode(words, convert_to_tensor=True)


# async def get_similar_words_with_sbert(search_term: str, top_n: int = 10):
#     loop = asyncio.get_running_loop()
#     search_embedding = await loop.run_in_executor(None, model.encode, search_term)
#     scores = util.pytorch_cos_sim(search_embedding, word_embeddings)[0]
#     top_results = scores.topk(top_n)
#     similar_words = []
#     for idx, score in zip(top_results.indices, top_results.values):
#         if score.item() > 0.5:
#             similar_words.append(words[idx])
#     return similar_words


def generate_password_hash(password: str):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password.encode("utf-8"))
    return sha256_hash.hexdigest()


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.utcnow() + (
        expiry
        if expiry is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token


def verify_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True},
        )
        return token_data
    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
        raise ExpiredToken(message=ErrorMessage.EXPIRED_TOKEN.format())
    except jwt.PyJWTError as e:
        logging.exception("Invalid token")
        raise InvalidOrExpiredToken(
            message=ErrorMessage.INVALID_OR_EXPIRED_TOKEN.format()
        )


def generate_OTP():
    """Function to generate OTP of 6 digits."""
    return "".join(random.choices("0123456789", k=6))


private_key_pem = settings.BACKEND_KEY


def decrypt_password(encrypted_password: str, encrypted_aes_key: str, iv: str) -> str:
    try:
        # Import private key
        private_key = RSA.import_key(private_key_pem)

        # Create PKCS1_OAEP cipher for RSA decryption (for AES key only)
        cipher_rsa = PKCS1_OAEP.new(private_key)

        # Decrypt only the AES key using RSA-OAEP
        aes_key = cipher_rsa.decrypt(base64.b64decode(encrypted_aes_key))

        # IV is base64 encoded text:
        aes_iv = base64.b64decode(iv)

        # Decrypt password using AES
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        decrypted_password = unpad(
            cipher_aes.decrypt(base64.b64decode(encrypted_password)), AES.block_size
        ).decode("utf-8")

        return decrypted_password
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}") from e
