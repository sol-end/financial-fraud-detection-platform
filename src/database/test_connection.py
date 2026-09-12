from src.database.connection import get_connection


def main():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user, version();"
            )
            result = cursor.fetchone()

        print("✅ Python database connection successful!")
        print(f"Database: {result[0]}")
        print(f"User: {result[1]}")
        print(f"Version: {result[2]}")

    finally:
        connection.close()
        print("✅ Database connection closed.")


if __name__ == "__main__":
    main()
