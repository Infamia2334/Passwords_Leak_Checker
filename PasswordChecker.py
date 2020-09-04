
import sys
import requests
import hashlib #DO SHA1 hashing


def request_api_data(query):
#Request Data from API
    url = "https://api.pwnedpasswords.com/range/" + query                               
    result = requests.get(url)
    if result.status_code != 200:
       raise RuntimeError(f"Cancerous Error Code: {result.status_code}, Check the API and try again mofo")  
    
    return result

def get_password_breach_counts(hashes, hashed_password): 
#Get the number of times hashed_password was breached
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashed_password:
            return count
    return 0

def pwned_api_check(password):
#Check password if it exists in API response
    sha1_pass = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()              #Hashing the Password Using Sha1 hashing
    first5char_pass, tail_pass = sha1_pass[:5], sha1_pass[5:]                           #Grabbing The first 5 Charachters of the hashed password and the rest of the charachters
    response = request_api_data(first5char_pass)
    # print(first5char_pass, tail_pass) 
    return get_password_breach_counts(response, tail_pass)



def main(args) :
    for password in args:
        count = pwned_api_check(password)
        if(count):
            print(f"Alas!Looks like your password:{password} was breached {count} times....Please Consider changing it(Also you are retarded lol)")
        else:
            print("Password was never Breached....at least you don't have shit for brains")


main(sys.argv[1:])