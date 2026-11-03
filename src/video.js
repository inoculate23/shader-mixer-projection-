import {loopRange} from './model.js';
export class VideoDeck{
 constructor(element,config,onStatus=()=>{}){this.element=element;this.config=config;this.onStatus=onStatus;element.muted=true;element.playsInline=true;element.preload='auto';element.addEventListener('loadedmetadata',()=>{[config.in,config.out]=loopRange(config.in,config.out,element.duration);this.apply();onStatus('Ready · '+config.filename);});element.addEventListener('error',()=>onStatus('Cannot decode this video. Try an H.264 MP4.'));element.addEventListener('ended',()=>{if(config.loop){element.currentTime=config.in;element.play().catch(e=>onStatus(e.message));}});}
 load(file,preserve=false){this.release();if(!preserve){this.config.in=0;this.config.out=0;}this.config.filename=file.name;this.url=URL.createObjectURL(file);this.element.src=this.url;this.element.load();this.onStatus('Loading '+file.name+' · tap Play when ready');}
 apply(){const c=this.config,e=this.element;if(Number.isFinite(e.duration)&&e.duration>0){[c.in,c.out]=loopRange(c.in,c.out,e.duration);if(e.currentTime<c.in||e.currentTime>=c.out)e.currentTime=c.in;}e.playbackRate=c.rate;}
 async toggle(){if(!this.url){this.onStatus('Choose a local video first');return;}if(this.element.paused){this.apply();await this.element.play();}else this.element.pause();}
 tick(){const e=this.element,c=this.config;if(!this.url||!e.duration)return;if(c.loop&&!e.paused&&!e.seeking&&(e.currentTime>=c.out||e.currentTime<c.in)){e.currentTime=c.in;}}
 release(){this.element.pause();this.element.removeAttribute('src');this.element.load();if(this.url)URL.revokeObjectURL(this.url);this.url=null;}
}
