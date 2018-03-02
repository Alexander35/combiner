from threading import Thread
import subprocess
import json
from .models import Worker, Data

def save_data(worker, data):
	try:
		data = Data(
				from_worker=worker,
				data=data,
			)
		data.save()
	except Exception as e:
		print('unable to save the data for worker_id : {} {}'.format(worker_id, e))

def get_params(input_params):
	try:
		return input_params.split(',')
	except Exception as exc:
		print('unable to parse input_params to worker : {}'.format(exc))	

def run_cmd(worker):
	try:
		i_ps = get_params(worker.input_params)
		# i_p = input_params
		print(i_ps)
		args = [worker.run_command]
		[args.append(i_p) for i_p in i_ps ]
		print(args)
		sp = subprocess.Popen(args, stdout=subprocess.PIPE)
		data, err = sp.communicate()
		jdata = json.dumps(
				{
					'data' : data.decode(worker.char_set, worker.str_error_type),
					'err' : err,
				}
			)
		print( json.loads(jdata))
		output_data = json.loads(jdata)
		worker.status='Ready'
		worker.save()
		save_data(worker, output_data)

	except Exception as exc:
		print('Unable to perform worker job : {}'.format(exc))
		return '{}'.format(exc)	

# def worker_initialize(cmd, input_params, char_set, str_error_type):
def worker_initialize(worker):
	try:
		worker_thread = Thread(target=run_cmd, args=(worker,))
		worker_thread.start()
	except Exception as exc:
		print('Unable to create worker thread: {}'.format(exc))