import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:4000/api/chat"  
TONE_API_URL="http://127.0.0.1:4000/api/tone"

def test_input_validation(api_url):
    """
    Test the API for input validation against malicious inputs.
    """
    print("\n--- Input Validation Tests ---")
    test_inputs = [
        {"chat": "'; DROP TABLE users;--", "expected_behavior": "Sanitized or error-handled input."},
        {"chat": "<script>alert('Hacked!')</script>", "expected_behavior": "Sanitized or error-handled input."},
        {"chat": "Normal input text.", "expected_behavior": "Respond correctly."}
    ]
    for test in test_inputs:
        try:
            response = requests.post(api_url, json={"chat": test["chat"]})
            if response.status_code == 200:
                print(f"Input: {test['chat']} - Passed")
            else:
                print(f"Input: {test['chat']} - Failed")
        except Exception as e:
            print(f"Input: {test['chat']} - Error: {e}")


def test_dos(api_url):
    """
    Test the API for denial-of-service (DoS) vulnerabilities.
    """
    print("\n--- DoS Tests ---")
    # Large payload test
    large_input = {"chat": "A" * 100000}
    try:
        response = requests.post(api_url, json=large_input, timeout=5)
        if response.status_code == 200:
            print("DoS Large Payload Test: Passed")
        else:
            print("DoS Large Payload Test: Failed")
    except requests.exceptions.RequestException as e:
        print(f"DoS Large Payload Test: Failed (Error: {e})")

    # Rapid request test
    print("\nSimulating 100 rapid requests...")
    for i in range(100):  # Simulate 100 rapid requests
        try:
            response = requests.post(api_url, json={"chat": "Test"}, timeout=1)
            if response.status_code != 200:
                print(f"DoS Rapid Requests Test: Failed on request {i + 1}")
                break
        except requests.exceptions.RequestException as e:
            print(f"DoS Rapid Requests Test: Failed on request {i + 1} (Error: {e})")
            break
    else:
        print("DoS Rapid Requests Test: Passed")


def test_data_privacy(api_url):
    """
    Test the API for data privacy issues (e.g., logging sensitive data).
    """
    print("\n--- Data Privacy Tests ---")
    sensitive_input = {"chat": "My password is password123"}
    try:
        response = requests.post(api_url, json=sensitive_input)
        if response.status_code == 200:
            print("Privacy Test: Passed (Response successful, ensure logs are private).")
        else:
            print("Privacy Test: Failed (Unexpected response).")
    except Exception as e:
        print(f"Privacy Test: Error: {e}")
    

def test_input_validation_tone(api_url):
    """
    Test the API for input validation against malicious inputs.
    """
    print("\n--- Input Validation Tests ---")
    test_inputs = [
        {"chat": "'; DROP TABLE users;--", "expected_behavior": "Sanitized or error-handled input."},
        {"chat": "<script>alert('Hacked!')</script>", "expected_behavior": "Sanitized or error-handled input."},
        {"chat": "Normal input text.", "expected_behavior": "Respond correctly."}
    ]
    for test in test_inputs:
        try:
            response = requests.post(api_url, json={"chat": test["chat"]})
            if response.status_code == 200:
                print(f"Input: {test['chat']} - Passed")
            else:
                print(f"Input: {test['chat']} - Failed")
        except Exception as e:
            print(f"Input: {test['chat']} - Error: {e}")


def test_dos_tone(api_url):
    """
    Test the API for denial-of-service (DoS) vulnerabilities.
    """
    print("\n--- DoS Tests ---")
    # Large payload test
    large_input = {"chat": "A" * 100000}
    try:
        response = requests.post(api_url, json=large_input, timeout=5)
        if response.status_code == 200:
            print("DoS Large Payload Test: Passed")
        else:
            print("DoS Large Payload Test: Failed")
    except requests.exceptions.RequestException as e:
        print(f"DoS Large Payload Test: Failed (Error: {e})")

    # Rapid request test
    print("\nSimulating 100 rapid requests...")
    for i in range(100):  # Simulate 100 rapid requests
        try:
            response = requests.post(api_url, json={"chat": "Test"}, timeout=1)
            if response.status_code != 200:
                print(f"DoS Rapid Requests Test: Failed on request {i + 1}")
                break
        except requests.exceptions.RequestException as e:
            print(f"DoS Rapid Requests Test: Failed on request {i + 1} (Error: {e})")
            break
    else:
        print("DoS Rapid Requests Test: Passed")


def test_data_privacy_tone(api_url):
    """
    Test the API for data privacy issues (e.g., logging sensitive data).
    """
    print("\n--- Data Privacy Tests ---")
    sensitive_input = {"chat": "My password is password123"}
    try:
        response = requests.post(api_url, json=sensitive_input)
        if response.status_code == 200:
            print("Privacy Test: Passed (Response successful, ensure logs are private).")
        else:
            print("Privacy Test: Failed (Unexpected response).")
    except Exception as e:
        print(f"Privacy Test: Error: {e}")


def main():
    """
    Run all security and privacy tests.
    """
    print("Starting Security and Privacy Tests...\n")
    
    # Input Validation Tests
    test_input_validation(API_URL)
    
    # DoS Tests
    test_dos(API_URL)
    
    # Data Privacy Tests
    test_data_privacy(API_URL)
    
    print("Starting Security Tests for Tone Detection API...\n")
    
    # Input Validation Tests
    test_input_validation_tone(TONE_API_URL)
    
    # DoS Tests
    test_dos_tone(TONE_API_URL)
    
    # Data Privacy Tests
    test_data_privacy_tone(TONE_API_URL)
    
    print("\nAll Tests Completed.")


if __name__ == "__main__":
    main()
