/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var SignUpFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(SignUpFormViewModel, FormViewModel);

	document.addEventListener('DOMContentLoaded', function () {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('sign-up-form');
		var formVm = new SignUpFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
