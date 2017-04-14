/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var SignInFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(SignInFormViewModel, FormViewModel);

	document.addEventListener('DOMContentLoaded', function () {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('sign-in-form');
		var formVm = new SignInFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
