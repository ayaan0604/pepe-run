import json

class SavesManager:
    def __init__(self):
        self.filePath = "data/saves.json"
    

    def read(self):
        with open(self.filePath, 'r') as f:
            return json.load(f)
        
    def write(self, data):
        with open(self.filePath, 'w') as f:
            json.dump(data, f, indent=4)

    def getHighScore(self):
        return self.read()["highScore"]
    
    def updateHighScore(self, score):
        data = self.read()
        data["highScore"] = score
        self.write(data=data)

if __name__ == "__main__":
    sm = SavesManager()
    sm.updateHighScore(100)
    print(sm.getHighScore())