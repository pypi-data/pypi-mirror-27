import re, sys

# A bj phone number must have 8 digits
# And must start with 60, 61, 62, 64, 65, 66, 67, 90, 93, 94, 95, 96, 97

regexp = r"^([6]+[0-2|4-7])"
regexp_ = r"^(([9]+[0|3-7]))"

def validate_number(phone_number):
    if len(phone_number) != 8:
        return False
    else:
        if re.match(regexp, phone_number) is not None or re.match(regexp_, phone_number) is not None:
            return True
        else:
            return False

def main():
    return validate_number(sys.argv[-1])

if __name__ == '__main__':
    main()
