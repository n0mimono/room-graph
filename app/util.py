import hashlib
import json


class Util:
    @staticmethod
    def get_sig(s: str) -> str:
        key = 'AFsBK_NxRbLU'
        b = (s + key).encode('utf-8')
        return hashlib.sha224(b).hexdigest()
