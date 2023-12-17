async def update_user_points(db, cursor, user_id: int, points: int):
    try:
        query = "UPDATE curr_points SET points = (SELECT points FROM curr_points WHERE user_id = %s) +  %s WHERE user_id = %s"
        values = (user_id, points, user_id)
        cursor.execute(query, values)
        db.commit()


    except(ValueError):
         return (ValueError)

async def check_user_points(db, cursor, user_id: int):
    try:
        query = f"SELECT points FROM curr_points WHERE user_id = {user_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            print(f"{check_user_points.__name__}: user with id {user_id} was not found")
            return -1
    
    except(ValueError):
        return None


async def add_new_user(db, cursor, user_id: int):
    try:
        query = "INSERT INTO curr_points (user_id, points) VALUES (%s, %s)"
        values = (user_id, 1000)
        cursor.execute(query, values)

        db.commit()

        print(cursor.rowcount, "user inserted.")

    except(ValueError):
        return ValueError
