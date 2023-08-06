"""
Kite Connect API client for Python -- [https://kite.trade](kite.trade)

Rainmatter (c) 2016

License
-------
KiteConnect Python library is licensed under the MIT License

The library
-----------
Kite Connect is a set of REST-like APIs that expose
many capabilities required to build a complete
investment and trading platform. Execute orders in
real time, manage user portfolio, stream live market
data (WebSockets), and more, with the simple HTTP API collection

This module provides an easy to use abstraction over the HTTP APIs.
The HTTP calls have been converted to methods and their JSON responses
are returned as native Python structures, for example, dicts, lists, bools etc.
See the **[Kite Connect API documentation](https://kite.trade/docs/connect/v1/)**
for the complete list of APIs, supported parameters and values, and response formats.

Getting started
---------------
	#!python
	from kiteconnect import KiteConnect

	# Initialise.
	kite = KiteConnect(api_key="your_api_key")

	# Assuming you have obtained the `request_token`
	# after the auth flow redirect by redirecting the
	# user to kite.login_url()
	try:
		user = kite.request_access_token(request_token="obtained_request_token",
										secret="your_api_secret")

		kite.set_access_token(user["access_token"])
	except Exception as e:
		print("Authentication failed", str(e))
		raise

	print(user["user_id"], "has logged in")

	# Get the list of positions.
	print(kite.positions())

	# Place an order.
	order_id = kite.order_place(
		tradingsymbol="INFY",
		exchange="NSE",
		quantity=1,
		transaction_type="BUY",
		order_type="MARKET"
	)

	# Fetch all orders
	kite.orders()

	# Get instruments
	kite.instruments()

	# Place an mutual fund order
	kite.mf_order_place(
		tradingsymbol="INF090I01239",
		transaction_type="BUY",
		amount=5000,
		tag="mytag"

	# Cancel a mutual fund order
	kite.mf_order_cancel(order_id="order_id")

	# Get mutual fund instruments
	kite.mf_instruments()

A typical web application
-------------------------
In a typical web application where a new instance of
views, controllers etc. are created per incoming HTTP
request, you will need to initialise a new instance of
Kite client per request as well. This is because each
individual instance represents a single user that's
authenticated, unlike an **admin** API where you may
use one instance to manage many users.

Hence, in your web application, typically:

- You will initialise an instance of the Kite client
- Redirect the user to the `login_url()`
- At the redirect url endpoint, obtain the
`request_token` from the query parameters
- Initialise a new instance of Kite client,
use `request_access_token()` to obtain the `access_token`
along with authenticated user data
- Store this response in a session and use the
stored `access_token` and initialise instances
of Kite client for subsequent API calls.

Exceptions
----------
Kite Connect client saves you the hassle of detecting API errors
by looking at HTTP codes or JSON error responses. Instead,
it raises aptly named **[exceptions](exceptions.m.html)** that you can catch.
"""
from six import StringIO, PY2
import ssl
import csv
import time
import json
import struct
import hashlib
import logging
import requests
import threading

import websocket

import kiteconnect.exceptions as ex

# Initialize logger
logger = logging.getLogger(__name__)


