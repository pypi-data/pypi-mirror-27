class ExList(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def map(self, f):
        return ExList([f(x) for x in self])

    def filter(self, f):
        return ExList([x for x in self if f(x)])

    def fold(self, ini, f):
        if len(self) == 0:
            return ini
        else:
            return ExList(self[1:]).fold(f(ini,self[0]),f)

    def foreach(self, f):
        for ele in self:
            f(ele)
        return

    def flatten(self):
        newlist = ExList()
        self.foreach(lambda lst: lst.foreach(lambda ele: newlist.append(ele)))
        return newlist

    def flatmap(self, f):
        return self.map(f).flatten()

    def __getitem__(self,k):
        if isinstance(k,slice):
            return ExList(list.__getitem__(self,k))
        return list.__getitem__(self,k)

    def drop(self,i):
        return self[i:]

    def take(self,i):
        return self[:i]
