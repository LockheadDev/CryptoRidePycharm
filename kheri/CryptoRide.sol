// SPDX-License-Identifier: GNU

pragma solidity >=0.7.0 <0.9.0;

contract CryptoRide{  
    mapping(uint16 => ride) public idToRide;
    //mapping(address => uint16[]) public driverToIds;

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
        string location;
        uint baseCost;
        uint16 avSeats;
    }

    function getBid(uint16 _id, address _bidder) view public returns (uint) {
        return idToRide[_id].addressToBid[_bidder];
    }

    function getPreviousBid(uint16 _id, address _bidder) view public returns (uint) {
        return idToRide[_id].addressToPreviousBid[_bidder];
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

    function getLocation(uint16 _id) view public returns (string memory) {
        return idToRide[_id].location;
    }

    function getBaseCost(uint16 _id) view public returns (uint) {
        return idToRide[_id].baseCost;
    }

    function getAvSeats(uint16 _id) view public returns (uint16) {
        return idToRide[_id].avSeats;
    }

    function publishRide(uint16 _id, string calldata _fromTime, string calldata _toTime, string calldata _location, uint _baseCost, uint16 _avSeats) public {
        idToRide[_id].driver = payable(msg.sender); // Driver
        idToRide[_id].available = true; // Disponibilidad
        idToRide[_id].payed = false; // Pagada
        idToRide[_id].fromTime = _fromTime; // Tiempo de inicio
        idToRide[_id].toTime = _toTime; // Tiempo de fin
        idToRide[_id].location = _location; // Lugar
        idToRide[_id].baseCost = _baseCost; // Costo minimo
        idToRide[_id].avSeats = _avSeats; // Asientos
        //driverToIds[msg.sender].push(_id); // Aregar id a arreglo de ids de ese usuario
    }

    function bidForRide(uint16 _id) public payable {
        require(msg.sender != idToRide[_id].driver, "The bidder cannot be the driver");
        require(msg.value >= idToRide[_id].baseCost, "The bid cannot be lower than the base cost");
        require(msg.value > idToRide[_id].addressToBid[idToRide[_id].highestBidder], "The bid cannot be lower than the highest bid");
        require(msg.sender != idToRide[_id].highestBidder, "The bidder cannot be the highest bidder");
        require(idToRide[_id].available == true, "The bidding time has expired");
        if(idToRide[_id].addressToBid[msg.sender] > 0) { // Si el bidder ya habia hecho un bid
            idToRide[_id].addressToPreviousBid[msg.sender] += idToRide[_id].addressToBid[msg.sender]; // acumular el bid anterior
        }else{ // Si es su primer bid
            idToRide[_id].bidders.push(payable(msg.sender));
        }
        idToRide[_id].addressToBid[msg.sender] = msg.value; // Guardar el bid actual
        idToRide[_id].highestBidder = msg.sender; // Registrar como highest bidder
    }

    function closeRide(uint16 _id) public {
        require(idToRide[_id].driver == msg.sender, "Only the driver can close the ride");
        idToRide[_id].available = false;
    }

    function payRide(uint16 _id) public {
        require(idToRide[_id].driver == msg.sender, "Only the driver can initialize the payments");
        require(idToRide[_id].available == false, "The bidding time has not expired"); // Requerir que no este disponible
        require(idToRide[_id].payed == false, "The ride has been paid"); // Requerir que no haya sido pagada previamente
        for(uint i=0; i<idToRide[_id].bidders.length; i++){
            if(idToRide[_id].bidders[i] == idToRide[_id].highestBidder){ // Si el bidder es el highest bidder
                idToRide[_id].driver.transfer(idToRide[_id].addressToBid[idToRide[_id].highestBidder]); // pagar al driver
                idToRide[_id].bidders[i].transfer(idToRide[_id].addressToPreviousBid[idToRide[_id].bidders[i]]); // regresar bid previo
            }else{  // Si el bidder no gano
                idToRide[_id].bidders[i].transfer(idToRide[_id].addressToBid[idToRide[_id].bidders[i]]); // regresar bid mas grande
                idToRide[_id].bidders[i].transfer(idToRide[_id].addressToPreviousBid[idToRide[_id].bidders[i]]); // y el resto de bids
            }
        }
        idToRide[_id].rider = idToRide[_id].highestBidder; // Registrar al highset bidder como el rider
        idToRide[_id].payed = true; // Pagado
    }
}