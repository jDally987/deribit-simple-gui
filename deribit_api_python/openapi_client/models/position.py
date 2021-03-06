# coding: utf-8

"""
    Deribit API

    #Overview  Deribit provides three different interfaces to access the API:  * [JSON-RPC over Websocket](#json-rpc) * [JSON-RPC over HTTP](#json-rpc) * [FIX](#fix-api) (Financial Information eXchange)  With the API Console you can use and test the JSON-RPC API, both via HTTP and  via Websocket. To visit the API console, go to __Account > API tab >  API Console tab.__   ##Naming Deribit tradeable assets or instruments use the following system of naming:  |Kind|Examples|Template|Comments| |----|--------|--------|--------| |Future|<code>BTC-25MAR16</code>, <code>BTC-5AUG16</code>|<code>BTC-DMMMYY</code>|<code>BTC</code> is currency, <code>DMMMYY</code> is expiration date, <code>D</code> stands for day of month (1 or 2 digits), <code>MMM</code> - month (3 first letters in English), <code>YY</code> stands for year.| |Perpetual|<code>BTC-PERPETUAL</code>                        ||Perpetual contract for currency <code>BTC</code>.| |Option|<code>BTC-25MAR16-420-C</code>, <code>BTC-5AUG16-580-P</code>|<code>BTC-DMMMYY-STRIKE-K</code>|<code>STRIKE</code> is option strike price in USD. Template <code>K</code> is option kind: <code>C</code> for call options or <code>P</code> for put options.|   # JSON-RPC JSON-RPC is a light-weight remote procedure call (RPC) protocol. The  [JSON-RPC specification](https://www.jsonrpc.org/specification) defines the data structures that are used for the messages that are exchanged between client and server, as well as the rules around their processing. JSON-RPC uses JSON (RFC 4627) as data format.  JSON-RPC is transport agnostic: it does not specify which transport mechanism must be used. The Deribit API supports both Websocket (preferred) and HTTP (with limitations: subscriptions are not supported over HTTP).  ## Request messages > An example of a request message:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 8066,     \"method\": \"public/ticker\",     \"params\": {         \"instrument\": \"BTC-24AUG18-6500-P\"     } } ```  According to the JSON-RPC sepcification the requests must be JSON objects with the following fields.  |Name|Type|Description| |----|----|-----------| |jsonrpc|string|The version of the JSON-RPC spec: \"2.0\"| |id|integer or string|An identifier of the request. If it is included, then the response will contain the same identifier| |method|string|The method to be invoked| |params|object|The parameters values for the method. The field names must match with the expected parameter names. The parameters that are expected are described in the documentation for the methods, below.|  <aside class=\"warning\"> The JSON-RPC specification describes two features that are currently not supported by the API:  <ul> <li>Specification of parameter values by position</li> <li>Batch requests</li> </ul>  </aside>   ## Response messages > An example of a response message:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 5239,     \"testnet\": false,     \"result\": [         {             \"currency\": \"BTC\",             \"currencyLong\": \"Bitcoin\",             \"minConfirmation\": 2,             \"txFee\": 0.0006,             \"isActive\": true,             \"coinType\": \"BITCOIN\",             \"baseAddress\": null         }     ],     \"usIn\": 1535043730126248,     \"usOut\": 1535043730126250,     \"usDiff\": 2 } ```  The JSON-RPC API always responds with a JSON object with the following fields.   |Name|Type|Description| |----|----|-----------| |id|integer|This is the same id that was sent in the request.| |result|any|If successful, the result of the API call. The format for the result is described with each method.| |error|error object|Only present if there was an error invoking the method. The error object is described below.| |testnet|boolean|Indicates whether the API in use is actually the test API.  <code>false</code> for production server, <code>true</code> for test server.| |usIn|integer|The timestamp when the requests was received (microseconds since the Unix epoch)| |usOut|integer|The timestamp when the response was sent (microseconds since the Unix epoch)| |usDiff|integer|The number of microseconds that was spent handling the request|  <aside class=\"notice\"> The fields <code>testnet</code>, <code>usIn</code>, <code>usOut</code> and <code>usDiff</code> are not part of the JSON-RPC standard.  <p>In order not to clutter the examples they will generally be omitted from the example code.</p> </aside>  > An example of a response with an error:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 8163,     \"error\": {         \"code\": 11050,         \"message\": \"bad_request\"     },     \"testnet\": false,     \"usIn\": 1535037392434763,     \"usOut\": 1535037392448119,     \"usDiff\": 13356 } ``` In case of an error the response message will contain the error field, with as value an object with the following with the following fields:  |Name|Type|Description |----|----|-----------| |code|integer|A number that indicates the kind of error.| |message|string|A short description that indicates the kind of error.| |data|any|Additional data about the error. This field may be omitted.|  ## Notifications  > An example of a notification:  ```json {     \"jsonrpc\": \"2.0\",     \"method\": \"subscription\",     \"params\": {         \"channel\": \"deribit_price_index.btc_usd\",         \"data\": {             \"timestamp\": 1535098298227,             \"price\": 6521.17,             \"index_name\": \"btc_usd\"         }     } } ```  API users can subscribe to certain types of notifications. This means that they will receive JSON-RPC notification-messages from the server when certain events occur, such as changes to the index price or changes to the order book for a certain instrument.   The API methods [public/subscribe](#public-subscribe) and [private/subscribe](#private-subscribe) are used to set up a subscription. Since HTTP does not support the sending of messages from server to client, these methods are only availble when using the Websocket transport mechanism.  At the moment of subscription a \"channel\" must be specified. The channel determines the type of events that will be received.  See [Subscriptions](#subscriptions) for more details about the channels.  In accordance with the JSON-RPC specification, the format of a notification  is that of a request message without an <code>id</code> field. The value of the <code>method</code> field will always be <code>\"subscription\"</code>. The <code>params</code> field will always be an object with 2 members: <code>channel</code> and <code>data</code>. The value of the <code>channel</code> member is the name of the channel (a string). The value of the <code>data</code> member is an object that contains data  that is specific for the channel.   ## Authentication  > An example of a JSON request with token:  ```json {     \"id\": 5647,     \"method\": \"private/get_subaccounts\",     \"params\": {         \"access_token\": \"67SVutDoVZSzkUStHSuk51WntMNBJ5mh5DYZhwzpiqDF\"     } } ```  The API consists of `public` and `private` methods. The public methods do not require authentication. The private methods use OAuth 2.0 authentication. This means that a valid OAuth access token must be included in the request, which can get achived by calling method [public/auth](#public-auth).  When the token was assigned to the user, it should be passed along, with other request parameters, back to the server:  |Connection type|Access token placement |----|-----------| |**Websocket**|Inside request JSON parameters, as an `access_token` field| |**HTTP (REST)**|Header `Authorization: bearer ```Token``` ` value|  ### Additional authorization method - basic user credentials  <span style=\"color:red\"><b> ! Not recommended - however, it could be useful for quick testing API</b></span></br>  Every `private` method could be accessed by providing, inside HTTP `Authorization: Basic XXX` header, values with user `ClientId` and assigned `ClientSecret` (both values can be found on the API page on the Deribit website) encoded with `Base64`:  <code>Authorization: Basic BASE64(`ClientId` + `:` + `ClientSecret`)</code>   ### Additional authorization method - Deribit signature credentials  The Derbit service provides dedicated authorization method, which harness user generated signature to increase security level for passing request data. Generated value is passed inside `Authorization` header, coded as:  <code>Authorization: deri-hmac-sha256 id=```ClientId```,ts=```Timestamp```,sig=```Signature```,nonce=```Nonce```</code>  where:  |Deribit credential|Description |----|-----------| |*ClientId*|Can be found on the API page on the Deribit website| |*Timestamp*|Time when the request was generated - given as **miliseconds**. It's valid for **60 seconds** since generation, after that time any request with an old timestamp will be rejected.| |*Signature*|Value for signature calculated as described below | |*Nonce*|Single usage, user generated initialization vector for the server token|  The signature is generated by the following formula:  <code> Signature = HEX_STRING( HMAC-SHA256( ClientSecret, StringToSign ) );</code></br>  <code> StringToSign =  Timestamp + \"\\n\" + Nonce + \"\\n\" + RequestData;</code></br>  <code> RequestData =  UPPERCASE(HTTP_METHOD())  + \"\\n\" + URI() + \"\\n\" + RequestBody + \"\\n\";</code></br>   e.g. (using shell with ```openssl``` tool):  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientId=AAAAAAAAAAA</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientSecret=ABCD</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Timestamp=$( date +%s000 )</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Nonce=$( cat /dev/urandom | tr -dc 'a-z0-9' | head -c8 )</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;URI=\"/api/v2/private/get_account_summary?currency=BTC\"</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;HttpMethod=GET</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Body=\"\"</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Signature=$( echo -ne \"${Timestamp}\\n${Nonce}\\n${HttpMethod}\\n${URI}\\n${Body}\\n\" | openssl sha256 -r -hmac \"$ClientSecret\" | cut -f1 -d' ' )</code></br></br> <code>&nbsp;&nbsp;&nbsp;&nbsp;echo $Signature</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;shell output> ea40d5e5e4fae235ab22b61da98121fbf4acdc06db03d632e23c66bcccb90d2c  (**WARNING**: Exact value depends on current timestamp and client credentials</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;curl -s -X ${HttpMethod} -H \"Authorization: deri-hmac-sha256 id=${ClientId},ts=${Timestamp},nonce=${Nonce},sig=${Signature}\" \"https://www.deribit.com${URI}\"</code></br></br>    ### Additional authorization method - signature credentials (WebSocket API)  When connecting through Websocket, user can request for authorization using ```client_credential``` method, which requires providing following parameters (as a part of JSON request):  |JSON parameter|Description |----|-----------| |*grant_type*|Must be **client_signature**| |*client_id*|Can be found on the API page on the Deribit website| |*timestamp*|Time when the request was generated - given as **miliseconds**. It's valid for **60 seconds** since generation, after that time any request with an old timestamp will be rejected.| |*signature*|Value for signature calculated as described below | |*nonce*|Single usage, user generated initialization vector for the server token| |*data*|**Optional** field, which contains any user specific value|  The signature is generated by the following formula:  <code> StringToSign =  Timestamp + \"\\n\" + Nonce + \"\\n\" + Data;</code></br>  <code> Signature = HEX_STRING( HMAC-SHA256( ClientSecret, StringToSign ) );</code></br>   e.g. (using shell with ```openssl``` tool):  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientId=AAAAAAAAAAA</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientSecret=ABCD</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Timestamp=$( date +%s000 ) # e.g. 1554883365000 </code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Nonce=$( cat /dev/urandom | tr -dc 'a-z0-9' | head -c8 ) # e.g. fdbmmz79 </code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Data=\"\"</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Signature=$( echo -ne \"${Timestamp}\\n${Nonce}\\n${Data}\\n\" | openssl sha256 -r -hmac \"$ClientSecret\" | cut -f1 -d' ' )</code></br></br> <code>&nbsp;&nbsp;&nbsp;&nbsp;echo $Signature</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;shell output> e20c9cd5639d41f8bbc88f4d699c4baf94a4f0ee320e9a116b72743c449eb994  (**WARNING**: Exact value depends on current timestamp and client credentials</code></br></br>   You can also check the signature value using some online tools like, e.g: [https://codebeautify.org/hmac-generator](https://codebeautify.org/hmac-generator) (but don't forget about adding *newline* after each part of the hashed text and remember that you **should use** it only with your **test credentials**).   Here's a sample JSON request created using the values from the example above:  <code> {                            </br> &nbsp;&nbsp;\"jsonrpc\" : \"2.0\",         </br> &nbsp;&nbsp;\"id\" : 9929,               </br> &nbsp;&nbsp;\"method\" : \"public/auth\",  </br> &nbsp;&nbsp;\"params\" :                 </br> &nbsp;&nbsp;{                        </br> &nbsp;&nbsp;&nbsp;&nbsp;\"grant_type\" : \"client_signature\",   </br> &nbsp;&nbsp;&nbsp;&nbsp;\"client_id\" : \"AAAAAAAAAAA\",         </br> &nbsp;&nbsp;&nbsp;&nbsp;\"timestamp\": \"1554883365000\",        </br> &nbsp;&nbsp;&nbsp;&nbsp;\"nonce\": \"fdbmmz79\",                 </br> &nbsp;&nbsp;&nbsp;&nbsp;\"data\": \"\",                          </br> &nbsp;&nbsp;&nbsp;&nbsp;\"signature\" : \"e20c9cd5639d41f8bbc88f4d699c4baf94a4f0ee320e9a116b72743c449eb994\"  </br> &nbsp;&nbsp;}                        </br> }                            </br> </code>   ### Access scope  When asking for `access token` user can provide the required access level (called `scope`) which defines what type of functionality he/she wants to use, and whether requests are only going to check for some data or also to update them.  Scopes are required and checked for `private` methods, so if you plan to use only `public` information you can stay with values assigned by default.  |Scope|Description |----|-----------| |*account:read*|Access to **account** methods - read only data| |*account:read_write*|Access to **account** methods - allows to manage account settings, add subaccounts, etc.| |*trade:read*|Access to **trade** methods - read only data| |*trade:read_write*|Access to **trade** methods - required to create and modify orders| |*wallet:read*|Access to **wallet** methods - read only data| |*wallet:read_write*|Access to **wallet** methods - allows to withdraw, generate new deposit address, etc.| |*wallet:none*, *account:none*, *trade:none*|Blocked access to specified functionality|    <span style=\"color:red\">**NOTICE:**</span> Depending on choosing an authentication method (```grant type```) some scopes could be narrowed by the server. e.g. when ```grant_type = client_credentials``` and ```scope = wallet:read_write``` it's modified by the server as ```scope = wallet:read```\"   ## JSON-RPC over websocket Websocket is the prefered transport mechanism for the JSON-RPC API, because it is faster and because it can support [subscriptions](#subscriptions) and [cancel on disconnect](#private-enable_cancel_on_disconnect). The code examples that can be found next to each of the methods show how websockets can be used from Python or Javascript/node.js.  ## JSON-RPC over HTTP Besides websockets it is also possible to use the API via HTTP. The code examples for 'shell' show how this can be done using curl. Note that subscriptions and cancel on disconnect are not supported via HTTP.  #Methods   # noqa: E501

    OpenAPI spec version: 2.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Position(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'direction': 'str',
        'average_price_usd': 'float',
        'estimated_liquidation_price': 'float',
        'floating_profit_loss': 'float',
        'floating_profit_loss_usd': 'float',
        'open_orders_margin': 'float',
        'total_profit_loss': 'float',
        'realized_profit_loss': 'float',
        'delta': 'float',
        'initial_margin': 'float',
        'size': 'float',
        'maintenance_margin': 'float',
        'kind': 'str',
        'mark_price': 'float',
        'average_price': 'float',
        'settlement_price': 'float',
        'index_price': 'float',
        'instrument_name': 'str',
        'size_currency': 'float'
    }

    attribute_map = {
        'direction': 'direction',
        'average_price_usd': 'average_price_usd',
        'estimated_liquidation_price': 'estimated_liquidation_price',
        'floating_profit_loss': 'floating_profit_loss',
        'floating_profit_loss_usd': 'floating_profit_loss_usd',
        'open_orders_margin': 'open_orders_margin',
        'total_profit_loss': 'total_profit_loss',
        'realized_profit_loss': 'realized_profit_loss',
        'delta': 'delta',
        'initial_margin': 'initial_margin',
        'size': 'size',
        'maintenance_margin': 'maintenance_margin',
        'kind': 'kind',
        'mark_price': 'mark_price',
        'average_price': 'average_price',
        'settlement_price': 'settlement_price',
        'index_price': 'index_price',
        'instrument_name': 'instrument_name',
        'size_currency': 'size_currency'
    }

    def __init__(self, direction=None, average_price_usd=None, estimated_liquidation_price=None, floating_profit_loss=None, floating_profit_loss_usd=None, open_orders_margin=None, total_profit_loss=None, realized_profit_loss=None, delta=None, initial_margin=None, size=None, maintenance_margin=None, kind=None, mark_price=None, average_price=None, settlement_price=None, index_price=None, instrument_name=None, size_currency=None):  # noqa: E501
        """Position - a model defined in OpenAPI"""  # noqa: E501

        self._direction = None
        self._average_price_usd = None
        self._estimated_liquidation_price = None
        self._floating_profit_loss = None
        self._floating_profit_loss_usd = None
        self._open_orders_margin = None
        self._total_profit_loss = None
        self._realized_profit_loss = None
        self._delta = None
        self._initial_margin = None
        self._size = None
        self._maintenance_margin = None
        self._kind = None
        self._mark_price = None
        self._average_price = None
        self._settlement_price = None
        self._index_price = None
        self._instrument_name = None
        self._size_currency = None
        self.discriminator = None

        self.direction = direction
        if average_price_usd is not None:
            self.average_price_usd = average_price_usd
        if estimated_liquidation_price is not None:
            self.estimated_liquidation_price = estimated_liquidation_price
        self.floating_profit_loss = floating_profit_loss
        if floating_profit_loss_usd is not None:
            self.floating_profit_loss_usd = floating_profit_loss_usd
        self.open_orders_margin = open_orders_margin
        self.total_profit_loss = total_profit_loss
        if realized_profit_loss is not None:
            self.realized_profit_loss = realized_profit_loss
        self.delta = delta
        self.initial_margin = initial_margin
        self.size = size
        self.maintenance_margin = maintenance_margin
        self.kind = kind
        self.mark_price = mark_price
        self.average_price = average_price
        self.settlement_price = settlement_price
        self.index_price = index_price
        self.instrument_name = instrument_name
        if size_currency is not None:
            self.size_currency = size_currency

    @property
    def direction(self):
        """Gets the direction of this Position.  # noqa: E501

        direction, `buy` or `sell`  # noqa: E501

        :return: The direction of this Position.  # noqa: E501
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """Sets the direction of this Position.

        direction, `buy` or `sell`  # noqa: E501

        :param direction: The direction of this Position.  # noqa: E501
        :type: str
        """
        if direction is None:
            raise ValueError("Invalid value for `direction`, must not be `None`")  # noqa: E501
        allowed_values = ["buy", "sell"]  # noqa: E501
        if direction not in allowed_values:
            raise ValueError(
                "Invalid value for `direction` ({0}), must be one of {1}"  # noqa: E501
                .format(direction, allowed_values)
            )

        self._direction = direction

    @property
    def average_price_usd(self):
        """Gets the average_price_usd of this Position.  # noqa: E501

        Only for options, average price in USD  # noqa: E501

        :return: The average_price_usd of this Position.  # noqa: E501
        :rtype: float
        """
        return self._average_price_usd

    @average_price_usd.setter
    def average_price_usd(self, average_price_usd):
        """Sets the average_price_usd of this Position.

        Only for options, average price in USD  # noqa: E501

        :param average_price_usd: The average_price_usd of this Position.  # noqa: E501
        :type: float
        """

        self._average_price_usd = average_price_usd

    @property
    def estimated_liquidation_price(self):
        """Gets the estimated_liquidation_price of this Position.  # noqa: E501

        Only for futures, estimated liquidation price  # noqa: E501

        :return: The estimated_liquidation_price of this Position.  # noqa: E501
        :rtype: float
        """
        return self._estimated_liquidation_price

    @estimated_liquidation_price.setter
    def estimated_liquidation_price(self, estimated_liquidation_price):
        """Sets the estimated_liquidation_price of this Position.

        Only for futures, estimated liquidation price  # noqa: E501

        :param estimated_liquidation_price: The estimated_liquidation_price of this Position.  # noqa: E501
        :type: float
        """

        self._estimated_liquidation_price = estimated_liquidation_price

    @property
    def floating_profit_loss(self):
        """Gets the floating_profit_loss of this Position.  # noqa: E501

        Floating profit or loss  # noqa: E501

        :return: The floating_profit_loss of this Position.  # noqa: E501
        :rtype: float
        """
        return self._floating_profit_loss

    @floating_profit_loss.setter
    def floating_profit_loss(self, floating_profit_loss):
        """Sets the floating_profit_loss of this Position.

        Floating profit or loss  # noqa: E501

        :param floating_profit_loss: The floating_profit_loss of this Position.  # noqa: E501
        :type: float
        """
        if floating_profit_loss is None:
            raise ValueError("Invalid value for `floating_profit_loss`, must not be `None`")  # noqa: E501

        self._floating_profit_loss = floating_profit_loss

    @property
    def floating_profit_loss_usd(self):
        """Gets the floating_profit_loss_usd of this Position.  # noqa: E501

        Only for options, floating profit or loss in USD  # noqa: E501

        :return: The floating_profit_loss_usd of this Position.  # noqa: E501
        :rtype: float
        """
        return self._floating_profit_loss_usd

    @floating_profit_loss_usd.setter
    def floating_profit_loss_usd(self, floating_profit_loss_usd):
        """Sets the floating_profit_loss_usd of this Position.

        Only for options, floating profit or loss in USD  # noqa: E501

        :param floating_profit_loss_usd: The floating_profit_loss_usd of this Position.  # noqa: E501
        :type: float
        """

        self._floating_profit_loss_usd = floating_profit_loss_usd

    @property
    def open_orders_margin(self):
        """Gets the open_orders_margin of this Position.  # noqa: E501

        Open orders margin  # noqa: E501

        :return: The open_orders_margin of this Position.  # noqa: E501
        :rtype: float
        """
        return self._open_orders_margin

    @open_orders_margin.setter
    def open_orders_margin(self, open_orders_margin):
        """Sets the open_orders_margin of this Position.

        Open orders margin  # noqa: E501

        :param open_orders_margin: The open_orders_margin of this Position.  # noqa: E501
        :type: float
        """
        if open_orders_margin is None:
            raise ValueError("Invalid value for `open_orders_margin`, must not be `None`")  # noqa: E501

        self._open_orders_margin = open_orders_margin

    @property
    def total_profit_loss(self):
        """Gets the total_profit_loss of this Position.  # noqa: E501

        Profit or loss from position  # noqa: E501

        :return: The total_profit_loss of this Position.  # noqa: E501
        :rtype: float
        """
        return self._total_profit_loss

    @total_profit_loss.setter
    def total_profit_loss(self, total_profit_loss):
        """Sets the total_profit_loss of this Position.

        Profit or loss from position  # noqa: E501

        :param total_profit_loss: The total_profit_loss of this Position.  # noqa: E501
        :type: float
        """
        if total_profit_loss is None:
            raise ValueError("Invalid value for `total_profit_loss`, must not be `None`")  # noqa: E501

        self._total_profit_loss = total_profit_loss

    @property
    def realized_profit_loss(self):
        """Gets the realized_profit_loss of this Position.  # noqa: E501

        Realized profit or loss  # noqa: E501

        :return: The realized_profit_loss of this Position.  # noqa: E501
        :rtype: float
        """
        return self._realized_profit_loss

    @realized_profit_loss.setter
    def realized_profit_loss(self, realized_profit_loss):
        """Sets the realized_profit_loss of this Position.

        Realized profit or loss  # noqa: E501

        :param realized_profit_loss: The realized_profit_loss of this Position.  # noqa: E501
        :type: float
        """

        self._realized_profit_loss = realized_profit_loss

    @property
    def delta(self):
        """Gets the delta of this Position.  # noqa: E501

        Delta parameter  # noqa: E501

        :return: The delta of this Position.  # noqa: E501
        :rtype: float
        """
        return self._delta

    @delta.setter
    def delta(self, delta):
        """Sets the delta of this Position.

        Delta parameter  # noqa: E501

        :param delta: The delta of this Position.  # noqa: E501
        :type: float
        """
        if delta is None:
            raise ValueError("Invalid value for `delta`, must not be `None`")  # noqa: E501

        self._delta = delta

    @property
    def initial_margin(self):
        """Gets the initial_margin of this Position.  # noqa: E501

        Initial margin  # noqa: E501

        :return: The initial_margin of this Position.  # noqa: E501
        :rtype: float
        """
        return self._initial_margin

    @initial_margin.setter
    def initial_margin(self, initial_margin):
        """Sets the initial_margin of this Position.

        Initial margin  # noqa: E501

        :param initial_margin: The initial_margin of this Position.  # noqa: E501
        :type: float
        """
        if initial_margin is None:
            raise ValueError("Invalid value for `initial_margin`, must not be `None`")  # noqa: E501

        self._initial_margin = initial_margin

    @property
    def size(self):
        """Gets the size of this Position.  # noqa: E501

        Position size for futures size in quote currency (e.g. USD), for options size is in base currency (e.g. BTC)  # noqa: E501

        :return: The size of this Position.  # noqa: E501
        :rtype: float
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this Position.

        Position size for futures size in quote currency (e.g. USD), for options size is in base currency (e.g. BTC)  # noqa: E501

        :param size: The size of this Position.  # noqa: E501
        :type: float
        """
        if size is None:
            raise ValueError("Invalid value for `size`, must not be `None`")  # noqa: E501

        self._size = size

    @property
    def maintenance_margin(self):
        """Gets the maintenance_margin of this Position.  # noqa: E501

        Maintenance margin  # noqa: E501

        :return: The maintenance_margin of this Position.  # noqa: E501
        :rtype: float
        """
        return self._maintenance_margin

    @maintenance_margin.setter
    def maintenance_margin(self, maintenance_margin):
        """Sets the maintenance_margin of this Position.

        Maintenance margin  # noqa: E501

        :param maintenance_margin: The maintenance_margin of this Position.  # noqa: E501
        :type: float
        """
        if maintenance_margin is None:
            raise ValueError("Invalid value for `maintenance_margin`, must not be `None`")  # noqa: E501

        self._maintenance_margin = maintenance_margin

    @property
    def kind(self):
        """Gets the kind of this Position.  # noqa: E501

        Instrument kind, `\"future\"` or `\"option\"`  # noqa: E501

        :return: The kind of this Position.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this Position.

        Instrument kind, `\"future\"` or `\"option\"`  # noqa: E501

        :param kind: The kind of this Position.  # noqa: E501
        :type: str
        """
        if kind is None:
            raise ValueError("Invalid value for `kind`, must not be `None`")  # noqa: E501
        allowed_values = ["future", "option"]  # noqa: E501
        if kind not in allowed_values:
            raise ValueError(
                "Invalid value for `kind` ({0}), must be one of {1}"  # noqa: E501
                .format(kind, allowed_values)
            )

        self._kind = kind

    @property
    def mark_price(self):
        """Gets the mark_price of this Position.  # noqa: E501

        Current mark price for position's instrument  # noqa: E501

        :return: The mark_price of this Position.  # noqa: E501
        :rtype: float
        """
        return self._mark_price

    @mark_price.setter
    def mark_price(self, mark_price):
        """Sets the mark_price of this Position.

        Current mark price for position's instrument  # noqa: E501

        :param mark_price: The mark_price of this Position.  # noqa: E501
        :type: float
        """
        if mark_price is None:
            raise ValueError("Invalid value for `mark_price`, must not be `None`")  # noqa: E501

        self._mark_price = mark_price

    @property
    def average_price(self):
        """Gets the average_price of this Position.  # noqa: E501

        Average price of trades that built this position  # noqa: E501

        :return: The average_price of this Position.  # noqa: E501
        :rtype: float
        """
        return self._average_price

    @average_price.setter
    def average_price(self, average_price):
        """Sets the average_price of this Position.

        Average price of trades that built this position  # noqa: E501

        :param average_price: The average_price of this Position.  # noqa: E501
        :type: float
        """
        if average_price is None:
            raise ValueError("Invalid value for `average_price`, must not be `None`")  # noqa: E501

        self._average_price = average_price

    @property
    def settlement_price(self):
        """Gets the settlement_price of this Position.  # noqa: E501

        Last settlement price for position's instrument 0 if instrument wasn't settled yet  # noqa: E501

        :return: The settlement_price of this Position.  # noqa: E501
        :rtype: float
        """
        return self._settlement_price

    @settlement_price.setter
    def settlement_price(self, settlement_price):
        """Sets the settlement_price of this Position.

        Last settlement price for position's instrument 0 if instrument wasn't settled yet  # noqa: E501

        :param settlement_price: The settlement_price of this Position.  # noqa: E501
        :type: float
        """
        if settlement_price is None:
            raise ValueError("Invalid value for `settlement_price`, must not be `None`")  # noqa: E501

        self._settlement_price = settlement_price

    @property
    def index_price(self):
        """Gets the index_price of this Position.  # noqa: E501

        Current index price  # noqa: E501

        :return: The index_price of this Position.  # noqa: E501
        :rtype: float
        """
        return self._index_price

    @index_price.setter
    def index_price(self, index_price):
        """Sets the index_price of this Position.

        Current index price  # noqa: E501

        :param index_price: The index_price of this Position.  # noqa: E501
        :type: float
        """
        if index_price is None:
            raise ValueError("Invalid value for `index_price`, must not be `None`")  # noqa: E501

        self._index_price = index_price

    @property
    def instrument_name(self):
        """Gets the instrument_name of this Position.  # noqa: E501

        Unique instrument identifier  # noqa: E501

        :return: The instrument_name of this Position.  # noqa: E501
        :rtype: str
        """
        return self._instrument_name

    @instrument_name.setter
    def instrument_name(self, instrument_name):
        """Sets the instrument_name of this Position.

        Unique instrument identifier  # noqa: E501

        :param instrument_name: The instrument_name of this Position.  # noqa: E501
        :type: str
        """
        if instrument_name is None:
            raise ValueError("Invalid value for `instrument_name`, must not be `None`")  # noqa: E501

        self._instrument_name = instrument_name

    @property
    def size_currency(self):
        """Gets the size_currency of this Position.  # noqa: E501

        Only for futures, position size in base currency  # noqa: E501

        :return: The size_currency of this Position.  # noqa: E501
        :rtype: float
        """
        return self._size_currency

    @size_currency.setter
    def size_currency(self, size_currency):
        """Sets the size_currency of this Position.

        Only for futures, position size in base currency  # noqa: E501

        :param size_currency: The size_currency of this Position.  # noqa: E501
        :type: float
        """

        self._size_currency = size_currency

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Position):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
