


class TNote():
    
    def __init__(self,solfa,duration,pitch):
        self.solfa=solfa
        self.duration=duration
        self.pitch=pitch
        
def get(t,dur,r,pos,note):
    vals=(t,dur,r)
    if vals == (0,0.25,0.75):
        if pos==100:
            return '|{},'.format(note.solfa)
        else:
            return ':{},'.format(note.solfa)
    if vals == (.25 , .25, .5):
        return ',{}.'.format(note.solfa)
    if vals == (.75, .25, 0):
        if pos==1:
            return ',{}|'.format(note.solfa)
        else:
            return ',{}:'.format(note.solfa)
    if vals == (0,0.25,0.75):
        if pos==100:
            return '|{},'.format(note.solfa)
        else:
            return ':{},'.format(note.solfa)
    if vals == (.5 , .25, .25):
        return '.{},'.format(note.solfa)
    if vals == (0, .5, .5):
        if pos==100:
            return '| {} .'.format(note.solfa)
        else:
            return ': {} .'.format(note.solfa)
    if vals == (.5, .5, 0):
        if pos!=1:
            return '. {} :'.format(note.solfa)
        else:
            return '. {} |'.format(note.solfa)
    
    if vals == (0, 1., 0):
        #fullnotes
        if pos==100:
            return '|    {}    :'.format(note.solfa)
        elif pos == 10:
            return ':    {}    :'.format(note.solfa)
        elif pos ==1:
            return ':    {}    |'.format(note.solfa)
    
    if vals == (.25, .5, .25):
        return ',{}.-,'.format(note.solfa)
    
    if vals == (.25 , .75, 0):
        if pos !=1:
            return ',{}. - :'.format(note.solfa)
        else:
            return ',{}. - |'.format(note.solfa)
    
    if vals == (0, 0.75, .25):
        if pos==100:
            return '| {} .-,'.format(note.solfa)
        else:
            return ': {} .-,'.format(note.solfa)

class Container():
    def __init__(self,taken,rem,pos):
        self.taken= taken
        self.rem= rem
        self.pos= pos
    
    def take_note(self,tnotes):
        snotes=''
        note=tnotes.pop(0)
        while True:
            dur= note.duration
            taken=self.taken
            rem=self.rem
            pos=self.pos
            
            if dur < self.rem:
                print('###')
                exp=get(taken, dur, rem-dur, pos,note)
                print(exp, taken, dur, rem-dur, pos)
                snotes+=exp
                self.taken=taken+dur
                self.rem=1-self.taken
                
                if len(tnotes)==0:
                    return snotes, tnotes
                else:
                    note=tnotes.pop(0)
                    continue
            elif dur== self.rem:
                print('##')
                exp=get(taken, dur, 0, pos,note)
                snotes+=exp
                print(exp,0)
                return snotes, tnotes
                break
            elif dur > self.rem:
                print('#')
                exp=get(taken, rem, 0, pos,note)
                print(exp, taken, dur, rem-dur, pos)
                tnotes.insert(0,TNote('-',dur-rem,0))
                snotes+=exp
                return snotes, tnotes
                

def convert(d):
            
    tnotes=[TNote(*i) for i in d]
    sdd=''
    n=0
    while n>=0:#for no in [100,10,1]:#while len(tnotes):
        bar = [100,10,10,1]
        no= bar[n]
        if 1:
            con= Container(0,1,no)
            sd,tnotes=con.take_note(tnotes)
            sdd+=sd
            if len(tnotes)==0:
                break
            if n==(len(bar)-1):
                n=0
            else:
                n+=1
    return sdd.replace('||','|\n|').replace('::',':').replace('..','.').replace(',,',',')


