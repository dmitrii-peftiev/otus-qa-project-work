class Endpoints:
    USERS = "/users"
    REGISTER = "/register"
    LOGIN = "/login"
    RESOURCES = "/unknown"

    @staticmethod
    def user_by_id(user_id: int) -> str:
        return f"/users/{user_id}"

    @staticmethod
    def resource_by_id(resource_id: int) -> str:
        return f"/unknown/{resource_id}"
