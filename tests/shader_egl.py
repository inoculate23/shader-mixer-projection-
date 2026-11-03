"""Optional cloud shader integration test. Uses system EGL/Mesa, no Python packages.
Run: python3 tests/shader_egl.py (Linux with surfaceless EGL + GLES2 support).
"""
import ctypes as C, re, pathlib, math
E=C.CDLL('libEGL.so.1'); P=C.c_void_p; I=C.c_int; U=C.c_uint

def egl(name,restype,args):
 f=getattr(E,name);f.restype=restype;f.argtypes=args;return f
getproc=egl('eglGetProcAddress',P,[C.c_char_p])
platform=C.CFUNCTYPE(P,U,P,C.POINTER(I))(getproc(b'eglGetPlatformDisplayEXT'))
display=platform(0x31DD,None,None)
assert egl('eglInitialize',U,[P,C.POINTER(I),C.POINTER(I)])(display,C.byref(I()),C.byref(I())), 'EGL initialize failed'
assert egl('eglBindAPI',U,[U])(0x30A0)
attrs=(I*13)(0x3024,8,0x3023,8,0x3022,8,0x3033,1,0x3040,4,0x3025,0,0x3038)
config=P();count=I()
assert egl('eglChooseConfig',U,[P,C.POINTER(I),C.POINTER(P),I,C.POINTER(I)])(display,attrs,C.byref(config),1,C.byref(count)) and count.value
surface=egl('eglCreatePbufferSurface',P,[P,P,C.POINTER(I)])(display,config,(I*5)(0x3057,64,0x3056,64,0x3038))
context=egl('eglCreateContext',P,[P,P,P,C.POINTER(I)])(display,config,None,(I*3)(0x3098,2,0x3038))
assert context and surface
assert egl('eglMakeCurrent',U,[P,P,P,P])(display,surface,surface,context)
def gl(name,result,args):return C.CFUNCTYPE(result,*args)(getproc(name.encode()))
create=gl('glCreateShader',U,[U]);source=gl('glShaderSource',None,[U,I,C.POINTER(C.c_char_p),P]);compile=gl('glCompileShader',None,[U]);status=gl('glGetShaderiv',None,[U,U,C.POINTER(I)]);log=gl('glGetShaderInfoLog',None,[U,I,P,P])
text=(pathlib.Path(__file__).parent.parent/'src/renderer.js').read_text();shaders=[]
for name,kind in [('vertex',0x8B31),('fragment',0x8B30)]:
 code=re.search(r'const '+name+r'=`(.*?)`;',text,re.S).group(1).encode();s=create(kind);src=C.c_char_p(code);source(s,1,C.byref(src),None);compile(s);ok=I();status(s,0x8B81,C.byref(ok));buf=C.create_string_buffer(4096);log(s,4096,None,buf);assert ok.value,buf.value.decode();shaders.append(s)
program=gl('glCreateProgram',U,[])();attach=gl('glAttachShader',None,[U,U]);[attach(program,s) for s in shaders];gl('glLinkProgram',None,[U])(program);ok=I();gl('glGetProgramiv',None,[U,U,C.POINTER(I)])(program,0x8B82,C.byref(ok));assert ok.value,'link failed';gl('glUseProgram',None,[U])(program)
buf=U();gl('glGenBuffers',None,[I,C.POINTER(U)])(1,C.byref(buf));gl('glBindBuffer',None,[U,U])(0x8892,buf);verts=(C.c_float*12)(-1,-1,1,-1,-1,1,-1,1,1,-1,1,1);gl('glBufferData',None,[U,C.c_ssize_t,P,U])(0x8892,C.sizeof(verts),verts,0x88E4)
pos=gl('glGetAttribLocation',I,[U,C.c_char_p])(program,b'p');gl('glEnableVertexAttribArray',None,[U])(pos);gl('glVertexAttribPointer',None,[U,I,U,U,I,P])(pos,2,0x1406,0,0,None)
def uniform(name,values):
 loc=gl('glGetUniformLocation',I,[U,C.c_char_p])(program,name.encode());gl('glUniform'+str(len(values))+'f',None,[I]+[C.c_float]*len(values))(loc,*values)
