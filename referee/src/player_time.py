import rospy

class PlayerTime():
    def __init__(self, currentRound, currentSector, totalTime, lastSectorTime):
        self.currentRound = currentRound
        self.currentSector = currentSector
        self.totalTime = totalTime
        self.lastSectorTime = lastSectorTime

    def toString(self):
        return str(self.currentRound) + ", " + str(self.currentSector) + ", " + str(self.totalTime) + ", " + str(self.lastSectorTime)
    def __str__(self):
        return self.toString()
    def __repr__(self):
        return repr(self.toString())

    def update(self, sector, startTime):
        if not ((sector-1) == self.currentSector):
            return False

        now = rospy.get_rostime().to_sec()
        self.currentSector = sector
        self.lastSectorTime = now - self.totalTime - startTime
        self.totalTime = now - startTime
        
        return True
