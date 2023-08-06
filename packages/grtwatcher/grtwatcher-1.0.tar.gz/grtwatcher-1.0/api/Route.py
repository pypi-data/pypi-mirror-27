from .Api import Api

class Route(Api):
	def __init__(self):
		super().__init__()

	def stops(self, route_id, stop_id=False):
		if stop_id is False:
			return self.request('Stop/GetByRouteId', 'GET', routeId=route_id)
		else:
			return self.request('Stop/GetStopInfo', 'GET', routeId=route_id, stopId=stop_id)

	def buses(self, route_id):
		return self.request('Map/GetVehiclesByRouteId', 'GET', routeId=route_id)