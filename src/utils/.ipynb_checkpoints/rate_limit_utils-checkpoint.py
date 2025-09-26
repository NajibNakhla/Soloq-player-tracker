import time

def check_and_sleep_rate_limit(rate_limit_info, threshold=0.8, sleep_duration=10):
    """
    Checks if we're approaching rate limit and sleeps if necessary.
    
    Args:
        rate_limit_info: Dictionary with 'used' and 'max' keys
        threshold: Percentage of limit at which to trigger sleep (0.8 = 80%)
        sleep_duration: How long to sleep when approaching limit
    """
    if rate_limit_info["used"] >= (rate_limit_info["max"] * threshold):
        print(f"   Approaching rate limit ({rate_limit_info['used']}/{rate_limit_info['max']}). Sleeping for {sleep_duration}s...")
        time.sleep(sleep_duration)
        return True
    return False

def calculate_sleep_time(rate_limit_info, requests_per_second=1.0):
    """
    Calculates dynamic sleep time based on rate limit remaining.
    """
    remaining = rate_limit_info["max"] - rate_limit_info["used"]
    time_remaining = 60  # Assuming 1-minute window (adjust based on Riot's actual window)
    
    if remaining <= 0:
        return 10  # Emergency sleep if we hit limit
    
    # Calculate how long to sleep to stay under limit
    safe_sleep = max(0.1, time_remaining / remaining)
    return min(safe_sleep, 2.0)  # Cap at 2 seconds max