pragma solidity ^0.4.18;

import "./DecentralizedOrderBook.sol";

contract SlotManager{
    struct Trade {
        uint index;
        // no need to store the timestamp : implicitly given in the index
        //uint ts;
        uint quantity;
        uint price;
        address proposer;
        bool direction;
    }
    // no need of enum we just use a boolean
    //enum DirectionChoices { Bid, Sell }

    uint public slotPrice;
    bool public slotDirection;
    Trade[] orderBook;
    mapping (bytes32 => uint) private indexesMap;
    uint slotNumberOrder;
    DecentralizedOrderBook parent;

    function SlotManager(address _parent,uint _slotPrice){
        parent = DecentralizedOrderBook(_parent);
        slotPrice = _slotPrice;
    }

   function stackNewOrder(uint _quantity, uint _price, bool _direction, address _proposer){
        bytes32 tradeHash = keccak256(_quantity, _price, _direction, _proposer);
        indexesMap[tradeHash] = slotNumberOrder;
        Trade memory incomingTrade = Trade({index:slotNumberOrder,
                                            quantity: _quantity,
                                            price: _price,
                                            proposer: _proposer,
                                            direction:_direction});
        orderBook.push(incomingTrade);
        slotNumberOrder = slotNumberOrder+1;
   }

    function handleSlotOrder(uint _quantity, uint _price, bool _direction, address _proposer) public returns (uint){
        // this slot is empty
        // it takes the direction of the first incoming order
        // it then stores the order waiting for an order in the opposite direction
        if (slotNumberOrder == 0){
            // the slot has no direction for the moment : we give it one
            slotDirection = _direction;
            // we stack the incoming order because in the same direction of the slot
            stackNewOrder(_quantity,_price,_direction,_proposer);
        } else if (_direction == slotDirection){
            // we stack the incoming order because in the same direction of the slot
            stackNewOrder(_quantity,_price,_direction,_proposer);
        } else {
            // we loop over all existing orders
            // trying to fill up the incoming order
            // the slot is bid : the incoming order is an ask and the stacked orders are bid
            if (slotDirection){
                uint indexOrderToSuppress = 0;
                for(uint i=0; i< orderBook.length; i++){
                    Trade waitingTrade = orderBook[i];
                    if (waitingTrade.quantity <= _quantity){
                        // the waiting trade which wants to buy will receive the tokens
                        parent.settleToken(_proposer,waitingTrade.proposer,waitingTrade.quantity);
                        parent.settleCash(waitingTrade.proposer,_proposer,waitingTrade.quantity,waitingTrade.price);
                        _quantity = _quantity - waitingTrade.quantity;
                        indexOrderToSuppress = i+1;
                    } else {
                        // the waiting trade which wants to buy will receive the tokens
                        parent.settleToken(_proposer,waitingTrade.proposer,_quantity);
                        parent.settleCash(waitingTrade.proposer,_proposer,_quantity,waitingTrade.price);
                        orderBook[i].quantity = orderBook[i].quantity-_quantity;
                        _quantity = 0;
                    }
                    if (_quantity == 0){
                        break;
                    }
    	        }
    	        reallocateOrderBook(indexOrderToSuppress);
            } else {
            // the slot is ask : the incoming order is a bid
            // @todo : do the other side the waiting orders are ask selling orders
            }

        }
        return _quantity;
    }

    function handleSlotDeleteOrder(uint _quantity, uint _price, bool _direction, address _proposer) {
        bytes32 tradeHash = keccak256(_quantity, _price, _direction, _proposer);
        uint orderIndex = indexesMap[tradeHash];
        // @todo : delete order : use the keccak256 function to find back the order
        // and then suppress it from the order book array
        // and then give back the money and cancell the allowance
    }

    function reallocateOrderBook(uint lastIndexToSuppress){
        //worst case : all order books disappear : lastIndexToSuppress == orderBook.length
        // lastIndexToSuppress == 0 : we suppress nothing
        if (lastIndexToSuppress >= orderBook.length) return;

        // the one at lastIndexToSuppress is the first not to suppress
        for (uint i = lastIndexToSuppress; i<orderBook.length; i++){
            orderBook[i-lastIndexToSuppress] = orderBook[i];
        }

        for (uint j = orderBook.length - lastIndexToSuppress; j<orderBook.length; j++){
            orderBook[j] = orderBook[j+lastIndexToSuppress];
            delete orderBook[j];
        }

        orderBook.length = orderBook.length -lastIndexToSuppress;

    }
}
