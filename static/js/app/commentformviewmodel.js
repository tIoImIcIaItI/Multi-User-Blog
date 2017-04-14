/*globals document */
/*globals subclass */
/*globals FormViewModel */

(function (global, document) {
	'use strict';

	// Constructor
	// ReSharper disable once InconsistentNaming
	var CommentFormViewModel = function (form) {
		FormViewModel.call(this, form);
	};

	subclass(CommentFormViewModel, FormViewModel);

	document.addEventListener('DOMContentLoaded', function() {
		// Create, configure, and initialize the form view model
		var formEl = document.getElementById('comment-form');
		if (!formEl) return; // comment form only present for authenticated users

		var formVm = new CommentFormViewModel(formEl);
		formVm.onSubmitValid = function () { return true; };
		formVm.setInitialFocus();
	});

	// ReSharper disable once ThisInGlobalContext
}(this, document));
