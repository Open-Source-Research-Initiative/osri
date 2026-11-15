"""CPU/headless exercise of original CARLA0.8.4 public client API.
This is an adapted physics trajectory, not one of the paper's learned agents.
"""
import sys,csv,json,time,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'carla084/PythonClient'))
from carla.client import make_carla_client
from carla.settings import CarlaSettings
OUT=ROOT/'carla-output';OUT.mkdir(exist_ok=True)
start=time.time();rows=[]
with make_carla_client('localhost',2000,timeout=40) as client:
 settings=CarlaSettings();settings.set(SynchronousMode=True,SendNonPlayerAgentsInfo=True,NumberOfVehicles=0,NumberOfPedestrians=0,WeatherId=1,QualityLevel='Low',SeedVehicles=42,SeedPedestrians=42)
 scene=client.load_settings(settings);client.start_episode(0)
 for i in range(100):
  measurements,sensors=client.read_data();p=measurements.player_measurements;t=p.transform
  rows.append([i,measurements.game_timestamp,t.location.x,t.location.y,t.location.z,p.forward_speed,p.collision_vehicles,p.collision_pedestrians,p.collision_other,p.intersection_offroad,p.intersection_otherlane])
  client.send_control(steer=0.,throttle=.25,brake=0.,hand_brake=False,reverse=False)
with (OUT/'trajectory.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['frame','game_timestamp_ms','x_m','y_m','z_m','forward_speed_m_s','collision_vehicles','collision_pedestrians','collision_other','fraction_offroad','fraction_otherlane']);w.writerows(rows)
assert all(math.isfinite(float(v)) for row in rows for v in row)
summary={'status':'adapted_run','map':scene.map_name,'frames':len(rows),'final_speed_m_s':rows[-1][5],'distance_m':math.hypot(rows[-1][2]-rows[0][2],rows[-1][3]-rows[0][3]),'sensors':0,'renderer':'Unreal -nullrhi','elapsed_seconds':time.time()-start,'limitation':'No camera images or original MP/IL/RL model weights; this is a CPU/headless deterministic-control physics trajectory, not paper Table1 benchmark.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