class KiteConnect(object):
	"""
	The API client class. In production, you may initialise
	a single instance of this class per `api_key`.
	"""

	# Default root API endpoint. It's possible to
	# override this by passing the `root` parameter during initialisation.
	_root = "https://api.kite.trade"
	_login = "https://kite.trade/connect/login"

	# URIs to various calls
	_routes = {
		"parameters": "/parameters",
		"api.validate": "/session/token",
		"api.invalidate": "/session/token",
		"user.margins": "/user/margins/{segment}",

		"orders": "/orders",
		"trades": "/trades",
		"orders.info": "/orders/{order_id}",

		"orders.place": "/orders/{variety}",
		"orders.modify": "/orders/{variety}/{order_id}",
		"orders.cancel": "/orders/{variety}/{order_id}",
		"orders.trades": "/orders/{order_id}/trades",

		"portfolio.positions": "/portfolio/positions",
		"portfolio.holdings": "/portfolio/holdings",
		"portfolio.positions.modify": "/portfolio/positions",

		# MF api endpoints
		"mf.orders": "/mf/orders",
		"mf.order.info": "/mf/orders/{order_id}",
		"mf.order.place": "/mf/orders",
		"mf.order.cancel": "/mf/orders/{order_id}",

		"mf.sips": "/mf/sips",
		"mf.sip.info": "/mf/sips/{sip_id}",
		"mf.sip.place": "/mf/sips",
		"mf.sip.modify": "/mf/sips/{sip_id}",
		"mf.sip.cancel": "/mf/sips/{sip_id}",

		"mf.holdings": "/mf/holdings",
		"mf.instruments": "/mf/instruments",

		"market.instruments.all": "/instruments",
		"market.instruments": "/instruments/{exchange}",
		"market.quote": "/instruments/{exchange}/{tradingsymbol}",
		"market.quote.ohlc": "/quote/ohlc",
		"market.quote.ltp": "/quote/ltp",
		"market.historical": "/instruments/historical/{instrument_token}/{interval}",
		"market.trigger_range": "/instruments/{exchange}/{tradingsymbol}/trigger_range"
	}

	_timeout = 7

	def __init__(self, api_key, access_token=None, root=None, debug=False, timeout=7, micro_cache=True, proxies=None, pool=None):
		"""
		Initialise a new Kite Connect client instance.

		- `api_key` is the key issued to you
		- `access_token` is the token obtained after the login flow in
			exchange for the `request_token` . Pre-login, this will default to None,
		but once you have obtained it, you should
		persist it in a database or session to pass
		to the Kite Connect class initialisation for subsequent requests.
		- `root` is the API end point root. Unless you explicitly
		want to send API requests to a non-default endpoint, this
		can be ignored.
		- `debug`, if set to True, will serialise and print requests
		and responses to stdout.
		- `timeout` is the time (seconds) for which the API client will wait for
		a request to complete before it fails.
		- `micro_cache`, when set to True, will fetch the last cached
		version of an API response if available. This saves time on
		a roundtrip to the backend. Micro caches only live for several
		seconds to prevent data from turning stale.
		- `proxies` to set requests proxy.
		Check [python requests documentation](http://docs.python-requests.org/en/master/user/advanced/#proxies) for usage and examples.
		- `pool` is manages request pools. It takes a dict of params accepted by HTTPAdapter as described here http://docs.python-requests.org/en/master/api/
		"""
		self.api_key = api_key
		self.access_token = access_token
		self.debug = debug
		self.micro_cache = micro_cache
		self.session_hook = None
		self._timeout = timeout
		self.proxies = proxies if proxies else {}

		if pool:
			self.reqsession = requests.Session()
			reqadapter = requests.adapters.HTTPAdapter(**pool)
			self.reqsession.mount("https://", reqadapter)
		else:
			self.reqsession = requests

		if root:
			self._root = root

		# disable requests SSL warning
		requests.packages.urllib3.disable_warnings()

	def set_session_hook(self, method):
		"""
		Set a callback hook for session (`TokenError` -- timeout, expiry etc.) errors.
		An `access_token` (login session) can become invalid for a number of
		reasons, but it doesn't make sense for the client to
		try and catch it during every API call.

		A callback method that handles session errors
		can be set here and when the client encounters
		a token error at any point, it'll be called.

		This callback, for instance, can log the user out of the UI,
		clear session cookies, or initiate a fresh login.
		"""
		self.session_hook = method

	def set_access_token(self, access_token):
		"""Set the `access_token` received after a successful authentication."""
		self.access_token = access_token

	def login_url(self):
		"""
		Get the remote login url to which a user should be redirected
		to initiate the login flow.
		"""
		return "%s?api_key=%s" % (self._login, self.api_key)

	def request_access_token(self, request_token, secret):
		"""Do the token exchange with the `request_token` obtained after the login flow,
		and retrieve the `access_token` required for all subsequent requests. The
		response contains not just the `access_token`, but metadata for
		the user who has authenticated.

		- `request_token` is the token obtained from the GET paramers after a successful login redirect.
		- `secret` is the API secret issued with the API key.
		"""
		h = hashlib.sha256(self.api_key.encode("utf-8") + request_token.encode("utf-8") + secret.encode("utf-8"))
		checksum = h.hexdigest()

		resp = self._post("api.validate", {
			"request_token": request_token,
			"checksum": checksum
		})

		if "access_token" in resp:
			self.set_access_token(resp["access_token"])

		return resp

	def invalidate_token(self, access_token=None):
		"""Kill the session by invalidating the access token.

		- `access_token` to invalidate. Default is the active `access_token`.
		"""
		params = None
		if access_token:
			params = {"access_token": access_token}

		return self._delete("api.invalidate", params)

	def margins(self, segment):
		"""Get account balance and cash margin details for a particular segment.

		- `segment` is the trading segment (eg: equity or commodity)
		"""
		return self._get("user.margins", {"segment": segment})

	# orders
	def order_place(self,
					exchange,
					tradingsymbol,
					transaction_type,
					quantity,
					price=None,
					product=None,
					order_type=None,
					validity=None,
					disclosed_quantity=None,
					trigger_price=None,
					squareoff_value=None,
					stoploss_value=None,
					trailing_stoploss=None,
					variety="regular",
					tag=""):
		"""Place an order."""
		params = locals()
		del(params["self"])

		for k in params:
			if k is None:
				del(params[k])

		return self._post("orders.place", params)["order_id"]

	def order_modify(self,
					order_id,
					parent_order_id=None,
					exchange=None,
					tradingsymbol=None,
					transaction_type=None,
					quantity=None,
					price=None,
					order_type=None,
					product=None,
					trigger_price=0,
					validity="DAY",
					disclosed_quantity=0,
					variety="regular"):
		"""Modify an open order."""
		params = locals()
		del(params["self"])

		for k in params:
			if k is None:
				del(params[k])

		return self._put("orders.modify", params)["order_id"]

	def order_cancel(self, order_id, variety="regular", parent_order_id=None):
		"""Cancel an order"""
		return self._delete("orders.cancel", {
			"order_id": order_id,
			"variety": variety,
			"parent_order_id": parent_order_id
		})["order_id"]

	# orderbook and tradebook
	def orders(self, order_id=None):
		"""Get the collection of orders from the orderbook."""
		if order_id:
			return self._get("orders.info", {"order_id": order_id})
		else:
			return self._get("orders")

	def trades(self, order_id=None):
		"""
		Retreive the list of trades executed (all or ones under a particular order).

		An order can be executed in tranches based on market conditions.
		These trades are individually recorded under an order.

		- `order_id` is the ID of the order (optional) whose trades are to be retrieved.
		If no `order_id` is specified, all trades for the day are returned.
		"""
		if order_id:
			return self._get("orders.trades", {"order_id": order_id})
		else:
			return self._get("trades")

	def positions(self):
		"""Retrieve the list of positions."""
		return self._get("portfolio.positions")

	def holdings(self):
		"""Retrieve the list of equity holdings."""
		return self._get("portfolio.holdings")

	def product_modify(self,
						exchange,
						tradingsymbol,
						transaction_type,
						position_type,
						quantity,
						old_product,
						new_product):
		"""Modify an open position's product type."""
		return self._put("portfolio.positions.modify", {
			"exchange": exchange,
			"tradingsymbol": tradingsymbol,
			"transaction_type": transaction_type,
			"position_type": position_type,
			"quantity": quantity,
			"old_product": old_product,
			"new_product": new_product
		})

	def mf_orders(self, order_id=None):
		"""Get all mutual fund orders or individual order info."""
		if order_id:
			return self._get("mf.order.info", {"order_id": order_id})
		else:
			return self._get("mf.orders")

	def mf_order_place(self,
						tradingsymbol,
						transaction_type,
						quantity=None,
						amount=None,
						tag=None):
		"""Place a mutual fund order."""
		return self._post("mf.order.place", {
			"tradingsymbol": tradingsymbol,
			"transaction_type": transaction_type,
			"quantity": quantity,
			"amount": amount,
			"tag": tag
		})

	def mf_order_cancel(self, order_id):
		"""Cancel a mutual fund order"""
		return self._delete("mf.order.cancel", {"order_id": order_id})

	def mf_sips(self, sip_id=None):
		"""Get list of all mutual fund SIP's or individual SIP info."""
		if sip_id:
			return self._get("mf.sip.info", {"sip_id": sip_id})
		else:
			return self._get("mf.sips")

	def mf_sip_place(self,
						tradingsymbol,
						amount,
						instalments,
						frequency,
						initial_amount=None,
						instalment_day=None,
						tag=None):
		"""Place a mutual fund SIP"""
		return self._post("mf.sip.place", {
			"tradingsymbol": tradingsymbol,
			"amount": amount,
			"initial_amount": initial_amount,
			"instalments": instalments,
			"frequency": frequency,
			"instalment_day": instalment_day,
			"tag": tag
		})

	def mf_sip_modify(self,
						sip_id,
						amount,
						status,
						instalments,
						frequency,
						instalment_day=None):
		"""Modify a mutual fund SIP"""
		return self._put("mf.sip.modify", {
			"sip_id": sip_id,
			"amount": amount,
			"status": status,
			"instalments": instalments,
			"frequency": frequency,
			"instalment_day": instalment_day
		})

	def mf_sip_cancel(self, sip_id):
		"""Cancel a mutual fund SIP"""
		return self._delete("mf.sip.cancel", {"sip_id": sip_id})

	def mf_holdings(self):
		"""Get list of mutual fund holdings"""
		return self._get("mf.holdings")

	def mf_instruments(self):
		"""Get list of mutual fund instruments"""
		return self._parse_mf_instruments(self._get("mf.instruments"))

	def instruments(self, exchange=None):
		"""
		Retrieve the list of market instruments available to trade.

		Note that the results could be large, several hundred KBs in size,
		with tens of thousands of entries in the list.
		"""
		if exchange:
			params = {"exchange": exchange}

			return self._parse_csv(self._get("market.instruments", params))
		else:
			return self._parse_csv(self._get("market.instruments.all"))

	def quote(self, exchange, tradingsymbol):
		"""Retrieve quote and market depth for an instrument."""
		return self._get("market.quote", {"exchange": exchange, "tradingsymbol": tradingsymbol})

	def ohlc(self, instruments):
		"""
		Retrieve OHLC and market depth for list of instruments.

		- `instruments` is a list of instruments, Instrument are in the format of `tradingsymbol:exchange`. For example NSE:INFY
		"""
		return self._get("market.quote.ohlc", {"i": instruments})

	def ltp(self, instruments):
		"""
		Retrieve last price for list of instruments.

		- `instruments` is a list of instruments, Instrument are in the format of `tradingsymbol:exchange`. For example NSE:INFY
		"""
		return self._get("market.quote.ltp", {"i": instruments})

	def historical(self, instrument_token, from_date, to_date, interval, continuous=False):
		"""
		Retrieve historical data (candles) for an instrument.

		Although the actual response JSON from the API does not have field
		names such has 'open', 'high' etc., this functin call structures
		the data into an array of objects with field names. For example:

		- `instrument_token` is the instrument identifier (retrieved from the instruments()) call.
		- `date_from` is the From date (yyyy-mm-dd)
		- `date_to` is the To date (yyyy-mm-dd)
		- `interval` is the candle interval (minute, day, 5 minute etc.)
		- `continuous` is a boolean flag to get continous data for futures and options instruments.
		"""
		data = self._get("market.historical", {
			"instrument_token": instrument_token,
			"from": from_date,
			"to": to_date,
			"interval": interval,
			"continuous": 1 if continuous else 0})

		records = []
		for d in data["candles"]:
			records.append({
				"date": d[0],
				"open": d[1],
				"high": d[2],
				"low": d[3],
				"close": d[4],
				"volume": d[5]
			})

		return records

	def trigger_range(self, exchange, tradingsymbol, transaction_type):
		"""Retrieve the buy/sell trigger range for Cover Orders."""
		return self._get("market.trigger_range", {"exchange": exchange, "tradingsymbol": tradingsymbol, "transaction_type": transaction_type})

	def _parse_csv(self, data):
		# decode to string for Python 3
		d = data
		if not PY2:
			d = data.decode('utf-8').strip()

		reader = csv.reader(StringIO(d))

		records = []
		header = next(reader)
		for row in reader:
			record = dict(zip(header, row))

			record["last_price"] = float(record["last_price"])
			record["strike"] = float(record["strike"])
			record["tick_size"] = float(record["tick_size"])
			record["lot_size"] = int(record["lot_size"])

			records.append(record)

		return records

	def _parse_mf_instruments(self, data):
		# decode to string for Python 3
		d = data
		if not PY2:
			d = data.decode('utf-8').strip()

		reader = csv.DictReader(StringIO(d))

		# Return list instead of file reader
		records = [row for row in reader]
		return records

	def _get(self, route, params=None):
		"""Alias for sending a GET request."""
		return self._request(route, "GET", params)

	def _post(self, route, params=None):
		"""Alias for sending a POST request."""
		return self._request(route, "POST", params)

	def _put(self, route, params=None):
		"""Alias for sending a PUT request."""
		return self._request(route, "PUT", params)

	def _delete(self, route, params=None):
		"""Alias for sending a DELETE request."""
		return self._request(route, "DELETE", params)

	def _request(self, route, method, parameters=None):
		"""Make an HTTP request."""
		params = {}
		if parameters:
			params = parameters.copy()

		# Micro cache?
		if self.micro_cache is False:
			params["no_micro_cache"] = 1

		# Is there a token?.
		if self.access_token:
			params["access_token"] = self.access_token

		# override instance's API key if one is supplied in the params
		if "api_key" not in params or not params.get("api_key"):
			params["api_key"] = self.api_key

		uri = self._routes[route]

		# 'RESTful' URLs.
		if "{" in uri:
			for k in params:
				uri = uri.replace("{" + k + "}", str(params[k]))

		url = self._root + uri

		if self.debug:
			logger.debug(" Request: {method} {url} {params}".format(
				method=method,
				url=url,
				params=params))

		try:
			r = self.reqsession.request(method,
					url,
					data=params if method in ["POST", "PUT"] else None,
					params=params if method in ["GET", "DELETE"] else None,
					verify=False,
					allow_redirects=True,
					timeout=self._timeout,
					proxies=self.proxies)
		except requests.ConnectionError:
			raise ex.ClientNetworkException("Gateway connection error", code=503)
		except requests.Timeout:
			raise ex.ClientNetworkException("Gateway timed out", code=504)
		except requests.HTTPError:
			raise ex.ClientNetworkException("Invalid response from gateway", code=502)
		except Exception as e:
			raise ex.ClientNetworkException(e.message, code=500)

		if self.debug:
			logger.debug(" Response: {code} {content}".format(
				code=r.status_code,
				content=r.content))

		# Validate the content type.
		if "json" in r.headers["content-type"]:
			try:
				data = json.loads(r.content.decode('utf8'))
			except:
				raise ex.DataException("Couldn't parse JSON response")

			# api error
			if data.get("error_type"):
				if r.status_code == 403:
					if self.session_hook:
						self.session_hook()
						return

				# native Kite errors
				exp = getattr(ex, data["error_type"])
				if data["error_type"] == "TwoFAException":
					raise(ex.TwoFAException(data["message"],
											questions=data["questions"] if "questions" in data else [],
											code=r.status_code))
				elif exp:
					raise(exp(data["message"], code=r.status_code))
				else:
					raise(ex.GeneralException(data["message"], code=r.status_code))

			return data["data"]
		elif "csv" in r.headers["content-type"]:
			return r.content
		else:
			raise ex.DataException("Unknown Content-Type (%s) in response: (%s)" % (r.headers["content-type"], r.content))


