def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    ciphertext = ""
    lentext=len(plaintext)
    lenkey=len(keyword)
    for i in range(lentext):
        if plaintext[i].lower() in alpha:
            if plaintext[i] in alpha:
                ciphertext += alpha[(alpha.find(plaintext[i])+alpha.find(keyword[i%lenkey].lower()))%len(alpha)]
            else:
                ciphertext += alpha[(alpha.find(plaintext[i].lower())+alpha.find(keyword[i%lenkey].lower()))%len(alpha)].upper()
        else:
            ciphertext+=plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    lentext=len(ciphertext)
    lenkey=len(keyword)
    for i in range(lentext):
        if ciphertext[i].lower() in alpha:
            if ciphertext[i] in alpha:
                plaintext += alpha[alpha.find(ciphertext[i])-alpha.find(keyword[i%lenkey].lower())]
            else:
                plaintext += alpha[alpha.find(ciphertext[i].lower())-alpha.find(keyword[i%lenkey].lower())].upper()
        else:
            plaintext+=ciphertext[i]
    return plaintext
