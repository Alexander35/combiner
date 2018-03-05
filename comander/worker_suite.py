from threading import Thread
import subprocess
import json
from .models import Worker, Data
# import re

def save_data(worker, data):
	try:
		data = Data(
				from_worker=worker,
				data=data,
			)
		data.save()
	except Exception as e:
		print('unable to save the data for worker_id : {} {}'.format(worker_id, e))

def traverse_json_params(worker_name, created_at):
	try:
		if created_at == 'latest':
			data = Data.objects.filter(from_worker__name=worker_name).latest('created_at')
		if created_at == 'earliest':
			data = Data.objects.filter(from_worker__name=worker_name).earliest('created_at')	
		if created_at == 'first':
			data = Data.objects.filter(from_worker__name=worker_name).first()		
		if created_at == 'last':
			data = Data.objects.filter(from_worker__name=worker_name).last()							
		print('DATA : {}'.format(data))
		return data.data.get('data')
	except Exception as exc:
		print('traverse json params error : {}'.format(exc))
	# print('234 {}{}'.format(worker_name, created_at))

def get_params(input_params):
	
	try:
		jsi_p = json.loads( input_params)
		input_params =  traverse_json_params(jsi_p.get('worker_name'),jsi_p.get('created_at'))	
	except Exception as exc:
		print('cant read json param : {}'.format(exc))	

	try:
		print('input_params {}'.format(input_params))
		return input_params.split(',')
	except Exception as exc:
		print('unable to parse input_params to worker : {}'.format(exc))

def run_cmd(worker):
	try:
		i_ps = get_params(worker.input_params)
		# print(i_ps)
		args = [worker.run_command.rstrip(' ')]
		[args.append(i_p) for i_p in i_ps ]
		print(args)
		sp = subprocess.Popen(args, stdout=subprocess.PIPE)
		worker.status='Processing'
		worker.save()
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

def worker_initialize(worker, join=None):
	try:
		worker_thread = Thread(target=run_cmd, args=(worker,))
		worker_thread.start()
		if join:
			worker_thread.join()
	except Exception as exc:
		print('Unable to create worker thread: {}'.format(exc))