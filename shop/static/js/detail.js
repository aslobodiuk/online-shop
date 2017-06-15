function out_of_stock(){
	if (stock < (+$("#id_quantity").val() + +in_cart)){
		alert("Недостаточно товара на складе");
		return false;
	};
	return true;
};

$(document).ready(function(){
	$("#add_to_cart").on('submit', function(){
		if (out_of_stock()) return true;
		return false;
	});
});