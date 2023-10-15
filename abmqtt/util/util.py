import os


class Util:
    @staticmethod
    def get_env_variable(name: str) -> str:
        result = os.environ.get(name)

        if result is None:
            raise ValueError

        return result
