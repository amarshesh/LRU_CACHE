class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.lruArray = []

    def shift(self, index: int, key: int):
        for i in range(index, len(self.lruArray) - 1):
            self.lruArray[i] = self.lruArray[i + 1]

        if len(self.lruArray) == self.capacity:
            self.lruArray[-1] = key
        else:
            self.lruArray.append(key)

    def printLru(self):
        print(self.lruArray)

    def get(self, key: int) -> int:
        index = -1

        for i in range(len(self.lruArray)):
            if key == self.lruArray[i]:
                index = i
                break

        if index == -1:
            return -1

        self.shift(index, key)
        return key

    def put(self, key: int, value: int) -> None:
        index = -1
        for i in range(len(self.lruArray)):
            if key == self.lruArray[i]:
                index = i
                break
        if index != -1:
            self.shift(index, key)
        else:
            if len(self.lruArray) < self.capacity:
                self.lruArray.append(key)
            else:
                self.shift(0, key)


lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
lru.printLru()
print(lru.get(1))
lru.printLru()
lru.put(3, 3)
lru.printLru()
print(lru.get(2))
lru.printLru()