class UserDatabase:
    def __init__(self, databaseConnection):
        self.db = databaseConnection

    def upload(self, userData):
        self.createTableFieldNames(userData)
        self.uploadUserInformation(userData)

    def createTableFieldNames(self, userData):
        cursor = self.db.cursor()
        columns = []
        for name, _ in userData:
            colType = "INTEGER" if name == "GradeLevel" else "TEXT"
            columns.append(f"{name} {colType}")
        createSql = f"CREATE TABLE IF NOT EXISTS Users ({', '.join(columns)})"
        cursor.execute(createSql)
        self.db.commit()

    def uploadUserInformation(self, userData):
        cursor = self.db.cursor()
        columns = [item[0] for item in userData]
        values = [item[1] for item in userData]
        insertSql = f"""
            INSERT INTO Users ({', '.join(columns)})
            VALUES ({', '.join(['?'] * len(values))})
        """
        cursor.execute(insertSql, values)
        self.db.commit()
