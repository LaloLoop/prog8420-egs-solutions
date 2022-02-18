from repository import DBRepository


class DBExporter:
    def __init__(self):
        self._repo = DBRepository()

    def export(self, file_path="./userdb-backup.csv"):
        with open(file_path, "w") as output_file:
            user_gen = self._repo.find_all()

            for u in user_gen:
                output_file.write(",".join(map(lambda c: str(c), u)) + "\n")
