from threading import Thread
import subprocess
import json

def get_params(input_params):
	try:
		return input_params.split(',')
	except Exception as exc:
		print('unable to parse input_params to worker : {}'.format(exc))	

def run_cmd(cmd, input_params):
	try:
		i_p = get_params(input_params)
		sp = subprocess.Popen([cmd, i_p], stdout=subprocess.PIPE)
		data, err = sp.communicate()
		jdata = json.dumps(
				{
					'data' : data.decode('cp866', 'ignore'),
					'err' : err,
				}
			)
		print( json.loads(jdata))		
	except Exception as exc:
		print('Unable to perform worker job : {}'.format(exc))
		return '{}'.format(exc)	

def worker_initialize(cmd, input_params, char_set, str_error_type):
	try:
		worker_thread = Thread(target=run_cmd, args=(cmd, input_params,))
		worker_thread.start()
	except Exception as exc:
		print('Unable to create worker thread: {}'.format(exc))