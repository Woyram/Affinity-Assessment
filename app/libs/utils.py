import hashlib
import random
from random import choice
import random
import re
from random import choice


class Utilites():
    """docstring for log"""
    
    '''
    Writing into files
    '''
    def generate_password(self, length=10):
        """
        Function to generate a password
        """

        char_set = {
                 'small': 'abcdefghijklmnopqrstuvwxyz',
                 'nums': '0123456789',
                 'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 'special': '^!\$%&/()=?+~#-_.:,;|\\'
                }

        password = []

        while len(password) < length:
            key = choice(list(char_set.keys()))
            # a_char = str(urandom(1))
            a_char = choice(char_set[key])
            if a_char in char_set[key]:
                if self.check_prev_char(password, char_set[key]):
                    continue
                else:
                    password.append(a_char)
        return ''.join(password)

    @staticmethod
    def retype_msisdn(msisdn: str):
        if isinstance(msisdn, str) == False: raise(ValueError('MSISDN must be a string type'))
        
        return "233" + msisdn[-9::]

    def check_prev_char(self, password, current_char_set):
        """
        Function to ensure that there are no consecutive 
        UPPERCASE/lowercase/numbers/special-characters.
        """

        index = len(password)
        if index == 0:
            return False
        else:
            prev_char = password[index - 1]
            if prev_char in current_char_set:
                return True
            else:
                return False

    def password_complexity_check(self, password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # Strength Value
        strength = 10

        # calculating the length
        length_error = len(password) < 8
        if length_error == True:
            strength -= 2

        # searching for digits
        digit_error = re.search(r"\d", password) is None
        if digit_error == True:
            strength -= 2

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        if uppercase_error == True:
            strength -= 2

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        if lowercase_error == True:
            strength -= 2

        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~@"+r'"]', password) is None
        if symbol_error == True:
            strength -= 2

        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

        return {
            'password_ok' : password_ok,
            'length_error' : length_error,
            'digit_error' : digit_error,
            'uppercase_error' : uppercase_error,
            'lowercase_error' : lowercase_error,
            'symbol_error' : symbol_error,
            'strength': strength
        }


    '''
    Writing into files
    '''

    def checksum_generator(self, merchant_ip, merchant_id, total_amount):
        info = '{0}{1}{2}'.format(merchant_ip, merchant_id, total_amount)
        salt_size = 6
        chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        _salt = ''.join(random.choice(chars) for i in range(salt_size))
        _checksum = hashlib.md5(info.encode('utf-8')).hexdigest()
        _checksum = list(_checksum)
        _checksum.insert(5, _salt)
        _checksum = ''.join(_checksum)
        return _checksum
