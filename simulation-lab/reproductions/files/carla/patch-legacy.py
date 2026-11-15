from pathlib import Path
root=Path(__file__).resolve().parent
for p in [root/'carla084/PythonClient/carla/client.py',root/'sources/driving-benchmarks/version084/carla/client.py']:
 s=p.read_text();p.write_text(s.replace('raise StopIteration','return'))
p=root/'sources/driving-benchmarks/version084/carla/planner/city_track.py'
s=p.read_text();p.write_text(s.replace('threshold=np.nan','threshold=1000000'))
