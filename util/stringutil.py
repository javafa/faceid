import hashlib

def generateHashCode(word:str) :
    sha = hashlib.new('md5')
    encoded = word.encode('utf-8')
    sha.update(encoded)
    return sha.hexdigest()