if __name__=='__main__':

    d=[('m', 1.0, 0), ('f', 0.5, 0), ('m', 0.5, 0), ('r', 0.5, 0), ('m', 1.0, 0), ('x', 1.0, 0), ('se', 0.5, 0), ('l', 0.5, 0), ('d', 0.5, 1), ('t', 0.5, 0), ('l', 0.5, 0), ('r', 1.0, 1), ('t', 0.5, 0), ('se', 1.0, 0), ('m', 1.0, 0), ('f', 1.0, 0), ('se', 0.5, 0), ('se', 0.5, 0), ('l', 0.5, 0), ('l', 0.5, 0), ('t', 0.25, 0), ('t', 0.25, 0), ('d', 0.5, 1), ('t', 0.5, 0), ('l', 0.5, 0), ('t', 0.5, 0), ('d', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('t', 0.5, 0), ('m', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('t', 0.5, 0), ('l', 0.5, 0), ('t', 1.0, 0), ('t', 1.0, 1), ('se', 0.5, 1), ('m', 1.0, 1), ('l', 1.0, 1), ('m', 0.5, 1), ('d', 0.5, 1), ('l', 0.5, 0), ('m', 0.5, 0), ('r', 0.5, 0), ('m', 0.5, 0), ('f', 0.5, 0), ('m', 0.5, 0), ('r', 0.5, 0), ('m', 0.5, 0), ('f', 0.5, 0), ('s', 0.5, 0), ('l', 0.5, 0), ('s', 0.5, 0), ('f', 0.5, 0), ('s', 0.5, 0), ('f', 0.5, 0), ('m', 0.5, 0), ('r', 0.5, 0), ('m', 0.5, 0), ('r', 0.5, 0), ('d', 0.5, 0), ('t', 0.5, -1), ('r', 0.5, 0), ('d', 0.5, 0), ('t', 0.5, -1), ('d', 0.5, 0), ('t', 0.5, -1), ('l', 0.5, -1), ('se', 0.5, -1), ('l', 0.5, -1), ('t', 0.5, -1), ('d', 0.5, 0), ('t', 0.5, -1), ('l', 0.5, -1), ('m', 0.5, 0), ('f', 0.5, 0), ('se', 0.5, 0), ('l', 0.5, 0), ('t', 0.5, 0), ('d', 0.5, 1), ('t', 0.5, 0), ('m', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('t', 0.5, 0), ('l', 0.5, 0), ('t', 1.0, 0), ('m', 1.0, 1), ('m', 1.0, 2), ('m', 0.5, 2), ('l', 1.0, 1), ('x', 1.0, 0), ('m', 1.0, 2), ('r', 1.0, 2), ('d', 1.0, 2), ('m', 0.5, 1), ('m', 0.5, 1), ('f', 0.5, 1), ('f', 0.5, 1), ('se', 0.5, 1), ('se', 0.5, 1), ('l', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('t', 0.5, 1), ('d', 0.5, 2), ('t', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('d', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('m', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('t', 0.5, 1), ('t', 0.5, 1), ('d', 0.5, 2), ('t', 0.5, 1), ('t', 0.5, 1), ('l', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('l', 0.5, 1), ('se', 0.5, 1), ('se', 0.5, 1), ('m', 0.5, 1), ('m', 0.5, 1), ('f', 0.5, 1), ('f', 0.5, 1), ('se', 0.5, 1), ('se', 0.5, 1), ('l', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('t', 0.5, 1), ('d', 0.5, 2), ('t', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('d', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('t', 0.5, 1), ('m', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('r', 0.5, 2), ('d', 0.5, 2), ('t', 0.5, 1), ('l', 0.5, 1), ('t', 0.5, 1), ('l', 0.5, 1), ('l', 0.5, 1), ('se', 0.5, 1), ('se', 0.5, 1), ('m', 0.5, 1), ('f', 0.5, 1), ('m', 0.5, 1), ('r', 0.5, 1), ('d', 0.5, 1), ('t', 0.5, 0), ('l', 0.5, 0), ('se', 1.0, 0), ('x', 0.5, 0), ('m', 0.25, 0), ('f', 0.25, 0), ('se', 0.25, 0), ('l', 0.25, 0), ('t', 0.25, 0), ('d', 0.25, 1), ('r', 0.25, 1), ('m', 0.25, 1), ('r', 0.25, 1), ('d', 0.25, 1), ('t', 0.25, 0), ('d', 0.25, 1), ('t', 0.25, 0), ('l', 0.25, 0), ('se', 0.25, 0), ('l', 0.25, 0), ('se', 0.25, 0), ('f', 0.25, 0), ('m', 0.25, 0), ('f', 0.25, 0), ('m', 0.25, 0), ('r', 0.25, 0), ('d', 0.25, 0), ('r', 0.25, 0), ('d', 0.25, 0), ('t', 0.25, -1), ('l', 0.25, -1), ('t', 0.25, -1), ('se', 1.0, -1), ('x', 1.0, 0), ('x', 1.0, 0), ('x', 1.0, 0)]


    print(convert(d))