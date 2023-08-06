import fileinput
import hashlib
import operator
import os
import platform


class Highscore:

    def __init__(self):
        self._highscore = self.load()

    def get_scores(self):
        return self._highscore

    @staticmethod
    def load():
        highscore = []
        cwd = os.getcwd()
        if platform.system() == "Linux" or platform.system() == "Darwin":
            try:
                f = open(f"{cwd}/highscore.dat", "r")
            except IOError:
                f = open(f"{cwd}/highscore.dat", "w")
            for line in fileinput.input(f"{cwd}/highscore.dat"):
                name, score, md5 = line.split('[::]')
                md5 = md5.replace('\n', '')

                if str(hashlib.md5(str.encode(str(name+score+"pygame"))).hexdigest()) == str(md5):
                    highscore.append([str(name), int(score), str(md5)])

            highscore.sort(key=operator.itemgetter(1), reverse=True)
            highscore = highscore[0:10]

            f.close()

        elif platform.system() == "Windows":
            try:
                f = open(f"{cwd}\highscore.dat", "r")
            except IOError:
                f = open(f"{cwd}\highscore.dat", "w")
            for line in fileinput.input(f"{cwd}\highscore.dat"):
                name, score, md5 = line.split('[::]')
                md5 = md5.replace('\n', '')

                if str(hashlib.md5(str.encode(str(name + score + "pygame"))).hexdigest()) == str(md5):
                    highscore.append([str(name), int(score), str(md5)])

            highscore.sort(key=operator.itemgetter(1), reverse=True)
            highscore = highscore[0:10]

            f.close()

        return highscore

    def add(self, name, score):
        hash = hashlib.md5((str(name+str(score)+"pygame")).encode("utf-8"))
        self._highscore.append([name, str(score), hash.hexdigest()])
        cwd = os.getcwd()

        if platform.system() == "Linux" or platform.system() == "Darwin":
            with open(f"{cwd}/highscore.dat", "w") as f:
                for name, score, md5 in self._highscore:
                    f.write(str(name)+"[::]"+str(score)+"[::]"+str(md5)+"\n")

        elif platform.system() == "Windows":
            with open(f"{cwd}\highscore.dat", "w") as f:
                for name, score, md5 in self._highscore:
                    f.write(str(name) + "[::]" + str(score) + "[::]" + str(md5) + "\n")
