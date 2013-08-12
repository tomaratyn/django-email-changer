# Django Email Changer

Django app to securely change a user's email. This app will email your user at the new email with an activation URL. Once they click the link in the email, the new email will be put into their user account.


## Settings

Django Email Changer has some custom settings it looks for.

### `EMAIL_CHANGE_NOTIFICATION_SUBJECT`

The subject of email change notifications.

Default: `"Email Change Activation"`

### `EMAIL_CHANGE_NOTIFICATION_EMAIL_TEMPLATE`

The template for email change notifications.

Default: `"django_email_changer/email_change_notification.txt"`

### `EMAIL_CHANGE_NOTIFICATION_FROM`

Who is the email change notification from.

Default: `"no-reply@example.com"`

### `EMAIL_CHANGE_ACTIVATION_SUCCESS_URL`

When a user activates their email, we'll redirect to this URL so you can execute your code.

Default: `"/user-email-changed"`

### `EMAIL_CHANGE_SUCCESS_URL`

After a successfully submitting a new email, the user is forwarded to this URL.

Default: `"/new-email-activation-sent"`

### `CHANGE_EMAIL_CODE_EXPIRY_TIME`

A dictionary of arguments for `datetime.timedelta`. If modification is more than `CHANGE_EMAIL_CODE_EXPIRY_TIME` days/hours/minutes/etc old then the modification will not be applied.

Default: `{"days": 3}`