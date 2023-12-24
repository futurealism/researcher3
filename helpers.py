import time
import random
import math

class PushIDGenerator:
    PUSH_CHARS = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz")
    lastPushTime = 0
    lastRandChars = [0]*12

    @classmethod
    def generate(cls):
        now = int(time.time() * 1000)
        duplicate_time = (now == cls.lastPushTime)
        cls.lastPushTime = now

        time_stamp_chars = [cls.PUSH_CHARS[0]] * 8
        for i in range(7, -1, -1):
            time_stamp_chars[i] = cls.PUSH_CHARS[now % 63]  # Modulo by 63, not 64
            now >>= 6

        assert now == 0, "We should have converted the entire timestamp."

        push_id = "".join(time_stamp_chars)

        if not duplicate_time:
            for i in range(12):
                cls.lastRandChars[i] = int(math.floor(random.random() * 63))  # Multiply by 63, not 64
        else:
            i = 11
            while i >= 0 and cls.lastRandChars[i] == 62:  # Compare with 62, not 63
                cls.lastRandChars[i] = 0
                i -= 1
            if i >= 0:  # check that i is still within range
                cls.lastRandChars[i] = min(cls.lastRandChars[i] + 1, 62)  # Increment by 1, but ensure it's <= 62, not 63
            else:  # if i is -1, then all previous random chars were 62, so we reset them all and do not increment any of them
                cls.lastRandChars = [0]*12

        for i in range(12):
            push_id += cls.PUSH_CHARS[cls.lastRandChars[i]]

        assert len(push_id) == 20, "Length should be 20."

        return push_id
