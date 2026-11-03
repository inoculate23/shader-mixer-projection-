export const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
export function domeDirection(x,y){const r=Math.hypot(x,y);if(r>1)return null;const t=r*Math.PI/2,s=r?Math.sin(t)/r:0;return [x*s,y*s,Math.cos(t)];}
export function bands(data,rate,fftSize){const ranges=[[20,250],[250,2000],[2000,12000]];return ranges.map(([lo,hi])=>{let sum=0,n=0;for(let i=0;i<data.length;i++){const hz=i*rate/fftSize;if(hz>=lo&&hz<hi){sum+=data[i]/255;n++;}}return n?sum/n:0;});}
export function deck(){return {pattern:0,speed:0.35,scale:2.3,hue:0.05,react:0.7};}
