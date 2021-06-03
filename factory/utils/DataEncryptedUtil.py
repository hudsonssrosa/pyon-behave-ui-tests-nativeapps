import hashlib
import random
import string
import time
import uuid
from datetime import date
from factory.handling.running_exception import RunningException as Rexc


class DataEncrypted:
    @staticmethod
    def generate_random_data(
        length=2,
        start_threshold=1,
        end_threshold=9999999,
        step=1,
        only_numbers=False,
        only_letters=False,
    ):
        length = int(length)
        all_letters = str(string.ascii_letters)
        end_threshold_in_range = int(end_threshold) + 1
        random_letters = "".join(random.choice(all_letters) for i in range(length))
        random_number = random.randrange(int(start_threshold), end_threshold_in_range, int(step))
        numbers_to_hash = str(random.randrange(int(start_threshold), end_threshold_in_range)) + str(
            date.today().strftime("%d%m%Y%H%M%S")
        )
        time.sleep(0.5)
        numeric_hash = str(random_number)[:length] if only_numbers and only_letters is False else ""
        alphabetic_hash = random_letters[:length] if only_letters and only_numbers is False else ""
        alphanumeric_hash = (
            DataEncrypted.parse_to_sha1(numbers_to_hash)[:length]
            if numeric_hash == "" and alphabetic_hash == ""
            else numeric_hash or alphabetic_hash
        )
        print(f"-> Hash generated: {alphanumeric_hash}")
        return alphanumeric_hash

    @staticmethod
    def parse_to_sha1(string_to_hash):
        try:
            hash_object = hashlib.sha1(bytes(string_to_hash, "utf-8"))
            hex_dig = hash_object.hexdigest()
            return hex_dig
        except InterruptedError as ie:
            Rexc.raise_exception_error("Parsing of object was not possible. ", ie)

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(":")
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