uniform('resolution',[64,64]);uniform('time',[1]);uniform('audio',[.4,.3,.2]);uniform('reactive',[.7,.7]);uniform('deckA',[0,.35,2.3,.05]);uniform('deckB',[2,.2,2.3,.6]);uniform('exposure',[1]);gl('glViewport',None,[I,I,I,I])(0,0,64,64)
def render(mode,mix,exposure=1):
 uniform('dome',[mode]);uniform('mixValue',[mix]);uniform('exposure',[exposure]);gl('glDrawArrays',None,[U,I,I])(4,0,6);pixels=(C.c_ubyte*(64*64*4))();gl('glReadPixels',None,[I,I,I,I,U,U,P])(0,0,64,64,0x1908,0x1401,pixels);assert gl('glGetError',U,[])()==0;return bytes(pixels)
a=render(0,0);b=render(0,1);mid=render(0,.5);assert a!=b and mid!=a and mid!=b;assert max(mid[0::4])>0
fisheye=render(1,.5);assert fisheye[:3]==bytes(3);assert fisheye!=mid
black=render(1,.5,0);assert all(black[i]==0 for i in range(len(black)) if i%4!=3)
# Each original shader must produce nonempty output at representative parameters.
for pattern in range(3):
 uniform('deckA',[pattern,.35,2.3,.05]);pixels=render(1,0);assert max(pixels[0::4])>0
# Upload real textures and validate blend algebra and spherical media conversions.
active=gl('glActiveTexture',None,[U]);bind=gl('glBindTexture',None,[U,U]);texparam=gl('glTexParameteri',None,[U,U,I]);teximage=gl('glTexImage2D',None,[U,I,I,I,I,I,U,U,P]);textures=(U*2)();gl('glGenTextures',None,[I,C.POINTER(U)])(2,textures)
for unit in range(2):
 active(0x84C0+unit);bind(0x0DE1,textures[unit])
 for key,val in [(0x2801,0x2600),(0x2800,0x2600),(0x2802,0x812F),(0x2803,0x812F)]:texparam(0x0DE1,key,val)
 loc=gl('glGetUniformLocation',I,[U,C.c_char_p])(program,('videoA' if unit==0 else 'videoB').encode());gl('glUniform1i',None,[I,I])(loc,unit)
def upload(unit,colors,w=1,h=1):
 active(0x84C0+unit);bind(0x0DE1,textures[unit]);data=(C.c_ubyte*len(colors))(*colors);teximage(0x0DE1,0,0x1908,w,h,0,0x1908,0x1401,data)
a_color=[51,102,153];b_color=[204,128,51];upload(0,a_color+[255]);upload(1,b_color+[255]);uniform('mediaA',[1,2,2,90]);uniform('mediaB',[1,2,2,90]);uniform('blendAmount',[1])
for mode in range(6):
 uniform('blendMode',[mode]);pixels=render(2,1)
 expected=[]
 for x,y in zip(a_color,b_color):
  a=x/255;b=y/255
  value=[b,min(1,a+b),1-(1-a)*(1-b),a*b,abs(a-b),2*a*b if a<.5 else 1-2*(1-a)*(1-b)][mode]
  expected.append(round(value**.85*255))
 assert all(abs(pixels[i]-expected[i])<=2 for i in range(3)),(mode,list(pixels[:3]),expected)
uniform('blendMode',[0]);uniform('blendAmount',[0])
gradient=[]
for y in range(64):
 for x in range(64):gradient.extend([x*4,y*4,80,255])
upload(0,gradient,64,64)
for output_mode,input_mode in [(0,0),(1,1),(2,2)]:
 uniform('mediaA',[1,input_mode,1,90]);pixels=render(output_mode,0)
 for x,y in [(32,32),(40,32),(32,40)]:
  at=(y*64+x)*4;expected=[round((x*4/255)**.85*255),round((y*4/255)**.85*255)]
  assert all(abs(pixels[at+i]-expected[i])<=5 for i in range(2)),(output_mode,x,y,list(pixels[at:at+3]),expected)
uniform('mediaA',[0,0,1,90])
for pattern in [1,2,3]:
 uniform('calibration',[pattern]);pixels=render(1,0);assert max(pixels[1::4])>0;assert pixels[:3]==bytes(3)
uniform('calibration',[0]);uniform('mediaA',[1,2,2,90]);uniform('rotationA',[0,0,0]);normal=render(2,0);uniform('rotationA',[90,0,0]);rotated=render(2,0);assert normal!=rotated
print('PASS: GLES2 compile/link; three shaders; flat, dome and equirectangular outputs; six blend modes checked against reference pixels; three video projection round trips using actual textures; calibration masks, rotation and blackout (64x64 software rendering).')
egl('eglMakeCurrent',U,[P,P,P,P])(display,None,None,None);egl('eglDestroyContext',U,[P,P])(display,context);egl('eglDestroySurface',U,[P,P])(display,surface);egl('eglTerminate',U,[P])(display)
