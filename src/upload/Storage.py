# Storage is reset when lambda is slept


class Storage:
    @staticmethod
    def save(data):
        if "storage" not in globals():
            global storage
            storage = set()

        if data in storage:
            raise Exception("Duplicate data")

        storage.add(data)
