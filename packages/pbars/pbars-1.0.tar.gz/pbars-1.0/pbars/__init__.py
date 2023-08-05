# ------------------------
#   Only For PYTHON 3
# ------------------------

class ProgressBar:
    def __init__(self, label, length, total, style="ascii", **kwargs):
        self.__label = label
        self.__length = int(length)
        self.__total = int(total)
        self.__style = style
        if style.lower() == "ascii":
            try:
                self.__fill = kwargs["fill"]
            except KeyError:
                self.__fill = "="
        pass

    def Progress(self, current):
        if self.__style.lower() == "ascii":
            self.__p_ascii(int(current))
            pass
        elif self.__style.lower() == "pip":
            self.__p_pip(int(current))
            pass
        pass

    def __p_ascii(self, x):
        perc = round((x * 100) / self.__total, 2)
        hash = int((perc * self.__length) / 100)
        Hash = self.__length - hash
        fill_space = " "
        dum = self.__fill * hash + fill_space * Hash
        print("{} [{}] {} % Completed".format(self.__label, dum, perc), end="\r")
        pass

    def __p_pip(self, x):
        perc = round((x * 100) / self.__total, 2)
        hash = int((perc * self.__length) / 100)
        Hash = self.__length - hash
        fill = "█"
        fill_space = " "
        dum = fill * hash + fill_space * Hash
        print("{} |{}| {} % Completed".format(self.__label, dum, perc), end="\r")
        pass

    pass

