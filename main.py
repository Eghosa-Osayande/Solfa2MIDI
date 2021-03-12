

TITLE= 'keys to imagination_violin_solo_160bpm'
TONIC='C'
TONIC_PITCH=5
BPM= 160
NUMERATOR=2
DENOMINATOR=4
#MODE= 'static'
MODE='dynamic'
PARTS= [ 
    
    #{'name' : 'Soprano', 'id' : 'key_static', 'volume' : 70,'instrument' : 53}, 
   {'name' : 'Soprano', 'id' : 'key_dynamic', 'volume' : 127,'instrument' : 40}, 
    
]
            
SCORE={ 

'key_dynamic':'''

m:-:-:-: f.m.r.m:-:x:
se.l.d'.t.l.r':t.se:m:f:
se.se.l.l.t,d',t,d',t.l.t.d'.r',d',r',d',t.m'.r'.d'.r'.d'.t.l.t:
t':se'.m':l':  m'.d'.l.m.r.m.
f,m,f,m,r. m.f.s.l.se.f.se.f.m.r.m.r.d.'t.r.d.'t.d.'t.'l.'se.'l.
m.f.m,m,r.m.f.se.l.t,d',t,d',t.m'.r'.d'.r'.d'.t.l.t:m':-.m'':-:-:m''.l':-:x:
m'':-.r'',m'',r'':-.d'',r'',d'':-.
m'.m'.f'.f'.  se'.se'.l'.l'.      
t'.t',d'',t',d'',t'.l'.  t'.d''.r'',d'',r'',d'',m''.r''.d''.r''.d''.t'.t'.d''.t'.t'.l'.l'.t'.l'.se'.se'.

m'.m'.f'.f'.  se'.se'.l'.l'.      
t'.t',d'',t',d'',t'.l'.  t'.d''.r''.d''.t'.
m''.r''.d''.r''.d''.t'.l'.t'.l'.l'.se'.se'.
m'.f'.m'.r'.d'.t.l.se:x.
m,f,se,l,t,d',r',m',r',d',
t,d',t,l,
se,l,se,f,
m,f,m,r,
d,r,d,'t,'l,'t,'se:x:x:x:
'''
,
'key_static':'''

|x:x:| m:-:-: f.m | r.m :-: x : se.l |
d'.t : l.r':-.t : se | m : f : se.se : l.l |
t,t.d' : t.l : t.d': r'.d' | t.m' : r'.d' : r'.d' : t.l | 
t : t' : se'.m' :-.l' | -.m' : d'.l: m.r: m.f |
m.r : m.f : se.l : se.f | se.f : m.r : m.r : d.'t |
r.d : 't.d : 't.'l: 'se.'l | m.f : m,m.r : m.f : se.l | 
t.d' : t.m' : r'.d' : r'.d' | t.l : t:m':-.m''| -: -:m'',m''. l':-|
x : m'': -.r'',m'' : r''| -.d'',r'': d'' :-.m' : m'.f' |
f'.se' : se'.l' : l'.t' : t'.d'' | t'.l' : t'.d'' : r''.d'' : m''.r'' |
d''.r'' : d''.t' : t'.d'' : t'.t' | l'.l' : t'.l' : se'.se': m'.m' | 
f'.f' : se'.se' : l'.l' : t'.t' | d''.t' : l'.t' : d''.r'' : d''.t' |
m''.r'' : d''.r'' :d''.t' : l'.t' | l'.l' : se'.se' : m'.f' : m'.r' |
d'.t : l.se :-: x.m,f : se,l.t,d' | r',m'.r',d' : t,d'.t,l : se,l.se,f : m,f.m,r |
d,r.d,'t : 'l,'t.'se:-.x:x|


'''

,

}


from solpha.conductor import Conductor, Cfg

settings=Cfg(TITLE, TONIC, TONIC_PITCH, BPM, PARTS, SCORE,MODE, NUMERATOR, DENOMINATOR)

Chijoke = c=Conductor(settings)
Chijoke.get_music_code()
filename=Chijoke.produce()
print('file saved at ' + filename)

import platform 

if platform.system() == 'Linux':
    import kivy
    if kivy.platform == 'android':
        from jnius import autoclass

        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        data=Uri.parse(filename)
        intent.setDataAndType(data, "audio/*")
        activity.startActivity(intent)
