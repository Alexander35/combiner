from threading import Thread
import subprocess
import json
from .models import Worker, Data, Worker_Msg

def save_data(worker, data):
	try:
		data = Data(
				from_worker=worker,
				data=data,
			)
		data.save()
	except Exception as e:
		notify = Worker_Msg(notify_type='error', data='unable to save the data for worker_id : {} {}'.format(worker_id, e), worker=worker)
		notify.save()		

def traverse_json_params(worker, worker_name, created_at):
	try:
		if created_at == 'latest':
			print('latest worker_name : {}'.format(worker_name))
			data = Data.objects.filter(from_worker__name=worker_name).latest('created_at')
		if created_at == 'earliest':
			data = Data.objects.filter(from_worker__name=worker_name).earliest('created_at')	
		if created_at == 'first':
			data = Data.objects.filter(from_worker__name=worker_name).first()		
		if created_at == 'last':
			data = Data.objects.filter(from_worker__name=worker_name).last()
		return data.data.get('data')
	except Exception as exc:
		notify = Worker_Msg(notify_type='error', data='traverse json params error : {}'.format(exc), worker=worker)
		notify.save()		

def get_params(worker):

	if(worker.input_type == 'db_data'):	
		try:
			jsi_p = json.loads( worker.input_params)
			input_params = traverse_json_params(worker,jsi_p.get('worker_name'),jsi_p.get('created_at'))	
			splitted_args = input_params.split(',')
			args=[]
			args.append('{}{}'.format(worker.path, worker.run_command))
			[args.append(i_p) for i_p in splitted_args ]
			return args
		except Exception as exc:
			notify = Worker_Msg(notify_type='warning', data='cant read json param  : {}'.format(exc), worker=worker)
			notify.save()

	if(worker.input_type == 'native'):
		try:
			splitted_args =  worker.input_params.split(',')
			args = ['{}{}'.format( worker.path, worker.run_command.rstrip(' '))]
			[args.append(i_p) for i_p in splitted_args ]
			return args

		except Exception as exc:
			notify = Worker_Msg(notify_type='error', data='unable to parse input_params to worker : {}'.format(exc), worker=worker)
			notify.save()

	if(worker.input_type == 'db_multiple_data'):
		try:
			jsi_p = json.loads( worker.input_params)
			print('input params : {}'.format(jsi_p))
			input_params = traverse_json_params(worker,jsi_p.get('worker_name'),jsi_p.get('created_at'))	
			# splitted_args = input_params.split(',')
			args=[]
			args.append('{}{}'.format(worker.path, worker.run_command))
			# [args.append(i_p) for i_p in splitted_args ]
			return '{}{}'.format(args, input_params)
		except Exception as exc:
			notify = Worker_Msg(notify_type='warning', data='cant read json param  : {}'.format(exc), worker=worker)
			notify.save()	

def run_cmd(worker):
	try:
		args = get_params(worker)

		print('JOB args : {}'.format(args))

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
		output_data = json.loads(jdata)
		worker.status='Ready'
		worker.save()
		save_data(worker, output_data)
	except Exception as exc:
		notify = Worker_Msg(notify_type='error', data='Unable to perform worker job : {}'.format(exc), worker=worker)
		notify.save()
		return '{}'.format(exc)	

def worker_initialize(worker, join=None):
	try:
		worker_thread = Thread(target=run_cmd, args=(worker,))
		worker_thread.start()
		if join:
			worker_thread.join()
	except Exception as exc:
		notify = Worker_Msg(notify_type='error', data='Unable to create worker thread: {}'.format(exc), worker=worker)
		notify.save()