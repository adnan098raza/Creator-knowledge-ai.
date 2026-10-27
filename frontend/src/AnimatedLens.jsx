import { useEffect, useRef } from "react";

const vertex = `attribute vec2 position; varying vec2 uv; void main(){ uv=position*.5+.5; gl_Position=vec4(position,0.,1.); }`;
const fragment = `
precision highp float; varying vec2 uv; uniform vec2 resolution; uniform float time; uniform vec2 pointer;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise(p);p=p*2.03+.13;a*=.5;}return v;}
void main(){
 vec2 p=(uv-.5)*(resolution/min(resolution.x,resolution.y));p+=pointer*.018;
 float r=.455,d=length(p);if(d>r)discard;
 float z=sqrt(max(0.,1.-dot(p/r,p/r)));vec3 normal=normalize(vec3(p/r,z));float t=time*.18;
 vec2 f=p*4.4;f.x+=sin(p.y*4.2+t)*.5;f.y+=cos(p.x*3.7-t)*.35;
 float n=fbm(f+vec2(t,-t*.7))*.62+fbm(f*1.6-vec2(t*.55,t))*.38;
 float a=sin(p.x*9.+p.y*5.+n*10.-t*2.4),b=sin(p.y*10.-p.x*5.+n*8.+t*1.8);
 vec3 midnight=vec3(.003,.005,.025),blue=vec3(.008,.035,.28),cobalt=vec3(.015,.18,.95),cyan=vec3(0.,.72,1.),violet=vec3(.27,.035,.92),pink=vec3(.9,.025,.48);
 vec3 c=mix(midnight,blue,smoothstep(0.,1.,n));c=mix(c,cobalt,smoothstep(-.3,.8,a)*.72);c=mix(c,cyan,smoothstep(.65,.98,b)*.68);c=mix(c,violet,smoothstep(-.25,.7,p.y+n*.45)*.72);c=mix(c,pink,smoothstep(.65,.98,sin(p.x*8.+n*9.-t))*smoothstep(-.12,.45,-p.y)*.58);
 vec3 light=normalize(vec3(-.48,.62,.95));float diffuse=max(dot(normal,light),0.);float spec=pow(max(dot(reflect(-light,normal),vec3(0.,0.,1.)),0.),18.);float gloss=exp(-((p.x+.18)*(p.x+.18)*38.+(p.y-.24)*(p.y-.24)*55.));
 c+=vec3(.15,.48,1.)*diffuse*.22+vec3(.55,.83,1.)*(spec*.72+gloss*(.52+.12*sin(t*3.)));
 c+=mix(cyan,violet,smoothstep(-.2,.7,p.y))*pow(1.-z,2.4)*.68;c*=1.-smoothstep(.25,r,d)*.28;c=pow(max(c,0.),vec3(.88));gl_FragColor=vec4(c,1.);
}`;
function shader(gl,type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){console.error(gl.getShaderInfoLog(s));gl.deleteShader(s);return null;}return s;}

export default function AnimatedLens(){
 const ref=useRef(null);const pointer=useRef({x:0,y:0});
 useEffect(()=>{
  const canvas=ref.current;if(!canvas)return;
  const gl=canvas.getContext("webgl",{alpha:true,antialias:true,powerPreference:"high-performance"});
  if(!gl){console.error("WebGL is not supported");return;}
  const vs=shader(gl,gl.VERTEX_SHADER,vertex),fs=shader(gl,gl.FRAGMENT_SHADER,fragment);if(!vs||!fs)return;
  const program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);
  if(!gl.getProgramParameter(program,gl.LINK_STATUS)){console.error(gl.getProgramInfoLog(program));return;}
  const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
  gl.useProgram(program);const pos=gl.getAttribLocation(program,"position");gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
  const res=gl.getUniformLocation(program,"resolution"),tm=gl.getUniformLocation(program,"time"),ptr=gl.getUniformLocation(program,"pointer");
  let raf=0,start=0;const resize=()=>{const box=canvas.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,2.5);canvas.width=Math.max(1,Math.round(box.width*dpr));canvas.height=Math.max(1,Math.round(box.height*dpr));gl.viewport(0,0,canvas.width,canvas.height);};
  const move=e=>{const b=canvas.getBoundingClientRect();pointer.current={x:((e.clientX-b.left)/b.width-.5)*2,y:((e.clientY-b.top)/b.height-.5)*-2};};
  const draw=now=>{if(!start)start=now;gl.clear(gl.COLOR_BUFFER_BIT);gl.useProgram(program);gl.uniform2f(res,canvas.width,canvas.height);gl.uniform1f(tm,(now-start)/1000);gl.uniform2f(ptr,pointer.current.x,pointer.current.y);gl.drawArrays(gl.TRIANGLES,0,6);raf=requestAnimationFrame(draw);};
  resize();const observer="ResizeObserver"in window?new ResizeObserver(resize):null;if(observer)observer.observe(canvas);else window.addEventListener("resize",resize);canvas.addEventListener("pointermove",move);raf=requestAnimationFrame(draw);
  return()=>{cancelAnimationFrame(raf);observer?.disconnect();window.removeEventListener("resize",resize);canvas.removeEventListener("pointermove",move);gl.deleteBuffer(buffer);gl.deleteProgram(program);gl.deleteShader(vs);gl.deleteShader(fs);};
 },[]);
 return <div className="animated-lens"><canvas ref={ref} aria-label="Procedurally animated iridescent lens"/></div>;
}
