import logging as log
import os
from signal import signal, SIGINT, SIGTERM
from sys import exit
from tornado.web import Application as WebApp
from tornado.ioloop import IOLoop as IO, PeriodicCallback

from wspr.web_endpoints import *
from wspr.websocket_endpoints import *
from wspr.shared_state import SharedState
from wspr.monitor import Monitor

PORT = 8080

def create_app():
	state = SharedState()
	monitor = Monitor(state)
	state.hardware_listener = monitor

	return (WebApp([
		(r'/', IndexEndpoint),
		(r'/bundle.js', BundleEndpoint),
		(r'/spots', SpotEndpoint),
		(r'/config', ConfigEndpoint, {'state': state})
	]), monitor)

def handle_interrupt(sig, frame):
	log.info('interrupted, shutting down...')
	exit(0)
	
def setup():
	log_level = log.DEBUG if os.environ.get('WSPR_DEBUG') else log.INFO
	log.basicConfig(format='%(levelname)s:\t%(message)s', level=log_level)
	signal(SIGINT, handle_interrupt)
	signal(SIGTERM, handle_interrupt)

def run():
	setup()
	log.debug('application startup...')

	app, monitor = create_app()
	log.debug('application created')
	app.listen(PORT)
	log.info('application listening on port %d', PORT)

	log.debug('hardware monitor start...')
	monitor.go()
	PeriodicCallback(monitor.toggle_GPIO, 1000).start()
	log.debug('monitor started')

	log.debug('starting I/O loop...')
	IO.current().start()
