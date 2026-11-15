from pathlib import Path
import subprocess,time,os,signal,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--attempt',default='3');parser.add_argument('--client',default='carla_headless_client.py');args=parser.parse_args()
log=(root/('carla-server-attempt'+args.attempt+'.log')).open('w')
env=dict(os.environ,SDL_VIDEODRIVER='offscreen',LIBGL_ALWAYS_SOFTWARE='1',OMP_NUM_THREADS='2')
server=subprocess.Popen(['./CarlaUE4.sh','/Game/Maps/Town01','-carla-server','-benchmark','-fps=10','-windowed','-ResX=320','-ResY=240','-opengl','-nullrhi','-nosound','-unattended'],cwd=root/'carla084',stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
try:
 time.sleep(12)
 with (root/('carla-client-attempt'+args.attempt+'.log')).open('w') as out:
  client=subprocess.run([__import__('sys').executable,str(root/args.client)],cwd=root,stdout=out,stderr=subprocess.STDOUT,timeout=120)
 print('client_exit_code',client.returncode)
 if client.returncode:raise SystemExit(client.returncode)
finally:
 os.killpg(server.pid,signal.SIGTERM)
 server.wait(timeout=20);log.close()
