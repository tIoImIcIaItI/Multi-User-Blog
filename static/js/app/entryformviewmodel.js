/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var EntryFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(EntryFormViewModel, FormViewModel);

	document.addEventListener('DOMContentLoaded', function() {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('entry-form');
		var formVm = new EntryFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
