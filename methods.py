def antispam():
    for user in users:
        if user.one_min_cnt >= 20:
            user.mute()
    conn = sqlite3.connect('bot.sqlite', check_same_thread = False)
    cursor = conn.cursor()
    cursor.execute(phr)
    conn.commit()
    conn.close()
