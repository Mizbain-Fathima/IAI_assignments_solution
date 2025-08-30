"""
Script to disable Redis requirements in XAgent
"""

import os
import sys
from pathlib import Path

def create_directories_if_needed():
    """Create necessary directories if they don't exist"""
    exts_dir = Path("XAgent/XAgentServer/exts")
    exts_dir.mkdir(parents=True, exist_ok=True)
    return exts_dir.exists()

def create_mock_redis():
    """Create a mock Redis client"""
    mock_redis_file = Path("XAgent/XAgentServer/exts/mock_redis.py")
    
    mock_redis_content = '''
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
'''
    with open(mock_redis_file, 'w') as f:
        f.write(mock_redis_content)
    
    return mock_redis_file.exists()

def patch_global_val():
    """Patch global_val.py to use mock Redis"""
    global_val_file = Path("XAgent/XAgentServer/application/global_val.py")
    
    if not global_val_file.exists():
        print(f"Error: {global_val_file} not found")
        return False
    
    with open(global_val_file, 'r') as f:
        content = f.read()
    
    # Check if already patched
    if "MockRedisClient" in content:
        print("global_val.py already patched")
        return True
    
    # Replace Redis import with mock
    new_content = content.replace(
        "from XAgentServer.exts.redis_ext import RedisClient",
        "# from XAgentServer.exts.redis_ext import RedisClient\n"
        "from XAgentServer.exts.mock_redis import MockRedisClient"
    )
    
    # Replace Redis initialization
    new_content = new_content.replace(
        "redis = RedisClient()",
        "redis = MockRedisClient()"
    )
    
    with open(global_val_file, 'w') as f:
        f.write(new_content)
    
    print("global_val.py patched successfully")
    return True

def patch_redis_ext():
    """Create a minimal redis_ext that uses mock"""
    redis_ext_file = Path("XAgent/XAgentServer/exts/redis_ext.py")
    
    if not redis_ext_file.exists():
        print("redis_ext.py not found - creating minimal version")
        redis_ext_content = '''
"""
Minimal Redis extension that uses mock client
"""

from .mock_redis import MockRedisClient

class RedisClient:
    def __init__(self):
        self.client = MockRedisClient()
    
    def delete_all_keys(self):
        return self.client.delete_all_keys()
    
    def set_key(self, key, value, ex=None):
        return self.client.set_key(key, value, ex)
    
    def get_key(self, key):
        return self.client.get_key(key)
    
    def delete_key(self, key):
        return self.client.delete_key(key)
    
    def exists(self, key):
        return self.client.exists(key)
    
    def flushdb(self):
        return self.client.flushdb()

# Global instance
redis_client = RedisClient()
'''
        with open(redis_ext_file, 'w') as f:
            f.write(redis_ext_content)
    
    return True

def disable_redis():
    """Main function to disable Redis requirements"""
    print("Disabling Redis requirements in XAgent...")
    
    # Create directories if needed
    if not create_directories_if_needed():
        print("Failed to create directories")
        return False
    
    # Create mock Redis
    if not create_mock_redis():
        print("Failed to create mock Redis")
        return False
    
    # Patch global_val.py
    if not patch_global_val():
        print("Failed to patch global_val.py")
        return False
    
    # Ensure redis_ext.py exists
    patch_redis_ext()
    
    print("Redis requirements disabled successfully")
    return True

if __name__ == "__main__":
    success = disable_redis()
    if success:
        print("\nXAgent should now work without Redis server!")
        print("Run: python -c \"from XAgentServer.application.global_val import redis; print('Redis mock working')\"")
    else:
        print("\nFailed to disable Redis requirements")
        sys.exit(1)