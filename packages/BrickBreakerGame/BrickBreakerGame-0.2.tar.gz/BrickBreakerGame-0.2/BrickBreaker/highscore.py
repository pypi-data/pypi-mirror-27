import fileinput
import hashlib
import operator
from pkg_resources import resource_filename
import getpass
import os


class Highscore:

    def __init__(self):
        self._highscore = self.load()

    def get_scores(self):
        return self._highscore

    @staticmethod
    def load():
        user = getpass.getuser()
        highscore = []
        try:
            f = open(f"/home/{user}/highscore.dat", "r")
        except IOError:
            f = open(f"/home/{user}/highscore.dat", "w")
        for line in fileinput.input(f"/home/{user}/highscore.dat"):
            name, score, md5 = line.split('[::]')
            md5 = md5.replace('\n', '')

            if str(hashlib.md5(str.encode(str(name+score+"pygame"))).hexdigest()) == str(md5):
                highscore.append([str(name), int(score), str(md5)])

        highscore.sort(key=operator.itemgetter(1), reverse=True)
        highscore = highscore[0:10]
        f.close()

        return highscore

    def add(self, name, score):
        user = getpass.getuser()
        hash = hashlib.md5((str(name+str(score)+"pygame")).encode("utf-8"))
        self._highscore.append([name, str(score), hash.hexdigest()])

        with open(f"/home/{user}/highscore.dat", "w") as f:
            for name, score, md5 in self._highscore:
                f.write(str(name)+"[::]"+str(score)+"[::]"+str(md5)+"\n")

