import sys
import hashlib

"""
This class will be used in order to check the proof-of-work.

Input: headerFile originalFile

headerFile = contains the header to be checked
originalFile = contains the original message

Author: Chris Zachariah
"""

# number of bytes to read from file at a time
BUF_SIZE = 65536


def main():
    # check number of arguments
    if len(sys.argv) != 3:
        print("Usage: ./pow-check headerFile originalFile")
        exit()

    # read from the headerFile and collect all the info needed
    initialHash = ''
    proof = ''
    finalHash = ''
    leading = ''
    numReceived = 0
    try:
        with open(sys.argv[1], "r") as f:
            for line in f:
                if "Initial-hash:" in line:
                    if initialHash == '':
                        initialHash = line
                        numReceived = numReceived + 1
                    if numReceived == 4:
                        break
                if "Proof-of-work:" in line:
                    if proof == '':
                        proof = line
                        numReceived = numReceived + 1
                    if numReceived == 4:
                        break
                if "Hash:" in line:
                    if finalHash == '':
                        finalHash = line
                        numReceived = numReceived + 1
                    if numReceived == 4:
                        break
                if "Leading-bits:" in line:
                    if leading == '':
                        leading = line
                        numReceived = numReceived + 1
                    if numReceived == 4:
                        break
        f.close()
    except IOError:
        print("Error reading from", sys.argv[1])
        exit()

    # clean up all the data collected
    if initialHash == '':
        cleanedInitialHash = ''
    else:
        initialHash = initialHash.split(":")
        cleanedInitialHash = initialHash[1].strip()

    if proof == '':
        cleanedProof = ''
    else:
        proof = proof.split(":")
        cleanedProof = proof[1].strip()

    if finalHash == '':
        cleanedFinalHash = ''
    else:
        finalHash = finalHash.split(":")
        cleanedFinalHash = finalHash[1].strip()

    if leading == '':
        cleanedLeading = ''
    else:
        leading = leading.split(":")
        cleanedLeading = leading[1].strip()

    hasPassed = True

    # read from the originalFile and hash the message
    sha256 = hashlib.sha256()
    try:
        with open(sys.argv[2], "rb") as f:
            while True:
                bytesBuf = f.read(BUF_SIZE)
                if not bytesBuf:
                    break
                sha256.update(bytesBuf)
        f.close()
    except IOError:
        print("Error reading from", sys.argv[2])
        exit()
    messageHash = sha256.hexdigest()

    # see if the header has an initial hash and then check if it matches the file's hash
    if len(cleanedInitialHash) == 0:
        hasPassed = False
        print("error: Missing Initial-hash from header.")
    else:
        if messageHash != cleanedInitialHash:
            hasPassed = False
            print("error: Header's Initial-hash does not match the file's hash")

    # make sure the header has a proof of work
    if len(cleanedProof) == 0:
        hasPassed = False
        print("error: Missing Proof-of-work from header.")
        exit()

    # compute the hash with the proof-of-work
    proof = cleanedProof
    conCat = proof + messageHash
    result = hashlib.sha256(conCat.encode()).hexdigest()

    # see if the header has the finalHash and then check if it matches with the result
    if len(cleanedFinalHash) == 0:
        hasPassed = False
        print("error: Missing Hash from header")
    else:
        if result != cleanedFinalHash:
            hasPassed = False
            print("error: Header's Hash does not match the computed hash using the proof-of-work")

    # compute the number of leading 0s
    end_length = len(result) * 4
    hex_as_int = int(result, 16)
    hex_as_binary = bin(hex_as_int)
    padded_binary = hex_as_binary[2:].zfill(end_length)
    computedLeading = str(padded_binary.find('1'))

    # see if the header has the leading 0s and then check if it matches with the computed value of leading 0s
    if len(cleanedLeading) == 0:
        hasPassed = False
        print("error: Missing Leading-bits in header")
    else:
        if computedLeading != cleanedLeading:
            hasPassed = False
            print("error: Header's Leading-bits (" + cleanedLeading + ") does not match computed leading bits (" + computedLeading + ")")

    # pass (no errors), fail(one or more errors)
    if hasPassed is True:
        print("pass")
    else:
        print("fail")


if __name__ == "__main__":
    main()
