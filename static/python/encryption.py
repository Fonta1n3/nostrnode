import rncryptor


def encrypt(data, password):
    cryptor = rncryptor.RNCryptor()
    return cryptor.encrypt(data, password)


def decrypt(encrypted_data, password):
    cryptor = rncryptor.RNCryptor()
    return cryptor.decrypt(encrypted_data, password)