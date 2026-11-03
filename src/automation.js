import {clamp,AUTOMATION_RANGES} from './model.js';
export class SliderAutomation{
 constructor(random=Math.random){this.random=random;this.slots=new Map();}
 reset(){this.slots.clear();}
 tick(state,dt){const cfg=state.automation;if(!cfg.enabled||state.frozen){if(!cfg.enabled)this.reset();return [];}
 const active=new Set(cfg.targets);for(const path of this.slots.keys())if(!active.has(path))this.slots.delete(path);
 const changed=[];let index=0;for(const path of cfg.targets){const range=AUTOMATION_RANGES[path];if(!range)continue;const [owner,key]=path.includes('.')?path.split('.'):['',path];const obj=owner?state[owner]:state;const [lo,hi]=range;let slot=this.slots.get(path);if(!slot){slot={base:obj[key],phase:0,from:obj[key],to:obj[key],mode:cfg.mode};this.slots.set(path,slot);}
 if(slot.mode!==cfg.mode){slot.base=obj[key];slot.phase=0;slot.from=obj[key];slot.to=obj[key];slot.mode=cfg.mode;}
 const radius=(hi-lo)*cfg.depth*.5;const min=clamp(slot.base-radius,lo,hi),max=clamp(slot.base+radius,lo,hi);const advance=Math.max(0,Math.min(dt,.25))*cfg.speed/20;
 if(cfg.mode==='random'){if(slot.phase===0)slot.to=min+this.random()*(max-min);slot.phase+=advance;if(slot.phase>=1){slot.from=obj[key];slot.to=min+this.random()*(max-min);slot.phase%=1;}const ease=slot.phase*slot.phase*(3-2*slot.phase);obj[key]=clamp(slot.from+(slot.to-slot.from)*ease,min,max);}
 else{slot.phase=(slot.phase+advance*(.8+index*.07))%1;obj[key]=clamp(slot.base+Math.sin(slot.phase*Math.PI*2)*radius,lo,hi);}
 changed.push(path);index++;}return changed;}
}
