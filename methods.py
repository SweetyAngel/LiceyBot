def antispam():
    for user in users:
        if user.one_min_cnt >= 20:
            user.mute()
