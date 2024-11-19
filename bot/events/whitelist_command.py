import requests

# API information
API_BASE_URL = "https://mcprofile.io/api/v1/java/username"
BEDROCK_API_BASE_URL = "https://mcprofile.io/api/v1/bedrock/gamertag"
API_KEY = "8c874b05-4c71-43fe-a416-eb670b3aeb0a"

# Attempt to fetch profile data
def get_mc_profile(user):
    """Gets any possible minecraft profile of user."""
    profile = get_java_profile(user)
    if (profile == None):
        profile = get_bedrock_profile(user)
    return profile

# Function to fetch data for a Java username
def get_java_profile(username):
    """Gets Java specific user profile."""
    url = f"{API_BASE_URL}/{username}"
    headers = {
        "x-api-key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            # Java profile not found
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# Function to fetch Bedrock profile
def get_bedrock_profile(gamertag):
    """Gets Bedrock specific user profile."""
    url = f"{BEDROCK_API_BASE_URL}/{gamertag}"
    headers = {
        "x-api-key": API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            # Bedrock profile not found
            return None
        
    except Exception as e:
        print(f"An error occurred during Bedrock lookup: {e}")
        return None
    

def get_whitelist_dic(user):
    """Gets minecraft whitelist data of user as a dictionary."""
    # Try Java profile first
    profile = get_java_profile(user)
    if profile is not None:
        return {
            "version": "java",
            "username": profile.get("username", ""),
            "floodgateuid": profile.get("floodgateuid", "")
        }

    # Try Bedrock profile if Java is not found
    profile = get_bedrock_profile(user)
    if profile is not None:
        return {
            "version": "bedrock",
            "username": profile.get("gamertag", ""),
            "floodgateuid": profile.get("floodgateuid", "")
        }

    # Return default data if no profile is found
    return {
        "version": "unknown",
        "username": "",
        "floodgateuid": ""
    }
        

def get_whitelist_delim(user):
    """Gets minecraft whitelist data of user as a delimited string."""
    # Try Java profile first
    profile = get_java_profile(user)
    if profile is not None:
        data = ["java", user, ""]
        return "|".join(data)

    # Try Bedrock profile if Java is not found
    profile = get_bedrock_profile(user)
    if profile is not None:
        data = ["bedrock", user, profile.get("floodgateuid", "")]
        return "|".join(data)

    # Return default data if no profile is found
    return "unknown||"