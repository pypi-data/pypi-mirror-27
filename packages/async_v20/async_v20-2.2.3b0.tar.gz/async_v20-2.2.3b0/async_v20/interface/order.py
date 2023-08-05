from .decorators import endpoint, shortcut
from ..definitions.types import ClientExtensions
from ..definitions.types import ClientID
from ..definitions.types import DateTime
from ..definitions.types import InstrumentName
from ..definitions.types import LimitOrderRequest
from ..definitions.types import MarketIfTouchedOrderRequest
from ..definitions.types import MarketOrderRequest
from ..definitions.types import OrderID
from ..definitions.types import OrderPositionFill
from ..definitions.types import OrderRequest
from ..definitions.types import OrderSpecifier
from ..definitions.types import OrderStateFilter
from ..definitions.types import OrderTriggerCondition
from ..definitions.types import OrderType
from ..definitions.types import PriceValue
from ..definitions.types import StopLossDetails
from ..definitions.types import StopLossOrderRequest
from ..definitions.types import StopOrderRequest
from ..definitions.types import TakeProfitDetails
from ..definitions.types import TakeProfitOrderRequest
from ..definitions.types import TimeInForce
from ..definitions.types import TradeID
from ..definitions.types import TrailingStopLossDetails
from ..definitions.types import TrailingStopLossOrderRequest
from ..definitions.types import Unit
from ..endpoints.annotations import Count
from ..endpoints.annotations import Ids
from ..endpoints.annotations import TradeClientExtensions
from ..endpoints.order import *

__all__ = ['OrderInterface']


