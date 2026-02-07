import pystalk


def get_pystalk_client(host: str = 'localhost', port: int = 11300):
	return pystalk.BeanstalkClient(host, port)


def pipes_status(client):
	"""Return a mapping of tube -> stats (or an {'error': msg}).

	Expects a client object with `list_tubes()` and `stats_tube(tube)` methods.
	"""
	result = {}
	try:
		tubes = client.list_tubes()
	except Exception as e:
		return {'error': f'list_tubes failed: {e}'}
	for t in tubes:
		try:
			result[t] = client.stats_tube(t)
		except Exception as e:
			result[t] = {'error': str(e)}
	return result