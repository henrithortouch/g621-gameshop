from hashlib import md5

from gameshop.secret_key import secret_key

def getPID(checksum):
    return checksum.split(",")[1].split(":")[1].strip()

def getChecksum(pid, ref, result):
    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum

def checkValidity(data):
    pid = data["pid"][0]
    ref = data["ref"][0]
    result = data["result"][0]

    checksum = getChecksum(pid, ref, result)
    validate_checksum = data["checksum"][0]

    validity = validate_checksum == checksum
    return validity
