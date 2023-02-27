import base64
import hashlib
from django.conf import settings


def mask_hash(hash, show=6, char="*"):
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked


class PasswordUtil:
    """
    使用 PBKDF2 算法的安全密码散列

    配置为使用 PBKDF2 + HMAC + SHA256。
    结果是一个 64 字节的二进制字符串。迭代可能会改变
    安全，但如果更改 SHA256，则必须重命名算法。
    """

    algorithm = settings.ENCODE_PASSWORD_SETTINGS["ALGORITHM"]
    iterations = settings.ENCODE_PASSWORD_SETTINGS["ITERATIONS"]
    salt = settings.ENCODE_PASSWORD_SETTINGS["SALT"]

    digest = hashlib.sha256

    def encode(self, password, salt=None, iterations=None):
        """
        使用 PBKDF2 算法生成密码散列
        """
        salt = salt or self.salt

        assert password is not None
        assert salt and "$" not in salt
        iterations = iterations or self.iterations
        hash = hashlib.pbkdf2_hmac(
            self.digest().name,
            bytes(password, "UTF-8"),
            bytes(salt, "UTF-8"),
            iterations,
        )
        # 解码 base64 编码的二进制散列
        hash = base64.b64encode(hash).decode("ascii").strip()
        return f"{self.algorithm}${iterations}${salt}${hash}"

    def decode(self, encoded):
        """
        解码一个密码散列，返回一个字典
        """
        algorithm, iterations, salt, hash = encoded.split("$", 3)
        assert algorithm == self.algorithm
        return {
            "algorithm": algorithm,
            "hash": hash,
            "iterations": int(iterations),
            "salt": salt,
        }

    def verify(self, password, encoded):
        """
        验证密码是否与散列匹配
        """
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded["salt"], decoded["iterations"])
        return bytes(encoded, "UTF-8") == bytes(encoded_2, "UTF-8")

    def safe_summary(self, encoded):
        """
        返回一个安全的密码散列摘要
        """
        decoded = self.decode(encoded)
        return {
            "algorithm": decoded["algorithm"],
            "iterations": decoded["iterations"],
            "salt": mask_hash(decoded["salt"]),
            "hash": mask_hash(decoded["hash"]),
        }


# if __name__ == "__main__":
#     print(
#         PasswordUtil.verify(
#             PasswordUtil(),
#             "heyan5201314",
#             "pbkdf2_sha256$100000$123456$I3cOmsILBnMRUsQFTlDB3y5XMEPH8J0xeROQzdeCtao=",
#         )
#     )
