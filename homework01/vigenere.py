def encrypt_vigenere(plaintext: str, keyword: str) -> str:

    alpha = 'абвгдеёжзийклмнопрстуфхчшщьыъэюя'
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

    plaintext = ""
    alpha = 'абвгдеёжзийклмнопрстуфхчшщьыъэюя'
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

if __name__ == "__main__":
    plaintext=input("Введите текст:\n")
    keyword=input("Введите ключ:\n")
    cyphertext=encrypt_vigenere(plaintext,keyword)
    print(f"Ваш зашифрованный текст: {cyphertext}")