class WebSocket(object):
	"""
	The WebSocket client for connecting to Kite Connect's streaming quotes service.

	Getting started:
	---------------

		#!python
		from kiteconnect import WebSocket

		# Initialise.
		kws = WebSocket("your_api_key", "your_public_token", "logged_in_user_id")

		# Callback for tick reception.
		def on_tick(tick, ws):
			print(tick)

		# Callback for successful connection.
		def on_connect(ws):
			# Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
			ws.subscribe([738561, 5633])

			# Set RELIANCE to tick in `full` mode.
			ws.set_mode(ws.MODE_FULL, [738561])

		# Assign the callbacks.
		kws.on_tick = on_tick
		kws.on_connect = on_connect

		# To enable auto reconnect WebSocket connection in case of network failure
		# - First param is interval between reconnection attempts in seconds.
		# Callback `on_reconnect` is triggered on every reconnection attempt. (Default interval is 5 seconds)
		# - Second param is maximum number of retries before the program exits triggering `on_noreconnect` calback. (Defaults to 50 attempts)
		# Note that you can also enable auto reconnection	 while initialising websocket.
		# Example `kws = WebSocket("your_api_key", "your_public_token", "logged_in_user_id", reconnect=True, reconnect_interval=5, reconnect_tries=50)`
		kws.enable_reconnect(reconnect_interval=5, reconnect_tries=50)

		# Infinite loop on the main thread. Nothing after this will run.
		# You have to use the pre-defined callbacks to manage subscriptions.
		kws.connect()

	Callbacks
	---------
	Param `ws` is the currently initialised WebSocket object itself.
	- `on_tick(ticks, ws)` -  Ticks (array of dicts) and the WebSocket object are passed as params.
	- `on_close(ws)` -  Triggered when connection is closed.
	- `on_error(error, ws)` -  Triggered when connection is closed with an error. Error object and WebSocket object are passed as params.
	- `on_connect` -  Triggered when connection is established successfully.
	- `on_message(data, ws)` -  Triggered when there is any message received. This is raw data received from WebSocket.
	- `on_reconnect(ws)` -  Triggered when auto reconnection is attempted.
	- `on_noreconnect` -  Triggered when number of auto reconnection attempts exceeds `reconnect_tries`.

	Tick structure (passed to the tick callback you assign):
	---------------------------
		[{
			"mode": "quote",
			"tradeable": True,
			"instrument_token": 738561,

			"last_price": 957,
			"last_quantity": 100,
			"sell_quantity": 2286,
			"buy_quantity": 0,
			"volume": 5333469,
			"change": 0,
			"average_price": 959,
			"ohlc": {
				"high": 973,
				"close": 957,
				"open": 969,
				"low": 956
			},
			"depth": {
				"sell": [{
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}],
				"buy": [{
					"price": 957,
					"orders": 196608,
					"quantity": 2286
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}, {
					"price": 0,
					"orders": 0,
					"quantity": 0
				}]
			}
		}]
	"""

	EXCHANGE_MAP = {
		"nse": 1,
		"nfo": 2,
		"cds": 3,
		"bse": 4,
		"bfo": 5,
		"bsecds": 6,
		"mcx": 7,
		"mcxsx": 8,
		"nseindices": 9
	}

	INDICES = [EXCHANGE_MAP["nseindices"]]

	READ_TIMEOUT = 5
	RECONNECT_INTERVAL = 5
	RECONNECT_TRIES = 50

	# Available streaming modes.
	MODE_FULL = "full"
	MODE_QUOTE = "quote"
	MODE_LTP = "ltp"

	# Available actions.
	_message_code = 11
	_message_subscribe = "subscribe"
	_message_unsubscribe = "unsubscribe"
	_message_setmode = "mode"

	# Default root API endpoint. It's possible to
	# override this by passing the `root` parameter during initialisation.
	_root = "wss://websocket.kite.trade/"

	def __init__(self, api_key, public_token, user_id, root=None, reconnect=False,
			reconnect_interval=0, reconnect_tries=0):
		"""
		Initialise websocket client instance.

		- `api_key` is the API key issued to you
		- `public_token` is the token obtained after the login flow in
			exchange for the `request_token` . Pre-login, this will default to None,
			but once you have obtained it, you should
			persist it in a database or session to pass
			to the Kite Connect class initialisation for subsequent requests.
		- 'user_id' is the Zerodha client id of the authenticated user
		- `root` is the websocket API end point root. Unless you explicitly
			want to send API requests to a non-default endpoint, this
			can be ignored.
		- `reconnect` is a boolean to enable WebSocket autreconnect in case of network failure/disconnection.
		- `reconnect_interval` - Interval (in seconds) between auto reconnection attemptes. Defaults to 5 seconds.
		- `reconnect_tries` - Maximum number reconnection attempts. Defaults to 50 attempts.
		"""
		self.socket_url = "{root}" \
			"?api_key={api_key}&user_id={user_id}&public_token={public_token}".format(
				root=root if root else self._root,
				api_key=api_key,
				public_token=public_token,
				user_id=user_id
			)
		self.socket = None
		self.websocket_thread = None

		# Placeholders for callbacks.
		self.on_tick = None
		self.on_close = None
		self.on_error = None
		self.on_connect = None
		self.on_message = None
		self.on_reconnect = None
		self.on_noreconnect = None

		# Map of currently subscribed tokens and its mode.
		self.subscribed_tokens = {}

		# Reconnect settings
		self.is_reconnect = reconnect
		self.reconnect_interval = reconnect_interval or self.RECONNECT_INTERVAL
		self.reconnect_tries = reconnect_tries or self.RECONNECT_TRIES

		# Last messare reveived time
		self._retry_count = 0
		self._last_read_time = 0
		self._current_timer = None
		self._current_websocket_url = None

	def _create_connection(self, url):
		"""Create a WebSocket client connection."""
		return websocket.WebSocketApp(url,
								on_open=self._on_connect,
								on_message=self._on_message,
								on_data=self._on_data,
								on_error=self._on_error,
								on_close=self._on_close)

	def connect(self, threaded=False, disable_ssl_verification=False, proxy=None):
		"""
		Start a WebSocket connection as a seperate thread.

		- `threaded` when set to True will open the connection
			in a new thread without blocking the main thread
		- `disable_ssl_verification` when set to True will disable ssl cert verifcation. Default is False.
		- `proxy` (dict) to set http proxy. Default is None.
			List of config
				`host` - http proxy host name.
				`port` - http proxy port. If not set, set to 80.
				`auth` - http proxy auth information (tuple of username and password. default is None)

			Example:
				```
				proxy = {
					'host': 'testhost',
					'port': 3000,
					'auth': ('username', 'password')
				}
				```
		"""
		kwargs = {}

		if proxy and proxy.get("host"):
			kwargs["http_proxy_host"] = proxy.get("host")
			kwargs["http_proxy_port"] = proxy.get("port")
			kwargs["http_proxy_auth"] = proxy.get("auth")

		if disable_ssl_verification:
			kwargs["sslopt"] = {"cert_reqs": ssl.CERT_NONE}

		# Skip if the connection is already open
		if self.socket and self.is_connected():
			return

		# Create a new connection with current time as unique id
		self.socket = self._create_connection(self.socket_url + "?uid=" + str(time.time()))

		# Run without threading
		if not threaded:
			try:
				self.socket.run_forever(**kwargs)
			except:
				import sys
				sys.exit()
		else:
			self.websocket_thread = threading.Thread(target=self.socket.run_forever, kwargs=kwargs)
			self.websocket_thread.daemon = True
			self.websocket_thread.start()

	def is_connected(self):
		"""Check if WebSocket connection is established."""
		if self.socket and self.socket.sock:
			return self.socket.sock.connected
		else:
			return False

	def reconnect(self):
		"""Reconnect WebSocket connection if it is not connected."""
		# If current connection is still active then disconnect to reconnect
		if self.is_connected():
			self.close()
			return

		# Exit reconnection if it exceeds maximum retries
		if self._retry_count > self.reconnect_tries:
			self.close()
			self.disable_reconnect()

			if self.on_noreconnect:
				self.on_noreconnect(self)
		# Try reconnection
		else:
			# Wait before try reconnection
			time.sleep(self.reconnect_interval)

			if self.on_reconnect:
				self.on_reconnect(self)

			self._retry_count += 1
			self.connect()

	def close(self):
		"""Close the WebSocket connection."""
		if self.is_connected():
			self.socket.close()

	def subscribe(self, instrument_tokens):
		"""Subscribe to a list of instrument_tokens.

		- `instrument_tokens` is list of instrument instrument_tokens to subscribe
		"""
		try:
			self.socket.send(json.dumps({"a": self._message_subscribe, "v": instrument_tokens}))

			for token in instrument_tokens:
				self.subscribed_tokens[token] = self.MODE_QUOTE

			return True
		except:
			self.close()
			raise

	def unsubscribe(self, instrument_tokens):
		"""Unsubscribe the given list of instrument_tokens.

		- `instrument_tokens` is list of instrument_tokens to unsubscribe.
		"""
		try:
			self.socket.send(json.dumps({"a": self._message_unsubscribe, "v": instrument_tokens}))

			for token in instrument_tokens:
				try:
					del(self.subscribed_tokens[token])
				except:
					pass

			return True
		except:
			self.close()
			raise

	def set_mode(self, mode, instrument_tokens):
		"""Set streaming mode for the given list of tokens.

		- `mode` is the mode to set. It can be one of the following class constants:
			MODE_LTP, MODE_QUOTE, or MODE_FULL.
		- `instrument_tokens` is list of instrument tokens on which the mode should be applied
		"""
		try:
			self.socket.send(json.dumps({"a": self._message_setmode, "v": [mode, instrument_tokens]}))

			# Record the mode for that subscription
			for token in instrument_tokens:
				self.subscribed_tokens[token] = mode

			return True
		except:
			self.close()
			raise

	def resubscribe(self):
		"""Resubscribe to all currently subscribed tokens. Used to restore all the
		subscribed tokens after successful reconnection.
		"""
		mode_full_tokens = []
		mode_quote_tokens = []
		mode_ltp_tokens = []

		for token, mode in self.subscribed_tokens.items():
			if mode == self.MODE_FULL:
				mode_full_tokens.append(token)
			elif mode == self.MODE_QUOTE:
				mode_quote_tokens.append(token)
			elif mode == self.MODE_LTP:
				mode_ltp_tokens.append(token)

		# subscribe for the tokens
		self.subscribe(mode_full_tokens + mode_quote_tokens + mode_ltp_tokens)

		# set modes
		self.set_mode(self.MODE_FULL, mode_full_tokens)
		self.set_mode(self.MODE_QUOTE, mode_quote_tokens)
		self.set_mode(self.MODE_LTP, mode_ltp_tokens)

	def enable_reconnect(self, reconnect_interval=None, reconnect_tries=None):
		"""Enable WebSocket autreconnect in case of network failure/disconnection.
		- `reconnect_interval` - Interval between auto reconnection attemptes. `on_reconnect` callback
			is triggered when reconnection is attempted.
		- `reconnect_tries` - Maximum number reconnection attempts. Defaults to 50 attempts.
			`on_noreconnect` callback is triggered when number of retries exceeds this value.
		"""
		self.is_reconnect = True
		self.reconnect_interval = reconnect_interval or self.RECONNECT_INTERVAL
		self.reconnect_tries = reconnect_tries or self.RECONNECT_TRIES

	def disable_reconnect(self):
		"""Disable WebSocket autreconnect."""
		self.is_reconnect = False

	def _on_connect(self, ws):
		# Set last read time
		self._last_read_time = int(time.time())

		# set current socket url
		if not self._current_websocket_url:
			self._current_websocket_url = ws.url

		# reset retry count
		self._retry_count = 0

		# Stop the current timer if its available
		if self._current_timer:
			self._current_timer.cancel()

		# Start the timer again for new connection
		self._timer()

		# Resubscribe to the old tokens if auto reconnect is true
		if self.is_reconnect:
			self.resubscribe()

		if self.on_connect:
			self.on_connect(self)

	def _on_data(self, ws, data, resp_type, data_continue):
		"""Receive raw data from WebSocket."""
		# Set last read time (Heartbeat is received every second)
		self._last_read_time = int(time.time())

		if self.on_tick:
			# If the message is binary, parse it and send it to the callback.
			if resp_type != 1 and len(data) > 4:
				self.on_tick(self._parse_binary(data), self)

	def _on_close(self, ws):
		"""Call 'on_close' callback when connection is closed."""
		# Ignore close callback from ghost connections
		if self._current_websocket_url and self._current_websocket_url != ws.url:
			return

		if self.on_close:
			self.on_close(self)

		# Cancel the current timer if any
		if self._current_timer:
			self._current_timer.cancel()

		# Reconnect if reconnect enabled
		if self.is_reconnect:
			self.reconnect()

	def _on_error(self, ws, error):
		"""Call 'on_error' callback when connection throws an error."""
		if self.on_error:
			self.on_error(error, self)

		self.close()

	def _on_message(self, ws, message):
		"""Call 'on_message' callback when text message is received."""
		if self.on_message:
			self.on_message(message, self)

	def _timer(self):
		stop_timer = False

		if int(time.time()) - self._last_read_time > self.READ_TIMEOUT:
			# Reset _current_websocket_url incase current connection times out
			# This is determined when last heart beat received time interval
			# exceeds read_timeout value
			self._current_websocket_url = None

			# close the current connection if it open
			if self.is_connected():
				self.close()

			# stop timer in this case
			stop_timer = True

		# Dont recall the timer if its stopped
		if stop_timer:
			return

		self._current_timer = threading.Timer(5, self._timer)
		self._current_timer.daemon = True
		self._current_timer.start()

	def _parse_binary(self, bin):
		"""Parse binary data to a (list of) ticks structure."""
		packets = self._split_packets(bin)  # split data to individual ticks packet
		data = []

		for packet in packets:
			instrument_token = self._unpack_int(packet, 0, 4)
			segment = instrument_token & 0xff  # Retrive segment constant from instrument_token

			divisor = 10000000.0 if segment == self.EXCHANGE_MAP["cds"] else 100.0

			# Parse index packets.
			if segment in self.INDICES:
				d = {}
				if len(packet) == 8:
					data.append({
						"tradeable": False,
						"mode": self.MODE_LTP,
						"instrument_token": instrument_token,
						"last_price": self._unpack_int(packet, 4, 8) / divisor
					})
				elif len(packet) == 28:
					data.append({
						"tradeable": False,
						"mode": self.MODE_QUOTE,
						"instrument_token": instrument_token,
						"last_price": self._unpack_int(packet, 4, 8) / divisor,
						"ohlc": {
							"high": self._unpack_int(packet, 8, 12) / divisor,
							"low": self._unpack_int(packet, 12, 16) / divisor,
							"open": self._unpack_int(packet, 16, 20) / divisor,
							"close": self._unpack_int(packet, 20, 24) / divisor
						},
						"change": self._unpack_int(packet, 24, 28) / divisor,
					})

				continue

			# Parse non-index packets.
			if len(packet) == 8:
				data.append({
					"tradeable": True,
					"mode": self.MODE_LTP,
					"instrument_token": instrument_token,
					"last_price": self._unpack_int(packet, 4, 8) / divisor
				})
			elif len(packet) > 8:
				d = {
					"tradeable": True,
					"mode": self.MODE_QUOTE,
					"instrument_token": instrument_token,
					"last_price": self._unpack_int(packet, 4, 8) / divisor,
					"last_quantity": self._unpack_int(packet, 8, 12),
					"average_price": self._unpack_int(packet, 12, 16) / divisor,
					"volume": self._unpack_int(packet, 16, 20),
					"buy_quantity": self._unpack_int(packet, 20, 24),
					"sell_quantity": self._unpack_int(packet, 24, 28),
					"ohlc": {
						"open": self._unpack_int(packet, 28, 32) / divisor,
						"high": self._unpack_int(packet, 32, 36) / divisor,
						"low": self._unpack_int(packet, 36, 40) / divisor,
						"close": self._unpack_int(packet, 40, 44) / divisor
					}
				}

				# Compute the change price.
				d["change"] = 0
				if(d["ohlc"]["close"] != 0):
					d["change"] = (d["last_price"] - d["ohlc"]["close"]) * 100 / d["ohlc"]["close"]

				# Market depth entries.
				depth = {}

				if len(packet) > 44:
					# Change mode to full
					d["mode"] = self.MODE_FULL

					# Set initial depth data
					depth = {
						"buy": [],
						"sell": []
					}

					# Compile the market depth lists.
					for i, p in enumerate(range(44, len(packet), 12)):
						depth["sell" if i >= 5 else "buy"].append({
							"quantity": self._unpack_int(packet, p, p + 4),
							"price": self._unpack_int(packet, p + 4, p + 8) / divisor,
							# Byte format is unsigned short for orders field
							"orders": self._unpack_int(packet, p + 8, p + 10, byte_format="H")
						})

				d["depth"] = depth
				data.append(d)

		return data

	def _split_packets(self, bin):
		"""Split the data to individual packets of ticks."""
		# Ignore heartbeat data.
		if len(bin) < 2:
			return []

		number_of_packets = self._unpack_int(bin, 0, 2, byte_format="H")
		packets = []

		j = 2
		for i in range(number_of_packets):
			packet_length = self._unpack_int(bin, j, j + 2, byte_format="H")
			packets.append(bin[j + 2: j + 2 + packet_length])
			j = j + 2 + packet_length

		return packets

	def _unpack_int(self, bin, start, end, byte_format="I"):
		"""Unpack binary data as unsgined interger. Default byte format is 4 byte unsigned int"""
		return struct.unpack(">" + byte_format, bin[start:end])[0]
