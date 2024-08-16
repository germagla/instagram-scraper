import instaloader
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Variables
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
session_file = f"session-{username}"

# Initialize Instaloader
L = instaloader.Instaloader()

def login_instaloader_cli():
    try:
        # Run the Instaloader CLI login command
        result = subprocess.run(
            ['instaloader', '-l', username],
            input=f"{password}\n",  # Pass password via stdin
            text=True,  # Treat input/output as strings
            capture_output=True  # Capture stdout and stderr
        )

        if result.returncode == 0:
            print("Instaloader CLI login successful.")
            # Save the session file
            # This assumes the session file is saved automatically by Instaloader CLI
        else:
            print("Instaloader CLI login failed:\n", result.stdout, result.stderr)
            raise RuntimeError("Login failed")

    except Exception as e:
        print("Exception occurred during CLI login:", str(e))
        raise

def load_session():
    try:
        if not os.path.exists(session_file):
            login_instaloader_cli()

        L.load_session_from_file(username, session_file)
        print("Session loaded successfully for user", username)
    except Exception as e:
        print("Failed to load session from file:", str(e))
        raise

def get_followers(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print("Fetched followers for", username)
        return set(profile.get_followers())
    except Exception as e:
        print("Error fetching followers for", username, ":", str(e))
        return set()

def common_followers(usernames):
    if not usernames:
        print("No usernames provided")
        return []

    common = get_followers(usernames[0])

    for username in usernames[1:]:
        common &= get_followers(username)

    print("Common followers retrieved for usernames:", ", ".join(usernames))
    return list(common)

def save_to_file(usernames, followers):
    try:
        # Ensure the results directory exists
        os.makedirs('results', exist_ok=True)

        # Create a suitable filename based on the usernames
        filename = f"results/common_followers_{'_'.join(usernames)}.txt"

        # Write the followers to the file
        with open(filename, 'w') as file:
            for follower in followers:
                file.write(f"{follower.username}\n")

        print("Common followers saved to", filename)
    except Exception as e:
        print("Error saving followers to file:", str(e))

def main():
    # Prompt for usernames at runtime
    usernames_input = input("Enter Instagram usernames separated by commas: ")
    usernames = [username.strip() for username in usernames_input.split(',')]

    # Load session
    load_session()

    # Get the common followers
    common_followers_list = common_followers(usernames)

    # Save the results to a file
    save_to_file(usernames, common_followers_list)

if __name__ == "__main__":
    main()
