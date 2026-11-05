import re, getpass
def run():
    value=getpass.getpass('Password to assess (not stored): ')
    checks=[len(value)>=12,bool(re.search(r'[a-z]',value)),bool(re.search(r'[A-Z]',value)),bool(re.search(r'\d',value)),bool(re.search(r'[^A-Za-z0-9]',value))]
    print('Estimated strength:', ['Very weak','Weak','Fair','Good','Strong','Very strong'][sum(checks)])
    print('Use unique passwords and a password manager.')
