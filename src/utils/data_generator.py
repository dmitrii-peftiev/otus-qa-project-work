from faker import Faker

fake = Faker()


def get_random_user() -> dict:
    return {"name": fake.first_name(), "job": fake.job()}


def get_random_password() -> str:
    return fake.password(length=10)


def get_random_checkout_info() -> dict:
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "postal_code": fake.postcode(),
    }
