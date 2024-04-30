from subprocess import check_output
from tabulate import tabulate

def get_profiles():
    command = "netsh wlan show profile"
    try:
        profiles = check_output(command, shell=False).decode()
        return profiles
    except:
        print('Error getting profiles')
        return 0

def parse_profiles(profiles):
    parsed_profiles = []

    profile_list = profiles.split(sep='\n')
    for profile in profile_list[9:]:
        profile = profile[27:]
        profile = profile.rstrip()
        if len(profile) > 0:
            parsed_profiles.append(profile)
    
    return parsed_profiles
        
def get_passwords(profile_list):
    passwords = {}
    for profile in profile_list:
        if len(profile) == 0:
            continue

        profile_formatted = (f'"{profile}"')
        command = f'netsh wlan show profile {profile_formatted} key="clear"'
        try: 
            profile_details = check_output(command, shell=False).decode()   # enter netsh cmd
            key_content_address = profile_details.find('Key Content')       # find Key Content address
            if key_content_address == -1:                                   # skip if no Key Content
                print(f'No password stored for {profile}')
                continue

            profile_details = profile_details[key_content_address + 25:]    # slice everything before the Key Content line
            line_break_address = profile_details.find('\n')                 # find next newline
            profile_details = profile_details[:line_break_address]          # slice everything after the newline
            password = profile_details.rstrip()
            passwords[profile] = password
        except:
            print(f'Error getting password for {profile}')

    return passwords

def generate_table(passwords):
    rows = []
    for entry in passwords:
        row = [entry, passwords[entry]]
        rows.append(row)
    table = tabulate(rows,headers=['SSID','Password'])
    return table


def main():

    profiles = get_profiles()
    if not profiles:
        print('Exiting wifi_dumper...')

    profile_list = parse_profiles(profiles)
    passwords = get_passwords(profile_list)

    table = generate_table(passwords)
    print('\n' + table)

    return passwords

main()