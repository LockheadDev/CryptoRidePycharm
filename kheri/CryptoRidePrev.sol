// SPDX-License-Identifier: MIT

/*
TODO
- Revisar que no se pueda mandar una cantidad a una funcion que no tiene
*/

pragma solidity >=0.7.0 <0.9.0;

contract CryptoRide{  
    mapping(uint16 => ride) public idToRide;
    mapping(address => uint16[]) public driverToIds;

    struct ride{
        mapping(address => uint) addressToBid;
        mapping(address => uint) addressToPreviousBid;
        address highestBidder;
        address rider;
        address payable driver;
        address payable[] bidders;
        bool available;
        bool payed;
        string fromTime;
        string toTime;
        uint baseCost;
        uint biddingTime;
        uint biddingEndTime;
        uint16 avSeats;
    }

    function getBid(uint16 _id, address _bidder) view public returns (uint) {
        return idToRide[_id].addressToPreviousBid[_bidder];
    }

    function getPreviousBid(uint16 _id, address _bidder) view public returns (uint) {
        return idToRide[_id].addressToBid[_bidder];
    }

    function getHighestBidder(uint16 _id) view public returns(address) {
		return idToRide[_id].highestBidder;
	}

    function getRider(uint16 _id) view public returns (address) {
        return idToRide[_id].rider;
    }

    function getDriver(uint16 _id) view public returns (address) {
        return idToRide[_id].driver;
    }

    function getAvailable(uint16 _id) view public returns (bool) {
        return idToRide[_id].available;
    }

    function getPayed(uint16 _id) view public returns (bool) {
        return idToRide[_id].payed;
    }

    function getFromTime(uint16 _id) view public returns (string memory) {
        return idToRide[_id].fromTime;
    }

    function getToTime(uint16 _id) view public returns (string memory) {
        return idToRide[_id].toTime;
    }

    function getBaseCost(uint16 _id) view public returns (uint) {
        return idToRide[_id].baseCost;
    }

    function getBiddingTime(uint16 _id) view public returns (uint) {
        return idToRide[_id].biddingTime;
    }

    function getBiddingEndTime(uint16 _id) view public returns (uint) {
        return idToRide[_id].biddingEndTime;
    }

    function getAvSeats(uint16 _id) view public returns (uint16) {
        return idToRide[_id].avSeats;
    }

    modifier isAvailable(uint16 _id) {
        if(block.timestamp >= idToRide[_id].biddingEndTime) { // Si ya paso el tiempo de inicio
            idToRide[_id].available = false; // quitar la disponibilidad
        }
        require(idToRide[_id].available == true); // Requerir que este disponible 
        _;
   }
    function publishRide(uint16 _id, string calldata _fromTime, string calldata _toTime, uint _baseCost, uint _biddingTime, uint16 _avSeats) public {
        /*
        for(uint i=0; i<driverToIds[msg.sender].length; i++){ // Revisar que el driver no tenga un ride a la misma hora
            require(_toTime <= idToRide[driverToIds[msg.sender][i]].fromTime); // El tiempo de fin no puede ser mayor al tiempo de inicio de otro
            require(_fromTime >= idToRide[driverToIds[msg.sender][i]].toTime); // El tiempo de inicio no puede ser menor al tiempo de fin de otro
        }*/
        idToRide[_id].driver = payable(msg.sender); // Driver
        idToRide[_id].available = true; // Disponibilidad
        idToRide[_id].payed = false; // Pagada
        idToRide[_id].fromTime = _fromTime; // Tiempo de inicio
        idToRide[_id].toTime = _toTime; // Tiempo de fin
        idToRide[_id].baseCost = _baseCost; // Costo minimo
        idToRide[_id].avSeats = _avSeats; // Asientos
        idToRide[_id].biddingTime = _biddingTime; // Tiempo para hacer bids
        idToRide[_id].biddingEndTime = (block.timestamp + _biddingTime); // Tiempo de fin de bids
        driverToIds[msg.sender].push(_id); // Aregar id a arreglo de ids de ese usuario
    }

    function bidForRide(uint16 _id) public payable isAvailable(_id) {
        require(msg.sender != idToRide[_id].highestBidder); // La persona que esta haciendo el bid no puede ser el highest bidder
        require(msg.value > idToRide[_id].addressToBid[idToRide[_id].highestBidder]); // La cantidad mandada al contrato no puede ser menor al highest bid
        require(msg.value >= idToRide[_id].baseCost); // La cantidad mandada al contrato no puede ser menor al costo base
        if(idToRide[_id].addressToBid[msg.sender] > 0) { // Si el bidder ya habia hecho un bid
            idToRide[_id].addressToPreviousBid[msg.sender] += idToRide[_id].addressToBid[msg.sender]; // acumular el bid anterior
        }
        idToRide[_id].addressToBid[msg.sender] = msg.value; // Guardar el bid actual
        idToRide[_id].highestBidder = msg.sender; // Registrar como highest bidder
    }

    modifier isNotPaid(uint16 _id) {
        if(block.timestamp >= idToRide[_id].biddingEndTime) { // Si ya paso el tiempo de inicio
            idToRide[_id].available = false; // quitar la disponibilidad
        }
        require(idToRide[_id].available == false); // Requerir que no este disponible
        require(idToRide[_id].payed == false); // Requerir que no haya sido pagada previamente
        _;
   }

    function startRide(uint16 _id) public isNotPaid(_id) {
        require(idToRide[_id].driver == msg.sender);
        for(uint i=0; i<idToRide[_id].bidders.length; i++){
            if(idToRide[_id].bidders[i] == idToRide[_id].highestBidder){ // Si el bidder es el highest bidder
                idToRide[_id].driver.transfer(idToRide[_id].addressToBid[idToRide[_id].highestBidder]); // pagar al driver
            }else{  // Si el bidder no gano
                idToRide[_id].bidders[i].transfer(idToRide[_id].addressToBid[idToRide[_id].bidders[i]]); // regresar bid mas grande
                idToRide[_id].bidders[i].transfer(idToRide[_id].addressToPreviousBid[idToRide[_id].bidders[i]]); // y el resto de bids
            }
        }
        idToRide[_id].rider = idToRide[_id].highestBidder; // Registrar al highset bidder como el rider
        idToRide[_id].payed = true; // Pagado
    }
}