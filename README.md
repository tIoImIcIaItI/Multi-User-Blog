# Multi-user Blog Submission

## Project Description

 A web application that provides a basic blog service. Registered users can post content, vote, and comment.

## Reviewing the Code

The [`.`](./), [`entries/`](entries/), and [`users/`](users/) folders contains the server-side application code, written in Python 2.7.

The [`static/`](static/) folder contains the custom client-side (JavaScript) application code [`static/js/app/`](static/js/app/), styles [`static/css/`](static/css/), and server-side (Jinja2) HTML template files [`static/templates/`](static/templates/).

3rd-party components and frameworks are used as follows.

- Google App Engine (GAE), webapp2, and Jinja2 serve the HTTP endpoints.
- GAE and NDB serve as the data store and API.
- UIKit provides foundational styling and utility CSS classes (ex. alerts, error styling).
- jQuery 3 is used only as a dependency of UIKit.
- Font Awesome provides scalable icons/glyphs.
- Google Fonts

## Running the App

The app is hosted on Google's cloud.

Open [`multi-user-blog-djking.appspot.com`](https://multi-user-blog-djking.appspot.com/) in a modern browser.

## Using the App

The user is initially presented with a list of all posts. Clicking a post presents the post content, comments, and votes. Authenticated users have additonal UI to create, edit, and delete as appropriate.

Authentication and user account details are managed by the application.

### Application Logic

#### Functionality for Non-authenticated Users
- View all posts and comments
- Sign up and sign in

#### Additional Functionality for Authenticated Users
- Create posts and comments
- Edit posts and comments they created
- Delete posts and comments they created
- Vote up or down, the posts of others (one vote per post)
- Sign out

### Validation

Form input validation occurs both server-side, and client-side on input, change, blur and submit.
Each form input will change color and display an error message if validation fails.
Aria attributes are used to mark invalid fields.
Browsers that do not block invalid form submittal will instead display an alert.
All browsers will show validation errors if an invalid form submit is attempted.

### Accessibility

Aria attributes and HTML semantic elements have been used throughout, for both static and dynamic content.
Error conditions and user alerts are announced via the aria `alert` role.
Contrast has been verified sufficient.
Visual states, icons, images, etc. are accessibly labeled.
Tab order and inclusion has been managed such that only and all interactive elements are navigable.
Interactive elements are of a minimum size.

### Error Handling

For the HTML endpoints, recoverable errors or user issues will display an alert banner, marked up with aria.

### Known Issues

- [UX] A redirect to a welcome page utilizing cookies is required by the ruberic.
- [UX] There are no limits on the number of entries displayed (no paging).

## Attributions

### Souce Code

The following were used in building the app and/or its execution.
- GAE Sessions [Prahlad Yeri](https://prahladyeri.wordpress.com/2013/11/21/how-to-handle-sessions-in-google-app-engine/)
- Email Validation [Scott Brady](https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script)

The client-side form validation and enhancement is carried forward from my [Meet Up Event Planner](https://github.com/tIoImIcIaItI/Meet-Up-Event-Planner) project, and includes the following attributions.

- Input Dirty Class:  [Google](https://developers.google.com/web/fundamentals/design-and-ui/input/forms/provide-real-time-validation?hl=en)
- Password Validation Regex: [The Art Of Web](http://www.the-art-of-web.com/javascript/validate-password/)
- Element.remove(): [Stack Overflow](http://stackoverflow.com/questions/3387427/remove-element-by-id)
- Element.prependChild(): [CallMeNick](http://callmenick.com/post/prepend-child-javascript)
- insertAfter(): [Stack Overflow](http://stackoverflow.com/a/4793630/6452184)
- Array.includes(): [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes)
- Standard Polyfills: [MDN](https://developer.mozilla.org)
- Random Number Utilities: [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random)
