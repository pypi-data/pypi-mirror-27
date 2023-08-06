## bjphonenumber
A fast minimal module to validate Beninese mobile phone numbers.

### Installation
```
$ pip install bj_phone_number
```

### Usage

This module assumes that you already know that Benines numbers are prefixed by `+229` and you should not expect your users to type that. Instead your UI should look something like this.

```
     |**********************|
+229 |  phone number here   |
     |**********************|
```
```
from bj_phone_number import validate_number

number = "66526416"

print(validate_number(number)) # validate
```


