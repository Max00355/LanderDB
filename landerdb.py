import json
import os

class Connect:

    def __init__(self, db_file):
        self.db = db_file
        self.json_data = {}
        # allows find to be called multiple times, without 
        # re-reading from disk unless a change has occured
        self.stale = True
        if not os.path.exists(self.db):
           self._save()

    def _load(self):
        if self.stale:
            with open(self.db, 'rb') as fp:
                fp = fp.read().decode("hex")
                self.json_data = json.loads(fp)

    def _save(self):
        with open(self.db, 'wb') as fp:
            f = json.dumps(self.json_data)
            fp.write(f.encode("hex"))
            self.stale = True

    def insert(self, collection, data):
        self._load()
        if collection not in self.json_data:
            self.json_data[collection] = []
        self.json_data[collection].append(data)
        self._save()

    def remove(self, collection, data):
        self._load()
        if collection not in self.json_data:
            return False
        self.json_data[collection].remove(data) #Will only delete one entry
        self._save()
            
    def find(self, collection, data):
        self._load()
        if collection not in self.json_data:
            return False
        output = []
        for x in self.json_data[collection]:
            if data != "all":
                for y in data:
                    try:
                        if data[y] == x[y]:
                            output.append(x)
                    except KeyError:
                        continue
            else:
                output.append(x)
        return output
    


