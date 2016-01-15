/**
*  Converts a number to Scientific Notation
* Use for example as:
* <script language="javascript"> document.write(to_scientific_notation({{ run.protonCharge }})); </script>
*/
function to_scientific_notation(num, decimals) {
    if (typeof(decimals)==='undefined') decimals = 2;
    try {
        var ret = num.toExponential(decimals);
        return ret;
    } catch (e) {
        return num;
    }
};


/**********************************************************************
 * Autocomplete
 */

/**
 * Populates the autocomplete for data for runs
 * for a certain experiment_id
 *  
 */

/*******************************************************************************
 * Function to populate the autocomplete from a remote json. This is used on a
 * field that needs a single run number!
 */
function set_autocomplete(selector, jsonurl) {
	$.ajax({
		url : jsonurl,
		type : 'get',
		dataType : 'json',
		async : true,
		success : function(data) {
			// console.log(data);
			$(selector).autocomplete({
				source : data,
				minLength : 0,
				// fires the change event on selection!
				select : function(event, ui) {
					this.value = ui.item.value;
					$(this).trigger('change');
					return false;
				},
			}).bind('focus', function() {
				if (!$(this).val().trim()) {
					$(this).keydown();
				}
			});
		},
	});
}

