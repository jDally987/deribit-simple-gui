# coding: utf-8

"""
    Deribit API

    #Overview  Deribit provides three different interfaces to access the API:  * [JSON-RPC over Websocket](#json-rpc) * [JSON-RPC over HTTP](#json-rpc) * [FIX](#fix-api) (Financial Information eXchange)  With the API Console you can use and test the JSON-RPC API, both via HTTP and  via Websocket. To visit the API console, go to __Account > API tab >  API Console tab.__   ##Naming Deribit tradeable assets or instruments use the following system of naming:  |Kind|Examples|Template|Comments| |----|--------|--------|--------| |Future|<code>BTC-25MAR16</code>, <code>BTC-5AUG16</code>|<code>BTC-DMMMYY</code>|<code>BTC</code> is currency, <code>DMMMYY</code> is expiration date, <code>D</code> stands for day of month (1 or 2 digits), <code>MMM</code> - month (3 first letters in English), <code>YY</code> stands for year.| |Perpetual|<code>BTC-PERPETUAL</code>                        ||Perpetual contract for currency <code>BTC</code>.| |Option|<code>BTC-25MAR16-420-C</code>, <code>BTC-5AUG16-580-P</code>|<code>BTC-DMMMYY-STRIKE-K</code>|<code>STRIKE</code> is option strike price in USD. Template <code>K</code> is option kind: <code>C</code> for call options or <code>P</code> for put options.|   # JSON-RPC JSON-RPC is a light-weight remote procedure call (RPC) protocol. The  [JSON-RPC specification](https://www.jsonrpc.org/specification) defines the data structures that are used for the messages that are exchanged between client and server, as well as the rules around their processing. JSON-RPC uses JSON (RFC 4627) as data format.  JSON-RPC is transport agnostic: it does not specify which transport mechanism must be used. The Deribit API supports both Websocket (preferred) and HTTP (with limitations: subscriptions are not supported over HTTP).  ## Request messages > An example of a request message:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 8066,     \"method\": \"public/ticker\",     \"params\": {         \"instrument\": \"BTC-24AUG18-6500-P\"     } } ```  According to the JSON-RPC sepcification the requests must be JSON objects with the following fields.  |Name|Type|Description| |----|----|-----------| |jsonrpc|string|The version of the JSON-RPC spec: \"2.0\"| |id|integer or string|An identifier of the request. If it is included, then the response will contain the same identifier| |method|string|The method to be invoked| |params|object|The parameters values for the method. The field names must match with the expected parameter names. The parameters that are expected are described in the documentation for the methods, below.|  <aside class=\"warning\"> The JSON-RPC specification describes two features that are currently not supported by the API:  <ul> <li>Specification of parameter values by position</li> <li>Batch requests</li> </ul>  </aside>   ## Response messages > An example of a response message:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 5239,     \"testnet\": false,     \"result\": [         {             \"currency\": \"BTC\",             \"currencyLong\": \"Bitcoin\",             \"minConfirmation\": 2,             \"txFee\": 0.0006,             \"isActive\": true,             \"coinType\": \"BITCOIN\",             \"baseAddress\": null         }     ],     \"usIn\": 1535043730126248,     \"usOut\": 1535043730126250,     \"usDiff\": 2 } ```  The JSON-RPC API always responds with a JSON object with the following fields.   |Name|Type|Description| |----|----|-----------| |id|integer|This is the same id that was sent in the request.| |result|any|If successful, the result of the API call. The format for the result is described with each method.| |error|error object|Only present if there was an error invoking the method. The error object is described below.| |testnet|boolean|Indicates whether the API in use is actually the test API.  <code>false</code> for production server, <code>true</code> for test server.| |usIn|integer|The timestamp when the requests was received (microseconds since the Unix epoch)| |usOut|integer|The timestamp when the response was sent (microseconds since the Unix epoch)| |usDiff|integer|The number of microseconds that was spent handling the request|  <aside class=\"notice\"> The fields <code>testnet</code>, <code>usIn</code>, <code>usOut</code> and <code>usDiff</code> are not part of the JSON-RPC standard.  <p>In order not to clutter the examples they will generally be omitted from the example code.</p> </aside>  > An example of a response with an error:  ```json {     \"jsonrpc\": \"2.0\",     \"id\": 8163,     \"error\": {         \"code\": 11050,         \"message\": \"bad_request\"     },     \"testnet\": false,     \"usIn\": 1535037392434763,     \"usOut\": 1535037392448119,     \"usDiff\": 13356 } ``` In case of an error the response message will contain the error field, with as value an object with the following with the following fields:  |Name|Type|Description |----|----|-----------| |code|integer|A number that indicates the kind of error.| |message|string|A short description that indicates the kind of error.| |data|any|Additional data about the error. This field may be omitted.|  ## Notifications  > An example of a notification:  ```json {     \"jsonrpc\": \"2.0\",     \"method\": \"subscription\",     \"params\": {         \"channel\": \"deribit_price_index.btc_usd\",         \"data\": {             \"timestamp\": 1535098298227,             \"price\": 6521.17,             \"index_name\": \"btc_usd\"         }     } } ```  API users can subscribe to certain types of notifications. This means that they will receive JSON-RPC notification-messages from the server when certain events occur, such as changes to the index price or changes to the order book for a certain instrument.   The API methods [public/subscribe](#public-subscribe) and [private/subscribe](#private-subscribe) are used to set up a subscription. Since HTTP does not support the sending of messages from server to client, these methods are only availble when using the Websocket transport mechanism.  At the moment of subscription a \"channel\" must be specified. The channel determines the type of events that will be received.  See [Subscriptions](#subscriptions) for more details about the channels.  In accordance with the JSON-RPC specification, the format of a notification  is that of a request message without an <code>id</code> field. The value of the <code>method</code> field will always be <code>\"subscription\"</code>. The <code>params</code> field will always be an object with 2 members: <code>channel</code> and <code>data</code>. The value of the <code>channel</code> member is the name of the channel (a string). The value of the <code>data</code> member is an object that contains data  that is specific for the channel.   ## Authentication  > An example of a JSON request with token:  ```json {     \"id\": 5647,     \"method\": \"private/get_subaccounts\",     \"params\": {         \"access_token\": \"67SVutDoVZSzkUStHSuk51WntMNBJ5mh5DYZhwzpiqDF\"     } } ```  The API consists of `public` and `private` methods. The public methods do not require authentication. The private methods use OAuth 2.0 authentication. This means that a valid OAuth access token must be included in the request, which can get achived by calling method [public/auth](#public-auth).  When the token was assigned to the user, it should be passed along, with other request parameters, back to the server:  |Connection type|Access token placement |----|-----------| |**Websocket**|Inside request JSON parameters, as an `access_token` field| |**HTTP (REST)**|Header `Authorization: bearer ```Token``` ` value|  ### Additional authorization method - basic user credentials  <span style=\"color:red\"><b> ! Not recommended - however, it could be useful for quick testing API</b></span></br>  Every `private` method could be accessed by providing, inside HTTP `Authorization: Basic XXX` header, values with user `ClientId` and assigned `ClientSecret` (both values can be found on the API page on the Deribit website) encoded with `Base64`:  <code>Authorization: Basic BASE64(`ClientId` + `:` + `ClientSecret`)</code>   ### Additional authorization method - Deribit signature credentials  The Derbit service provides dedicated authorization method, which harness user generated signature to increase security level for passing request data. Generated value is passed inside `Authorization` header, coded as:  <code>Authorization: deri-hmac-sha256 id=```ClientId```,ts=```Timestamp```,sig=```Signature```,nonce=```Nonce```</code>  where:  |Deribit credential|Description |----|-----------| |*ClientId*|Can be found on the API page on the Deribit website| |*Timestamp*|Time when the request was generated - given as **miliseconds**. It's valid for **60 seconds** since generation, after that time any request with an old timestamp will be rejected.| |*Signature*|Value for signature calculated as described below | |*Nonce*|Single usage, user generated initialization vector for the server token|  The signature is generated by the following formula:  <code> Signature = HEX_STRING( HMAC-SHA256( ClientSecret, StringToSign ) );</code></br>  <code> StringToSign =  Timestamp + \"\\n\" + Nonce + \"\\n\" + RequestData;</code></br>  <code> RequestData =  UPPERCASE(HTTP_METHOD())  + \"\\n\" + URI() + \"\\n\" + RequestBody + \"\\n\";</code></br>   e.g. (using shell with ```openssl``` tool):  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientId=AAAAAAAAAAA</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientSecret=ABCD</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Timestamp=$( date +%s000 )</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Nonce=$( cat /dev/urandom | tr -dc 'a-z0-9' | head -c8 )</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;URI=\"/api/v2/private/get_account_summary?currency=BTC\"</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;HttpMethod=GET</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Body=\"\"</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Signature=$( echo -ne \"${Timestamp}\\n${Nonce}\\n${HttpMethod}\\n${URI}\\n${Body}\\n\" | openssl sha256 -r -hmac \"$ClientSecret\" | cut -f1 -d' ' )</code></br></br> <code>&nbsp;&nbsp;&nbsp;&nbsp;echo $Signature</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;shell output> ea40d5e5e4fae235ab22b61da98121fbf4acdc06db03d632e23c66bcccb90d2c  (**WARNING**: Exact value depends on current timestamp and client credentials</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;curl -s -X ${HttpMethod} -H \"Authorization: deri-hmac-sha256 id=${ClientId},ts=${Timestamp},nonce=${Nonce},sig=${Signature}\" \"https://www.deribit.com${URI}\"</code></br></br>    ### Additional authorization method - signature credentials (WebSocket API)  When connecting through Websocket, user can request for authorization using ```client_credential``` method, which requires providing following parameters (as a part of JSON request):  |JSON parameter|Description |----|-----------| |*grant_type*|Must be **client_signature**| |*client_id*|Can be found on the API page on the Deribit website| |*timestamp*|Time when the request was generated - given as **miliseconds**. It's valid for **60 seconds** since generation, after that time any request with an old timestamp will be rejected.| |*signature*|Value for signature calculated as described below | |*nonce*|Single usage, user generated initialization vector for the server token| |*data*|**Optional** field, which contains any user specific value|  The signature is generated by the following formula:  <code> StringToSign =  Timestamp + \"\\n\" + Nonce + \"\\n\" + Data;</code></br>  <code> Signature = HEX_STRING( HMAC-SHA256( ClientSecret, StringToSign ) );</code></br>   e.g. (using shell with ```openssl``` tool):  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientId=AAAAAAAAAAA</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;ClientSecret=ABCD</code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Timestamp=$( date +%s000 ) # e.g. 1554883365000 </code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Nonce=$( cat /dev/urandom | tr -dc 'a-z0-9' | head -c8 ) # e.g. fdbmmz79 </code></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Data=\"\"</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;Signature=$( echo -ne \"${Timestamp}\\n${Nonce}\\n${Data}\\n\" | openssl sha256 -r -hmac \"$ClientSecret\" | cut -f1 -d' ' )</code></br></br> <code>&nbsp;&nbsp;&nbsp;&nbsp;echo $Signature</code></br></br>  <code>&nbsp;&nbsp;&nbsp;&nbsp;shell output> e20c9cd5639d41f8bbc88f4d699c4baf94a4f0ee320e9a116b72743c449eb994  (**WARNING**: Exact value depends on current timestamp and client credentials</code></br></br>   You can also check the signature value using some online tools like, e.g: [https://codebeautify.org/hmac-generator](https://codebeautify.org/hmac-generator) (but don't forget about adding *newline* after each part of the hashed text and remember that you **should use** it only with your **test credentials**).   Here's a sample JSON request created using the values from the example above:  <code> {                            </br> &nbsp;&nbsp;\"jsonrpc\" : \"2.0\",         </br> &nbsp;&nbsp;\"id\" : 9929,               </br> &nbsp;&nbsp;\"method\" : \"public/auth\",  </br> &nbsp;&nbsp;\"params\" :                 </br> &nbsp;&nbsp;{                        </br> &nbsp;&nbsp;&nbsp;&nbsp;\"grant_type\" : \"client_signature\",   </br> &nbsp;&nbsp;&nbsp;&nbsp;\"client_id\" : \"AAAAAAAAAAA\",         </br> &nbsp;&nbsp;&nbsp;&nbsp;\"timestamp\": \"1554883365000\",        </br> &nbsp;&nbsp;&nbsp;&nbsp;\"nonce\": \"fdbmmz79\",                 </br> &nbsp;&nbsp;&nbsp;&nbsp;\"data\": \"\",                          </br> &nbsp;&nbsp;&nbsp;&nbsp;\"signature\" : \"e20c9cd5639d41f8bbc88f4d699c4baf94a4f0ee320e9a116b72743c449eb994\"  </br> &nbsp;&nbsp;}                        </br> }                            </br> </code>   ### Access scope  When asking for `access token` user can provide the required access level (called `scope`) which defines what type of functionality he/she wants to use, and whether requests are only going to check for some data or also to update them.  Scopes are required and checked for `private` methods, so if you plan to use only `public` information you can stay with values assigned by default.  |Scope|Description |----|-----------| |*account:read*|Access to **account** methods - read only data| |*account:read_write*|Access to **account** methods - allows to manage account settings, add subaccounts, etc.| |*trade:read*|Access to **trade** methods - read only data| |*trade:read_write*|Access to **trade** methods - required to create and modify orders| |*wallet:read*|Access to **wallet** methods - read only data| |*wallet:read_write*|Access to **wallet** methods - allows to withdraw, generate new deposit address, etc.| |*wallet:none*, *account:none*, *trade:none*|Blocked access to specified functionality|    <span style=\"color:red\">**NOTICE:**</span> Depending on choosing an authentication method (```grant type```) some scopes could be narrowed by the server. e.g. when ```grant_type = client_credentials``` and ```scope = wallet:read_write``` it's modified by the server as ```scope = wallet:read```\"   ## JSON-RPC over websocket Websocket is the prefered transport mechanism for the JSON-RPC API, because it is faster and because it can support [subscriptions](#subscriptions) and [cancel on disconnect](#private-enable_cancel_on_disconnect). The code examples that can be found next to each of the methods show how websockets can be used from Python or Javascript/node.js.  ## JSON-RPC over HTTP Besides websockets it is also possible to use the API via HTTP. The code examples for 'shell' show how this can be done using curl. Note that subscriptions and cancel on disconnect are not supported via HTTP.  #Methods   # noqa: E501

    OpenAPI spec version: 2.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import openapi_client
from openapi_client.api.private_api import PrivateApi  # noqa: E501
from openapi_client.rest import ApiException


class TestPrivateApi(unittest.TestCase):
    """PrivateApi unit test stubs"""

    def setUp(self):
        self.api = openapi_client.api.private_api.PrivateApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_private_add_to_address_book_get(self):
        """Test case for private_add_to_address_book_get

        Adds new entry to address book of given type  # noqa: E501
        """
        pass

    def test_private_buy_get(self):
        """Test case for private_buy_get

        Places a buy order for an instrument.  # noqa: E501
        """
        pass

    def test_private_cancel_all_by_currency_get(self):
        """Test case for private_cancel_all_by_currency_get

        Cancels all orders by currency, optionally filtered by instrument kind and/or order type.  # noqa: E501
        """
        pass

    def test_private_cancel_all_by_instrument_get(self):
        """Test case for private_cancel_all_by_instrument_get

        Cancels all orders by instrument, optionally filtered by order type.  # noqa: E501
        """
        pass

    def test_private_cancel_all_get(self):
        """Test case for private_cancel_all_get

        This method cancels all users orders and stop orders within all currencies and instrument kinds.  # noqa: E501
        """
        pass

    def test_private_cancel_get(self):
        """Test case for private_cancel_get

        Cancel an order, specified by order id  # noqa: E501
        """
        pass

    def test_private_cancel_transfer_by_id_get(self):
        """Test case for private_cancel_transfer_by_id_get

        Cancel transfer  # noqa: E501
        """
        pass

    def test_private_cancel_withdrawal_get(self):
        """Test case for private_cancel_withdrawal_get

        Cancels withdrawal request  # noqa: E501
        """
        pass

    def test_private_change_subaccount_name_get(self):
        """Test case for private_change_subaccount_name_get

        Change the user name for a subaccount  # noqa: E501
        """
        pass

    def test_private_close_position_get(self):
        """Test case for private_close_position_get

        Makes closing position reduce only order .  # noqa: E501
        """
        pass

    def test_private_create_deposit_address_get(self):
        """Test case for private_create_deposit_address_get

        Creates deposit address in currency  # noqa: E501
        """
        pass

    def test_private_create_subaccount_get(self):
        """Test case for private_create_subaccount_get

        Create a new subaccount  # noqa: E501
        """
        pass

    def test_private_disable_cancel_on_disconnect_get(self):
        """Test case for private_disable_cancel_on_disconnect_get

        Disable Cancel On Disconnect for the connection. This does not change the default account setting.  # noqa: E501
        """
        pass

    def test_private_disable_tfa_for_subaccount_get(self):
        """Test case for private_disable_tfa_for_subaccount_get

        Disable two factor authentication for a subaccount.  # noqa: E501
        """
        pass

    def test_private_disable_tfa_with_recovery_code_get(self):
        """Test case for private_disable_tfa_with_recovery_code_get

        Disables TFA with one time recovery code  # noqa: E501
        """
        pass

    def test_private_edit_get(self):
        """Test case for private_edit_get

        Change price, amount and/or other properties of an order.  # noqa: E501
        """
        pass

    def test_private_enable_cancel_on_disconnect_get(self):
        """Test case for private_enable_cancel_on_disconnect_get

        Enable Cancel On Disconnect for the connection. This does not change the default account setting.  # noqa: E501
        """
        pass

    def test_private_get_account_summary_get(self):
        """Test case for private_get_account_summary_get

        Retrieves user account summary.  # noqa: E501
        """
        pass

    def test_private_get_address_book_get(self):
        """Test case for private_get_address_book_get

        Retrieves address book of given type  # noqa: E501
        """
        pass

    def test_private_get_current_deposit_address_get(self):
        """Test case for private_get_current_deposit_address_get

        Retrieve deposit address for currency  # noqa: E501
        """
        pass

    def test_private_get_deposits_get(self):
        """Test case for private_get_deposits_get

        Retrieve the latest users deposits  # noqa: E501
        """
        pass

    def test_private_get_email_language_get(self):
        """Test case for private_get_email_language_get

        Retrieves the language to be used for emails.  # noqa: E501
        """
        pass

    def test_private_get_margins_get(self):
        """Test case for private_get_margins_get

        Get margins for given instrument, amount and price.  # noqa: E501
        """
        pass

    def test_private_get_new_announcements_get(self):
        """Test case for private_get_new_announcements_get

        Retrieves announcements that have not been marked read by the user.  # noqa: E501
        """
        pass

    def test_private_get_open_orders_by_currency_get(self):
        """Test case for private_get_open_orders_by_currency_get

        Retrieves list of user's open orders.  # noqa: E501
        """
        pass

    def test_private_get_open_orders_by_instrument_get(self):
        """Test case for private_get_open_orders_by_instrument_get

        Retrieves list of user's open orders within given Instrument.  # noqa: E501
        """
        pass

    def test_private_get_order_history_by_currency_get(self):
        """Test case for private_get_order_history_by_currency_get

        Retrieves history of orders that have been partially or fully filled.  # noqa: E501
        """
        pass

    def test_private_get_order_history_by_instrument_get(self):
        """Test case for private_get_order_history_by_instrument_get

        Retrieves history of orders that have been partially or fully filled.  # noqa: E501
        """
        pass

    def test_private_get_order_margin_by_ids_get(self):
        """Test case for private_get_order_margin_by_ids_get

        Retrieves initial margins of given orders  # noqa: E501
        """
        pass

    def test_private_get_order_state_get(self):
        """Test case for private_get_order_state_get

        Retrieve the current state of an order.  # noqa: E501
        """
        pass

    def test_private_get_position_get(self):
        """Test case for private_get_position_get

        Retrieve user position.  # noqa: E501
        """
        pass

    def test_private_get_positions_get(self):
        """Test case for private_get_positions_get

        Retrieve user positions.  # noqa: E501
        """
        pass

    def test_private_get_settlement_history_by_currency_get(self):
        """Test case for private_get_settlement_history_by_currency_get

        Retrieves settlement, delivery and bankruptcy events that have affected your account.  # noqa: E501
        """
        pass

    def test_private_get_settlement_history_by_instrument_get(self):
        """Test case for private_get_settlement_history_by_instrument_get

        Retrieves public settlement, delivery and bankruptcy events filtered by instrument name  # noqa: E501
        """
        pass

    def test_private_get_subaccounts_get(self):
        """Test case for private_get_subaccounts_get

        Get information about subaccounts  # noqa: E501
        """
        pass

    def test_private_get_transfers_get(self):
        """Test case for private_get_transfers_get

        Adds new entry to address book of given type  # noqa: E501
        """
        pass

    def test_private_get_user_trades_by_currency_and_time_get(self):
        """Test case for private_get_user_trades_by_currency_and_time_get

        Retrieve the latest user trades that have occurred for instruments in a specific currency symbol and within given time range.  # noqa: E501
        """
        pass

    def test_private_get_user_trades_by_currency_get(self):
        """Test case for private_get_user_trades_by_currency_get

        Retrieve the latest user trades that have occurred for instruments in a specific currency symbol.  # noqa: E501
        """
        pass

    def test_private_get_user_trades_by_instrument_and_time_get(self):
        """Test case for private_get_user_trades_by_instrument_and_time_get

        Retrieve the latest user trades that have occurred for a specific instrument and within given time range.  # noqa: E501
        """
        pass

    def test_private_get_user_trades_by_instrument_get(self):
        """Test case for private_get_user_trades_by_instrument_get

        Retrieve the latest user trades that have occurred for a specific instrument.  # noqa: E501
        """
        pass

    def test_private_get_user_trades_by_order_get(self):
        """Test case for private_get_user_trades_by_order_get

        Retrieve the list of user trades that was created for given order  # noqa: E501
        """
        pass

    def test_private_get_withdrawals_get(self):
        """Test case for private_get_withdrawals_get

        Retrieve the latest users withdrawals  # noqa: E501
        """
        pass

    def test_private_logout_get(self):
        """Test case for private_logout_get

        Gracefully close websocket connection, when COD (Cancel On Disconnect) is enabled orders are not cancelled  # noqa: E501
        """
        pass

    def test_private_remove_from_address_book_get(self):
        """Test case for private_remove_from_address_book_get

        Adds new entry to address book of given type  # noqa: E501
        """
        pass

    def test_private_sell_get(self):
        """Test case for private_sell_get

        Places a sell order for an instrument.  # noqa: E501
        """
        pass

    def test_private_set_announcement_as_read_get(self):
        """Test case for private_set_announcement_as_read_get

        Marks an announcement as read, so it will not be shown in `get_new_announcements`.  # noqa: E501
        """
        pass

    def test_private_set_email_for_subaccount_get(self):
        """Test case for private_set_email_for_subaccount_get

        Assign an email address to a subaccount. User will receive an email with confirmation link.  # noqa: E501
        """
        pass

    def test_private_set_email_language_get(self):
        """Test case for private_set_email_language_get

        Changes the language to be used for emails.  # noqa: E501
        """
        pass

    def test_private_set_password_for_subaccount_get(self):
        """Test case for private_set_password_for_subaccount_get

        Set the password for the subaccount  # noqa: E501
        """
        pass

    def test_private_submit_transfer_to_subaccount_get(self):
        """Test case for private_submit_transfer_to_subaccount_get

        Transfer funds to a subaccount.  # noqa: E501
        """
        pass

    def test_private_submit_transfer_to_user_get(self):
        """Test case for private_submit_transfer_to_user_get

        Transfer funds to a another user.  # noqa: E501
        """
        pass

    def test_private_subscribe_get(self):
        """Test case for private_subscribe_get

        Subscribe to one or more channels.  # noqa: E501
        """
        pass

    def test_private_toggle_deposit_address_creation_get(self):
        """Test case for private_toggle_deposit_address_creation_get

        Enable or disable deposit address creation  # noqa: E501
        """
        pass

    def test_private_toggle_notifications_from_subaccount_get(self):
        """Test case for private_toggle_notifications_from_subaccount_get

        Enable or disable sending of notifications for the subaccount.  # noqa: E501
        """
        pass

    def test_private_toggle_subaccount_login_get(self):
        """Test case for private_toggle_subaccount_login_get

        Enable or disable login for a subaccount. If login is disabled and a session for the subaccount exists, this session will be terminated.  # noqa: E501
        """
        pass

    def test_private_unsubscribe_get(self):
        """Test case for private_unsubscribe_get

        Unsubscribe from one or more channels.  # noqa: E501
        """
        pass

    def test_private_withdraw_get(self):
        """Test case for private_withdraw_get

        Creates a new withdrawal request  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
