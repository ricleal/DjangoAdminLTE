/**
 * Converts a number to Scientific Notation Use for example as: <script
 * language="javascript"> document.write(to_scientific_notation({{
 * run.protonCharge }})); </script>
 */
function to_scientific_notation(num, decimals) {
	if (typeof (decimals) === 'undefined')
		decimals = 2;
	try {
		var ret = num.toExponential(decimals);
		return ret;
	} catch (e) {
		return num;
	}
};

/**
 * Remove duplicates from an array:
 * Use as:
 * uniqueCoords = uniq(coordinates, [].join)
 * See: http://stackoverflow.com/questions/14415787/remove-duplicate-element-pairs-from-multidimensional-array
 */

uniq = function(items, key) {
    var set = {};
    return items.filter(function(item) {
        var k = key ? key.apply(item) : item;
        return k in set ? false : set[k] = true;
    })
}

	

/*******************************************************************************
 * Autocomplete
 */

/**
 * Populates the autocomplete for data for runs for a certain experiment_id
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

// Used in the cancel buttons
function goBack() {
	window.history.back();
};

/*******************************************************************************
 * Function used instead of the default django delete It posts to the DeleteView
 * Call as: delete_object("{% url 'sans:eq-sans_reduction_delete' object.id %}", "{{object.title}}", "{{ csrf_token }}");
 * 
 */
function delete_object(delete_url, object_title, csrf_token) {
	BootstrapDialog.show({
		type : BootstrapDialog.TYPE_WARNING,
		title : 'Delete?',
		message : 'Are you sure you want to delete  ' + object_title + '?',
		buttons : [
				{
					label : 'Cancel',
					action : function(dialogRef) {
						dialogRef.close();
					}
				},
				{
					label : 'Delete',
					cssClass : 'btn-warning',
					action : function(dialogRef) {
						dialogRef.close();
						$.ajax({
							type : "POST",
							url : delete_url,
							data : {
								csrfmiddlewaretoken : csrf_token
							},
							success : function(result) {
								document.open();
								document.write(result);
								document.close();
							},
							error : function(xhr, ajaxOptions, thrownError) {
								BootstrapDialog.show({
									type : BootstrapDialog.TYPE_DANGER,
									message : 'Error deleting the object!<br/>'
											+ thrownError
								});
							}
						});
					}
				} ]
	});
}
