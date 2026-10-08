import sqlite3


DB_NAME = "fashion.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()


    # ==========================================
    # SAVED OUTFITS TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_outfits (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_name TEXT,

            outfit_id INTEGER,

            top TEXT,

            bottom TEXT,

            shoes TEXT,

            accessories TEXT,

            event TEXT,

            style TEXT,

            match_score REAL

        )
    """)


    # ==========================================
    # FEEDBACK TABLE
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_name TEXT,

            outfit_id INTEGER,

            feedback TEXT

        )
    """)


    conn.commit()

    conn.close()


def save_outfit(user_name, outfit):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO saved_outfits (

            user_name,
            outfit_id,
            top,
            bottom,
            shoes,
            accessories,
            event,
            style,
            match_score

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_name,

        int(outfit["outfit_id"]),

        outfit["top"],

        outfit["bottom"],

        outfit["shoes"],

        outfit["accessories"],

        outfit["event"],

        outfit["style"],

        float(outfit["match_score"])

    ))


    conn.commit()

    conn.close()


def save_feedback(
    user_name,
    outfit_id,
    feedback
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO feedback (

            user_name,
            outfit_id,
            feedback

        )

        VALUES (?, ?, ?)

    """, (

        user_name,

        int(outfit_id),

        feedback

    ))


    conn.commit()

    conn.close()


def get_feedback_score(
    user_name,
    outfit_id
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT feedback

        FROM feedback

        WHERE user_name = ?

        AND outfit_id = ?

    """, (

        user_name,

        int(outfit_id)

    ))


    results = cursor.fetchall()

    conn.close()


    score = 0


    for row in results:

        if row[0] == "Like":

            score += 10

        elif row[0] == "Dislike":

            score -= 10


    return score


def get_saved_outfits(user_name):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *

        FROM saved_outfits

        WHERE user_name = ?

    """, (

        user_name,

    ))


    results = cursor.fetchall()

    conn.close()


    return results