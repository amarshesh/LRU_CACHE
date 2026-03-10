from datetime import date
import threading
from time import time

print( f"Cache hit : Its tells us how many times we got the value from cache when we requested for it")
print( f"Cache Misses : Its tells us how many times we did not get the value from cache when we requested for it")
print( f"hit rate : Its tells us the percentage of times we got the value from cache when we requested for it")
print( f"Eviction : Its tells us how many times we removed the least recently used item from cache when we added a new item and the cache was full")
class DoubleLinkedListNode:
    def __init__(self, value, key, ttl=None):
        self.value = value
        self.key = key
        self.prev = None
        self.next = None
        self.entry_time = time.time()
        self.expiry_time = ttl
       



class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.NodesList = {}
        self.cache_hit = 0
        self.cache_misses = 0
        self.evection = 0
        # use RLock so nested calls (get -> remove_node -> add_node) can re-acquire
        self.lock = threading.RLock()

        self.head = DoubleLinkedListNode(-1, -1)
        self.tail = DoubleLinkedListNode(-1, -1)

        # connect sentinels
        self.head.next = self.tail
        self.tail.prev = self.head


    def add_node(self, node):
        # perform full pointer update under lock to avoid concurrent corruption
        with self.lock:
            # don't try to add sentinels
            if node is self.head or node is self.tail:
                return
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node


    def remove_node(self, node):
        # perform full pointer update under lock to avoid concurrent corruption
        with self.lock:
            # never remove sentinels
            if node is self.head or node is self.tail:
                return
            prev_node = node.prev
            next_node = node.next
            prev_node.next = next_node
            next_node.prev = prev_node
            node.prev = None
            node.next = None

    def get(self, key):
        with self.lock:
            if key not in self.NodesList:
                self.cache_misses += 1
                return -1

            node = self.NodesList[key]
            current_time = time.time()

            if node.expiry_time is not None and current_time - node.entry_time > node.expiry_time:
                self.remove_node(node)
                del self.NodesList[key]
                self.cache_misses += 1
                return -1

            self.remove_node(node)
            self.add_node(node)
            self.cache_hit += 1
            return node.value


    def put(self, key, value, ttl=None):
        with self.lock:
            if key in self.NodesList:
                node = self.NodesList[key]
                node.value = value
                node.expiry_time = ttl
                node.entry_time = time.time()
                
                self.remove_node(node)
                self.add_node(node)
            else:
                if len(self.NodesList) == self.capacity:
                    lru = self.tail.prev
                    if lru is self.head or lru is self.tail:
                        pass
                    else:
                        self.remove_node(lru)
                        if lru.key in self.NodesList:
                            del self.NodesList[lru.key]
                            self.evection += 1
                new_node = DoubleLinkedListNode(value, key, ttl)
                self.NodesList[key] = new_node
                self.add_node(new_node)

    def state(self):
        total = self.cache_hit + self.cache_misses
        hit_rate = self.cache_hit / total if total else 0
        return {
            "cache_hit": self.cache_hit,
            "cache_misses": self.cache_misses,
            "hit_rate": hit_rate,
            "evection": self.evection
        }
    
    def printLru(self):
        with self.lock:
            curr = self.head.next
            while curr != self.tail:
                print(f"{curr.key}:{curr.value}", end=" ")
                curr = curr.next
            print()


import time
print("\n---- TTL TEST ----")

lru = LRUCache(2)

lru.put("A", 10, ttl=2)
print("GET A:", lru.get("A"))

time.sleep(3)

print("GET A after expiry:", lru.get("A"))

lru.printLru()

print( f"State : {lru.state()}")

 