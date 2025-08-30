"""
Mock Redis client for development without Redis server
"""

class MockRedisClient:
    """Mock Redis client that simulates Redis operations"""
    
    def __init__(self):
        self.data = {}
        print("Using Mock Redis Client (no Redis server required)")
    
    def delete_all_keys(self):
        """Mock delete all keys"""
        self.data.clear()
        return True
    
    def set_key(self, key, value, ex=None):
        """Mock set key"""
        self.data[key] = value
        return True
    
    def get_key(self, key):
        """Mock get key"""
        return self.data.get(key)
    
    def delete_key(self, key):
        """Mock delete key"""
        if key in self.data:
            del self.data[key]
            return True
        return False
    
    def exists(self, key):
        """Mock exists"""
        return key in self.data
    
    def flushdb(self):
        """Mock flushdb"""
        self.data.clear()
        return True

# Create global instance
mock_redis = MockRedisClient()