class OrderInterface(object):
    @endpoint(POSTOrders)
    def post_order(self, order_request: OrderRequest = ...):
        """
        Post an OrderRequest.

        Args:

            order_request: :class:`~async_v20.definitions.types.OrderRequest`
                or a class derived from OrderRequest

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        pass

    @shortcut
    def create_order(self, instrument: InstrumentName, units: Unit, type: OrderType = 'MARKET',
                     trade_id: TradeID = ..., price: PriceValue = ..., client_trade_id: ClientID = ...,
                     time_in_force: TimeInForce = ..., gtd_time: DateTime = ...,
                     trigger_condition: OrderTriggerCondition = ..., client_extensions: ClientExtensions = ...,
                     distance: PriceValue = ..., price_bound: PriceValue = ...,
                     position_fill: OrderPositionFill = ..., take_profit_on_fill: TakeProfitDetails = ...,
                     stop_loss_on_fill: StopLossDetails = ...,
                     trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                     trade_client_extensions: ClientExtensions = ...):
        """
        create an OrderRequest

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(
            order_request=OrderRequest(
                instrument=instrument, units=units, type=type, trade_id=trade_id, price=price,
                client_trade_id=client_trade_id, time_in_force=time_in_force, gtd_time=gtd_time,
                trigger_condition=trigger_condition, client_extensions=client_extensions,
                distance=distance, price_bound=price_bound, position_fill=position_fill,
                take_profit_on_fill=take_profit_on_fill, stop_loss_on_fill=stop_loss_on_fill,
                trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
                trade_client_extensions=trade_client_extensions))

    @endpoint(GETOrders)
    def list_orders(self,
                    ids: Ids = ...,
                    state: OrderStateFilter = ...,
                    instrument: InstrumentName = ...,
                    count: Count = ...,
                    before_id: OrderID = ...):
        """
        Get a list of Orders for an Account

        Args:

            ids: :class:`~async_v20.endpoints.annotations.Ids`
            list of Order IDs to retrieve
            state: :class:`~async_v20.definitions.primitives.OrderStateFilter`
                The state to filter the requested Orders by
            instrument: :class:`~async_v20.definitions.primitives.InstrumentName`
                The instrument to filter the requested orders by
            count: :class:`~async_v20.endpoints.annotations.Count`
                The maximum number of Orders to return
            before_id: :class:`~async_v20.definitions.primitives.OrderID`
                The maximum Order ID to return. If not provided the most recent
                Orders in the Account are returned

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (orders= :class:`~async_v20.definitions.types.ArrayOrder`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

        """
        pass

    @endpoint(GETPendingOrders)
    def list_pending_orders(self):
        """
        List all pending Orders

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (orders= :class:`~async_v20.definitions.types.ArrayOrder`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

        """
        pass

    @endpoint(GETOrderSpecifier)
    def get_order(self, order_specifier: OrderSpecifier = ...):
        """
        Get details for a single Order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The Order Specifier

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (order= :class:`~async_v20.definitions.types.Order`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

        """
        pass

    @endpoint(PUTOrderSpecifier)
    def replace_order(self,
                      order_specifier: OrderSpecifier = ...,
                      order_request: OrderRequest = ...):
        """
        Replace an Order  by simultaneously cancelling it and
        creating a replacement Order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The Order Specifier
            order_request: :class:`~async_v20.definitions.types.OrderRequest`
                Specification of the replacing Order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        pass

    @endpoint(PUTOrderSpecifierCancel)
    def cancel_order(self, order_specifier: OrderSpecifier = ...):
        """
        Cancel a pending Order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The Order Specifier

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.OrderCancelRejectTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        pass

    @endpoint(PUTClientExtensions)
    def set_client_extensions(self,
                              order_specifier: OrderSpecifier = ...,
                              client_extensions: ClientExtensions = ...,
                              trade_client_extensions: TradeClientExtensions = ...):
        """
        Update the Client Extensions for an Order . Do not set,
        modify, or delete clientExtensions if your account is associated with
        MT4.

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The Order Specifier
            client_extensions: :class:`~async_v20.definitions.types.ClientExtensions`
                The Client Extensions to update for the Order. Do not set,
                modify, or delete clientExtensions if your account is
                associated with MT4.
            trade_client_extensions: :class:`~async_v20.endpoints.annotations.TradeClientExtensions`
                The Client Extensions to update for the Trade created when the
                Order is filled. Do not set, modify, or delete clientExtensions
                if your account is associated with MT4.

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (orderClientExtensionsModifyTransaction=
                :class:`~async_v20.definitions.types.OrderClientExtensionsModifyTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderClientExtensionsModifyRejectTransaction=
                :class:`~async_v20.definitions.types.OrderClientExtensionsModifyRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderClientExtensionsModifyRejectTransaction=
                :class:`~async_v20.definitions.types.OrderClientExtensionsModifyRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        pass

    @shortcut
    def market_order(self, instrument: InstrumentName, units: Unit,
                     time_in_force: TimeInForce = 'FOK', price_bound: PriceValue = ...,
                     position_fill: OrderPositionFill = 'DEFAULT', client_extensions: ClientExtensions = ...,
                     take_profit_on_fill: TakeProfitDetails = ..., stop_loss_on_fill: StopLossDetails = ...,
                     trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                     trade_client_extensions: ClientExtensions = ...):
        """
        Create a Market Order Request

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(
            order_request=MarketOrderRequest(instrument=instrument, units=units, time_in_force=time_in_force,
                                             price_bound=price_bound, position_fill=position_fill,
                                             client_extensions=client_extensions,
                                             take_profit_on_fill=take_profit_on_fill,
                                             stop_loss_on_fill=stop_loss_on_fill,
                                             trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
                                             trade_client_extensions=trade_client_extensions
                                             ))

    @shortcut
    def limit_order(self, instrument: InstrumentName, units: Unit, price: PriceValue,
                    time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                    position_fill: OrderPositionFill = 'DEFAULT', trigger_condition: OrderTriggerCondition = 'DEFAULT',
                    client_extensions: ClientExtensions = ..., take_profit_on_fill: TakeProfitDetails = ...,
                    stop_loss_on_fill: StopLossDetails = ...,
                    trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                    trade_client_extensions: ClientExtensions = ...):
        """
        Create a Limit Order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(order_request=LimitOrderRequest(
            instrument=instrument, units=units, price=price,
            time_in_force=time_in_force, gtd_time=gtd_time,
            position_fill=position_fill,
            trigger_condition=trigger_condition,
            client_extensions=client_extensions,
            take_profit_on_fill=take_profit_on_fill,
            stop_loss_on_fill=stop_loss_on_fill,
            trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
            trade_client_extensions=trade_client_extensions
        ))

    @endpoint(PUTOrderSpecifier)
    def limit_replace_order(self,
                            order_specifier: OrderSpecifier,
                            order_request: LimitOrderRequest):
        """
        Replace a pending Limit Order

        Args:
            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the Limit Order to replace
            order: :class:`~async_v20.definitions.types.LimitOrderRequest`
                The arguments to create a LimitOrderRequest

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        pass

    @shortcut
    def stop_order(self, trade_id: TradeID, price: PriceValue,
                   client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                   trigger_condition: OrderTriggerCondition = 'DEFAULT', client_extensions: ClientExtensions = ...):
        """
        Create a Stop Order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(
            order_request=StopLossOrderRequest(
                trade_id=trade_id, price=price, client_trade_id=client_trade_id,
                time_in_force=time_in_force, gtd_time=gtd_time,
                trigger_condition=trigger_condition, client_extensions=client_extensions
            ))

    @shortcut
    def stop_replace_order(self,
                           order_specifier: OrderSpecifier,
                           instrument: InstrumentName, units: Unit, price: PriceValue,
                           price_bound: PriceValue = ..., time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                           position_fill: OrderPositionFill = 'DEFAULT',
                           trigger_condition: OrderTriggerCondition = 'DEFAULT',
                           client_extensions: ClientExtensions = ..., take_profit_on_fill: TakeProfitDetails = ...,
                           stop_loss_on_fill: StopLossDetails = ...,
                           trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                           trade_client_extensions: ClientExtensions = ...):
        """
        Replace a pending Stop Order

        Args:
            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the Stop Order to replace
            order: :class:`~async_v20.definitions.types.StopOrderRequest`
                The arguments to create a StopOrderRequest

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        return self.replace_order(order_specifier=order_specifier,
                           order_request=StopOrderRequest(
                               instrument=instrument, units=units, price=price,
                               price_bound=price_bound, time_in_force=time_in_force,
                               gtd_time=gtd_time, position_fill=position_fill,
                               trigger_condition=trigger_condition,
                               client_extensions=client_extensions,
                               take_profit_on_fill=take_profit_on_fill,
                               stop_loss_on_fill=stop_loss_on_fill,
                               trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
                               trade_client_extensions=trade_client_extensions
                           ))

    @shortcut
    def market_if_touched_order(self, instrument: InstrumentName, units: Unit, price: PriceValue,
                                price_bound: PriceValue = ...,
                                time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                                position_fill: OrderPositionFill = 'DEFAULT',
                                trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                client_extensions: ClientExtensions = ...,
                                take_profit_on_fill: TakeProfitDetails = ...,
                                stop_loss_on_fill: StopLossDetails = ...,
                                trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                                trade_client_extensions: ClientExtensions = ...):
        """
        Create a market if touched order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(
            order_request=MarketIfTouchedOrderRequest(
                instrument=instrument, units=units, price=price,
                price_bound=price_bound, time_in_force=time_in_force,
                gtd_time=gtd_time, position_fill=position_fill,
                trigger_condition=trigger_condition,
                client_extensions=client_extensions,
                take_profit_on_fill=take_profit_on_fill,
                stop_loss_on_fill=stop_loss_on_fill,
                trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
                trade_client_extensions=trade_client_extensions
            ))

    @shortcut
    def market_if_touched_replace_order(self,
                                        order_specifier: OrderSpecifier,
                                        instrument: InstrumentName, units: Unit, price: PriceValue,
                                        price_bound: PriceValue = ...,
                                        time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                                        position_fill: OrderPositionFill = 'DEFAULT',
                                        trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                        client_extensions: ClientExtensions = ...,
                                        take_profit_on_fill: TakeProfitDetails = ...,
                                        stop_loss_on_fill: StopLossDetails = ...,
                                        trailing_stop_loss_on_fill: TrailingStopLossDetails = ...,
                                        trade_client_extensions: ClientExtensions = ...
                                        ):
        """
        Replace a pending market if touched order

        Args:
            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the MarketIfTouched Order to replace
            order: :class:`~async_v20.definitions.types.MarketIfTouchedOrderRequest`
                The arguments to create a MarketIfTouchedOrderRequest

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        return self.replace_order(order_specifier=order_specifier,
                                  order_request=MarketIfTouchedOrderRequest(
                                      instrument=instrument, units=units,
                                      price=price, price_bound=price_bound,
                                      time_in_force=time_in_force,
                                      gtd_time=gtd_time,
                                      position_fill=position_fill,
                                      trigger_condition=trigger_condition,
                                      client_extensions=client_extensions,
                                      take_profit_on_fill=take_profit_on_fill,
                                      stop_loss_on_fill=stop_loss_on_fill,
                                      trailing_stop_loss_on_fill=trailing_stop_loss_on_fill,
                                      trade_client_extensions=trade_client_extensions)
                                  )

    @shortcut
    def take_profit_order(self, trade_id: TradeID, price: PriceValue,
                          client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC',
                          gtd_time: DateTime = ...,
                          trigger_condition: OrderTriggerCondition = 'DEFAULT',
                          client_extensions: ClientExtensions = ...):
        """
        Create a take profit order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        return self.post_order(
            order_request=TakeProfitOrderRequest(
                trade_id=trade_id, price=price, client_trade_id=client_trade_id,
                time_in_force=time_in_force, gtd_time=gtd_time,
                trigger_condition=trigger_condition,
                client_extensions=client_extensions
            ))

    @shortcut
    def take_profit_replace_order(self,
                                  order_specifier: OrderSpecifier,
                                  trade_id: TradeID, price: PriceValue,
                                  client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC',
                                  gtd_time: DateTime = ...,
                                  trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                  client_extensions: ClientExtensions = ...
                                  ):
        """
        Replace a pending take profit order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the Take Profit Order to replace
            order: :class:`~async_v20.definitions.types.TakeProfitOrderRequest`

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.replace_order(order_specifier=order_specifier,
                                  order_request=TakeProfitOrderRequest(
                                      trade_id=trade_id, price=price,
                                      client_trade_id=client_trade_id,
                                      time_in_force=time_in_force, gtd_time=gtd_time,
                                      trigger_condition=trigger_condition,
                                      client_extensions=client_extensions)
                                  )

    @shortcut
    def stop_loss_order(self, trade_id: TradeID, price: PriceValue,
                        client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC', gtd_time: DateTime = ...,
                        trigger_condition: OrderTriggerCondition = 'DEFAULT',
                        client_extensions: ClientExtensions = ...):
        """
        Create a Stop Loss Order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(
            order_request=StopLossOrderRequest(
                trade_id=trade_id, price=price, client_trade_id=client_trade_id,
                time_in_force=time_in_force, gtd_time=gtd_time,
                trigger_condition=trigger_condition, client_extensions=client_extensions
            ))

    @shortcut
    def stop_loss_replace_order(self, order_specifier: OrderSpecifier,
                                trade_id: TradeID, price: PriceValue,
                                client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC',
                                gtd_time: DateTime = ...,
                                trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                client_extensions: ClientExtensions = ...):
        """
        Replace a pending Stop Loss Order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the Stop Loss Order to replace
            order: :class:`~async_v20.definitions.types.StopLossOrderRequest`

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

        """
        return self.replace_order(order_specifier=order_specifier,
                                  order_request=StopLossOrderRequest(
                                      trade_id=trade_id, price=price,
                                      client_trade_id=client_trade_id,
                                      time_in_force=time_in_force, gtd_time=gtd_time,
                                      trigger_condition=trigger_condition,
                                      client_extensions=client_extensions
                                  ))

    @shortcut
    def trailing_stop_loss_order(self, trade_id: TradeID, distance: PriceValue,
                                 client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC',
                                 gtd_time: DateTime = ...,
                                 trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                 client_extensions: ClientExtensions = ...):
        """
        Create a Trailing Stop Loss Order

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.post_order(order_request=TrailingStopLossOrderRequest(
            trade_id=trade_id, distance=distance,
            client_trade_id=client_trade_id,
            time_in_force=time_in_force,
            gtd_time=gtd_time,
            trigger_condition=trigger_condition,
            client_extensions=client_extensions
        ))

    @shortcut
    def trailing_stop_loss_replace_order(self, order_specifier: OrderSpecifier,
                                         trade_id: TradeID, distance: PriceValue,
                                         client_trade_id: ClientID = ..., time_in_force: TimeInForce = 'GTC',
                                         gtd_time: DateTime = ...,
                                         trigger_condition: OrderTriggerCondition = 'DEFAULT',
                                         client_extensions: ClientExtensions = ...):
        """
        Replace a pending Trailing Stop Loss Order

        Args:

            order_specifier: :class:`~async_v20.definitions.primitives.OrderSpecifier`
                The ID of the Take Profit Order to replace
            order: :class:`~async_v20.definitions.types.TrailingStopLossOrderRequest`

        Returns:

            status [201]
                :class:`~async_v20.interface.response.Response`
                (orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                orderCreateTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderReissueTransaction= :class:`~async_v20.definitions.types.Transaction`,
                orderReissueRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                replacingOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderCancelRejectTransaction= :class:`~async_v20.definitions.types.Transaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        return self.replace_order(order_specifier=order_specifier,
                                  order_request=TrailingStopLossOrderRequest(
                                      trade_id=trade_id, distance=distance,
                                      client_trade_id=client_trade_id,
                                      time_in_force=time_in_force,
                                      gtd_time=gtd_time,
                                      trigger_condition=trigger_condition,
                                      client_extensions=client_extensions
                                  ))
